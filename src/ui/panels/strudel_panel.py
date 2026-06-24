"""
Strudel Live Coding Panel for Kraftbeat.

Embeds the Strudel live coding environment in a QWebEngineView,
fully configured to behave like a real browser tab — with Web Audio,
MIDI, clipboard, and localStorage all working correctly.

Architecture:
  - A background Python HTTP server serves the local strudel_dist/ bundle.
  - A persistent QWebEngineProfile grants the necessary permissions.
  - The toolbar injects presets/themes via JavaScript into the running page.

Strudel is AGPL-3.0. Kraftbeat is also open-source (AGPL compatible).
"""

import logging
import os
import socket
import threading
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from utils.config import get_config

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QTimer, QEvent
from PyQt6.QtGui import QKeySequence

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import (
        QWebEngineProfile,
        QWebEnginePage,
        QWebEngineSettings,
        QWebEnginePermissionRequest,
    )
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    QWebEngineView = None
    # Placeholders to prevent NameError on import when WebEngine is missing
    class QWebEnginePage:
        class PermissionPolicy:
            PermissionGrantedByUser = None
    class QWebEngineProfile:
        class PersistentCookiesPolicy:
            AllowPersistentCookies = None
    class QWebEngineSettings:
        class WebAttribute:
            JavascriptEnabled = None
            JavascriptCanOpenWindows = None
            LocalStorageEnabled = None
            LocalContentCanAccessRemoteUrls = None
            AllowRunningInsecureContent = None
            PlaybackRequiresUserGesture = None
            WebAudioEnabled = None
            FullScreenSupportEnabled = None
            ScrollAnimatorEnabled = None
    class QWebEnginePermissionRequest:
        pass

logger = logging.getLogger(__name__)

# Paths
STRUDEL_LOCAL_PATH  = Path(__file__).parent.parent.parent.parent / "strudel_dist"
STRUDEL_PRESETS_PATH = Path(__file__).parent.parent.parent.parent / "strudel_presets"
STRUDEL_WEB_URL     = "https://strudel.cc"

# Singleton HTTP server
_strudel_server = None
_strudel_server_port = None
_server_lock = threading.Lock()


# ─────────────────────────────────────────────────────────────────────────────
# Local HTTP Server
# ─────────────────────────────────────────────────────────────────────────────

class _QuietHTTPHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass   # silence


def _find_free_port() -> int:
    host = get_config("strudel_host", "127.0.0.1")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


def start_strudel_server() -> int | None:
    global _strudel_server, _strudel_server_port
    with _server_lock:
        if _strudel_server is not None:
            return _strudel_server_port
        if not (STRUDEL_LOCAL_PATH / "index.html").exists():
            return None
        try:
            port = _find_free_port()
            host = get_config("strudel_host", "127.0.0.1")
            handler = partial(_QuietHTTPHandler, directory=str(STRUDEL_LOCAL_PATH))
            srv = HTTPServer((host, port), handler)
            threading.Thread(target=srv.serve_forever, daemon=True,
                             name="StrudelHTTP").start()
            _strudel_server = srv
            _strudel_server_port = port
            logger.info(f"Strudel HTTP server → http://{host}:{port}/")
            return port
        except Exception as e:
            logger.error(f"Strudel server failed: {e}")
            return None


def _get_strudel_url() -> QUrl:
    port = start_strudel_server()
    if port:
        host = get_config("strudel_host", "127.0.0.1")
        return QUrl(f"http://{host}:{port}/")
    logger.info("No local strudel_dist/, loading strudel.cc")
    return QUrl(STRUDEL_WEB_URL)


# ─────────────────────────────────────────────────────────────────────────────
# Strudel-Aware Web Page  (handles permission requests)
# ─────────────────────────────────────────────────────────────────────────────

class _StrudelPage(QWebEnginePage):
    """
    Custom page that auto-grants audio, MIDI, and clipboard permissions so
    Strudel behaves exactly like it does in a real browser.
    """

    def __init__(self, profile: "QWebEngineProfile", parent=None):
        super().__init__(profile, parent)

        # Qt 6.8+ uses permissionRequested signal
        if hasattr(self, "permissionRequested"):
            self.permissionRequested.connect(self._on_permission)

    def _on_permission(self, permission: "QWebEnginePermissionRequest"):
        """Auto-grant all requests (audio context, MIDI, clipboard)."""
        permission.grant()

    # Older Qt 6 API (< 6.8)
    def featurePermissionRequested(self, origin, feature):
        self.setFeaturePermission(
            origin, feature,
            QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
        )

    def javaScriptConsoleMessage(self, level, message, line, source):
        # Forward JS errors to the Python logger for debugging
        lvl = {0: "DEBUG", 1: "INFO", 2: "WARNING", 3: "ERROR"}.get(level, "INFO")
        logger.debug(f"[Strudel JS] ({source}:{line}) {message}")


# ─────────────────────────────────────────────────────────────────────────────
# Preset / Theme helpers (graceful fallback if the strudel modules are absent)
# ─────────────────────────────────────────────────────────────────────────────

def _load_strudel_modules():
    for attempt in [
        lambda: __import__("src.strudel.themes",   fromlist=["STRUDEL_THEMES", "get_theme_css"]),
        lambda: __import__("strudel.themes",        fromlist=["STRUDEL_THEMES", "get_theme_css"]),
    ]:
        try:
            m = attempt()
            return m
        except ImportError as e:
            logger.debug(f"Failed to load strudel modules from attempt: {e}")
    return None

_themes_mod = _load_strudel_modules()

STRUDEL_THEMES: dict = getattr(_themes_mod, "STRUDEL_THEMES", {})
_get_theme_css = getattr(_themes_mod, "get_theme_css", lambda x: "")


# ─────────────────────────────────────────────────────────────────────────────
# Keyboard Proxy — the core fix for arrow/enter/tab swallowing by Qt
# ─────────────────────────────────────────────────────────────────────────────

class _WebKeyFilter:
    """
    Install this on every child widget of a QWebEngineView so that ALL
    keyboard events (arrows, Enter, Backspace, Tab, etc.) go straight to
    Chromium's render widget without Qt intercepting them for focus traversal.

    Usage:
        filter = _WebKeyFilter(web_view)
        filter.install()
    """
    # Qt keys that the surrounding application must still see
    _PASS_THROUGH = {
        Qt.Key.Key_Escape,       # let user close dialogs
        Qt.Key.Key_F5,           # reload shortcut
    }

    def __init__(self, view):
        from PyQt6.QtCore import QObject

        class _Filter(QObject):
            def eventFilter(self_, watched, event):
                if event.type() in (QEvent.Type.KeyPress, QEvent.Type.KeyRelease):
                    key = event.key()
                    # Always pass through application-level shortcuts
                    if key in _WebKeyFilter._PASS_THROUGH:
                        return False
                    # Deliver directly to the web view — do NOT propagate up
                    view.setFocus(Qt.FocusReason.OtherFocusReason)
                    return False   # False = don't block, just make sure focus is right
                return False

        self._view = view
        self._filter_obj = _Filter(view)

    def install(self):
        """
        Walk every child of the QWebEngineView and install the event filter.
        The internal render widget is typically the first QWidget child.
        """
        self._view.installEventFilter(self._filter_obj)
        # Also patch focus proxy if accessible
        proxy = self._view.focusProxy()
        if proxy:
            proxy.installEventFilter(self._filter_obj)
            proxy.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Recurse children added later
        for child in self._view.findChildren(type(self._view)):
            child.installEventFilter(self._filter_obj)


def _get_presets_by_genre() -> dict:
    for mod_path in ["src.strudel.presets", "strudel.presets"]:
        try:
            m = __import__(mod_path, fromlist=["get_presets_by_genre"])
            return m.get_presets_by_genre()
        except Exception as e:
            logger.debug(f"Failed to load strudel presets via {mod_path}: {e}")
    # Fallback: scan the directory directly
    result = {}
    if STRUDEL_PRESETS_PATH.exists():
        for genre_dir in sorted(STRUDEL_PRESETS_PATH.iterdir()):
            if genre_dir.is_dir():
                presets = [
                    {"name": f.stem, "file": f.name}
                    for f in sorted(genre_dir.glob("*.js"))
                ]
                if presets:
                    result[genre_dir.name] = presets
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Main Panel
# ─────────────────────────────────────────────────────────────────────────────

class StrudelPanel(QWidget):
    """Embedded Strudel live-coding tab — feels like a real browser."""

    audio_exported = pyqtSignal(object, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window  = parent
        self.current_theme  = "kraftbeat"
        self.web_view       = None
        self._page          = None
        self._profile       = None
        self._key_filter = None   # set later inside _build_webview
        self._setup_ui()

    # ──────────────────────────────────────────────────────────────────────
    # Focus management — the key to making keyboard work like a real browser
    # ──────────────────────────────────────────────────────────────────────

    def showEvent(self, event):
        """Every time this tab becomes visible, push keyboard focus into Chromium."""
        super().showEvent(event)
        if self.web_view:
            QTimer.singleShot(50, lambda: self.web_view.setFocus(Qt.FocusReason.OtherFocusReason))

    def focusInEvent(self, event):
        """If Qt ever gives focus to the panel widget itself, redirect to the web view."""
        super().focusInEvent(event)
        if self.web_view:
            self.web_view.setFocus(Qt.FocusReason.OtherFocusReason)

    def keyPressEvent(self, event):
        """
        If a key somehow reaches the panel widget (not the web view), forward it.
        This is the last-resort catch-all.
        """
        if self.web_view:
            self.web_view.setFocus(Qt.FocusReason.OtherFocusReason)
        super().keyPressEvent(event)

    # ──────────────────────────────────────────────────────────────────────
    # UI Construction
    # ──────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_toolbar())

        if WEBENGINE_AVAILABLE:
            root.addWidget(self._build_webview(), stretch=1)
        else:
            root.addWidget(self._build_fallback(), stretch=1)

        root.addWidget(self._build_footer())

    def _build_toolbar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("""
            QFrame { background: #1e1e2e; border-bottom: 1px solid #3a3a52; }
            QPushButton {
                background: #2e2e45; border: none; border-radius: 5px;
                padding: 4px 8px; font-size: 13px; color: #ccc;
            }
            QPushButton:hover  { background: #3e3e60; }
            QPushButton:checked{ background: #6d28d9; color: white; }
            QComboBox { background: #2e2e45; border: 1px solid #4a4a68;
                        border-radius: 4px; padding: 3px 6px; color: #ddd; }
            QLineEdit { background: #2e2e45; border: 1px solid #4a4a68;
                        border-radius: 4px; padding: 3px 8px; color: #ddd; }
        """)
        bar.setFixedHeight(46)

        lay = QHBoxLayout(bar)
        lay.setContentsMargins(10, 4, 10, 4)
        lay.setSpacing(6)

        # ── Left: nav controls ──────────────────────────────────────────
        self._back_btn = QPushButton("◀")
        self._back_btn.setToolTip("Back")
        self._back_btn.setFixedWidth(30)
        self._back_btn.clicked.connect(self._nav_back)
        lay.addWidget(self._back_btn)

        self._fwd_btn = QPushButton("▶")
        self._fwd_btn.setToolTip("Forward")
        self._fwd_btn.setFixedWidth(30)
        self._fwd_btn.clicked.connect(self._nav_forward)
        lay.addWidget(self._fwd_btn)

        self._reload_btn = QPushButton("🔄")
        self._reload_btn.setToolTip("Reload (F5)")
        self._reload_btn.setFixedWidth(30)
        self._reload_btn.clicked.connect(self._reload)
        lay.addWidget(self._reload_btn)

        self._home_btn = QPushButton("🏠")
        self._home_btn.setToolTip("Go to Strudel home")
        self._home_btn.setFixedWidth(30)
        self._home_btn.clicked.connect(self._go_home)
        lay.addWidget(self._home_btn)

        # ── URL bar ─────────────────────────────────────────────────────
        self._url_bar = QLineEdit()
        self._url_bar.setPlaceholderText("URL")
        self._url_bar.returnPressed.connect(self._navigate_to_url)
        lay.addWidget(self._url_bar, stretch=1)

        lay.addSpacing(8)

        # ── Right: feature buttons ──────────────────────────────────────
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumWidth(90)
        self.theme_combo.setToolTip("Visual theme")
        for tid, tdata in STRUDEL_THEMES.items():
            self.theme_combo.addItem(tdata.get("display_name", tid), tid)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        lay.addWidget(self.theme_combo)

        # Presets
        self.preset_combo = QComboBox()
        self.preset_combo.setMinimumWidth(160)
        self.preset_combo.setToolTip("Load a pattern preset")
        self.preset_combo.addItem("🎼  Select Preset…", None)
        for genre, presets in sorted(_get_presets_by_genre().items()):
            label = genre.replace("_", " ").title()
            for p in presets:
                name = p.get("name", p.get("file", "?"))
                fstem = p.get("file", name).replace(".js", "")
                self.preset_combo.addItem(f"{label}: {name}", (genre, fstem))
        self.preset_combo.currentIndexChanged.connect(self._on_preset_selected)
        lay.addWidget(self.preset_combo)

        self._midi_btn = QPushButton("🎹")
        self._midi_btn.setToolTip("MIDI keyboard input")
        self._midi_btn.setCheckable(True)
        self._midi_btn.setFixedWidth(34)
        self._midi_btn.clicked.connect(self._toggle_midi)
        lay.addWidget(self._midi_btn)

        self._viz_btn = QPushButton("📊")
        self._viz_btn.setToolTip("Oscilloscope visualizer")
        self._viz_btn.setCheckable(True)
        self._viz_btn.setFixedWidth(34)
        self._viz_btn.clicked.connect(self._toggle_viz)
        lay.addWidget(self._viz_btn)

        self._ext_btn = QPushButton("↗")
        self._ext_btn.setToolTip("Open in system browser")
        self._ext_btn.setFixedWidth(30)
        self._ext_btn.clicked.connect(self._open_external)
        lay.addWidget(self._ext_btn)

        return bar

    def _build_webview(self) -> QWebEngineView:
        # ── Persistent profile so localStorage / IndexedDB survive reloads ──
        profile_path = str(
            Path(__file__).parent.parent.parent.parent / ".strudel_profile"
        )
        self._profile = QWebEngineProfile("kraftbeat_strudel")
        self._profile.setPersistentStoragePath(profile_path)
        self._profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
        )

        # ── Permissive settings ──────────────────────────────────────────
        s = self._profile.settings()
        for attr, val in [
            (QWebEngineSettings.WebAttribute.JavascriptEnabled,              True),
            (QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows,       True),
            (QWebEngineSettings.WebAttribute.LocalStorageEnabled,            True),
            (QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,True),
            (QWebEngineSettings.WebAttribute.AllowRunningInsecureContent,    True),
            (QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture,    False),
            (QWebEngineSettings.WebAttribute.WebAudioEnabled,                True),
            (QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,       True),
            (QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled,          True),
        ]:
            try:
                s.setAttribute(attr, val)
            except Exception as e:
                logger.debug(f"Qt attribute {attr} not supported/exposed: {e}")

        # ── Custom page with permission grants ───────────────────────────
        self._page = _StrudelPage(self._profile)

        # ── Web view ───────────────────────────────────────────────────
        self.web_view = QWebEngineView()
        self.web_view.setPage(self._page)

        # ── Critical: focus policy so Qt never steals keyboard from Chromium ──
        self.web_view.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Tab key must go to the editor, not traverse Qt widgets
        self.web_view.setTabOrder(self.web_view, self.web_view)

        self.web_view.setUrl(_get_strudel_url())
        self.web_view.loadFinished.connect(self._on_load_finished)
        self.web_view.urlChanged.connect(self._on_url_changed)

        # Install keyboard proxy AFTER the view is constructed so
        # Chromium's internal render widget already exists as a child.
        self._key_filter = _WebKeyFilter(self.web_view)
        # Defer install until the view has actually created its child widgets
        QTimer.singleShot(500, self._key_filter.install)

        logger.info("Strudel panel: QWebEngineView ready")
        return self.web_view

    def _build_fallback(self) -> QLabel:
        lbl = QLabel(
            "<h2>🎹 Strudel Live Coding</h2>"
            "<p><b>PyQt6-WebEngine</b> is not installed.</p>"
            "<pre style='background:#1e1e1e;padding:12px;border-radius:6px;'>"
            "pip install PyQt6-WebEngine</pre>"
            "<p>Or visit <a href='https://strudel.cc'>strudel.cc</a> directly.</p>"
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color:#a0a0b8; padding:40px;")
        lbl.setOpenExternalLinks(True)
        self.web_view = None
        return lbl

    def _build_footer(self) -> QFrame:
        foot = QFrame()
        foot.setStyleSheet("""
            QFrame { background:#181824; border-top:1px solid #2e2e45; }
        """)
        foot.setFixedHeight(30)
        lay = QHBoxLayout(foot)
        lay.setContentsMargins(12, 0, 12, 0)
        tip = QLabel(
            "💡 <b>Ctrl+Enter</b> to run &nbsp;|&nbsp; "
            "<b>Ctrl+.</b> to stop &nbsp;|&nbsp; "
            "Choose a preset to start instantly"
        )
        tip.setStyleSheet("color:#55556e; font-size:11px;")
        lay.addWidget(tip)
        lay.addStretch()

        self._status_label = QLabel()
        self._status_label.setStyleSheet("color:#55557e; font-size:11px;")
        lay.addWidget(self._status_label)
        return foot

    # ──────────────────────────────────────────────────────────────────────
    # Navigation
    # ──────────────────────────────────────────────────────────────────────

    def _nav_back(self):
        if self.web_view: self.web_view.back()

    def _nav_forward(self):
        if self.web_view: self.web_view.forward()

    def _reload(self):
        if self.web_view: self.web_view.reload()

    def _go_home(self):
        if self.web_view: self.web_view.setUrl(_get_strudel_url())

    def _navigate_to_url(self):
        if not self.web_view: return
        url = self._url_bar.text().strip()
        if url and not url.startswith("http"):
            url = "https://" + url
        self.web_view.setUrl(QUrl(url))
        # Give keyboard focus back to the web content immediately
        QTimer.singleShot(100, lambda: self.web_view.setFocus(Qt.FocusReason.OtherFocusReason))

    def _on_url_changed(self, url: QUrl):
        self._url_bar.setText(url.toString())

    def _on_load_finished(self, ok: bool):
        if ok:
            self._apply_theme(self.current_theme)
            self._status_label.setText("✅ Loaded")
            QTimer.singleShot(3000, lambda: self._status_label.setText(""))
            # Re-install key filter after each page load (new render widget)
            QTimer.singleShot(300, self._key_filter.install)
            # Give keyboard focus to the editor automatically
            QTimer.singleShot(400, lambda: self.web_view.setFocus(Qt.FocusReason.OtherFocusReason))
        else:
            self._status_label.setText("⚠️ Load failed — check internet?")

    # ──────────────────────────────────────────────────────────────────────
    # Theme
    # ──────────────────────────────────────────────────────────────────────

    def _on_theme_changed(self, _):
        tid = self.theme_combo.currentData()
        if tid:
            self.current_theme = tid
            self._apply_theme(tid)

    def _apply_theme(self, theme_id: str):
        if not self.web_view: return
        css = _get_theme_css(theme_id)
        if not css: return
        esc = css.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        self.web_view.page().runJavaScript(f"""
        (function(){{
            var id='kraftbeat-theme';
            var el=document.getElementById(id);
            if(el)el.remove();
            el=document.createElement('style');
            el.id=id;
            el.textContent=`{esc}`;
            document.head.appendChild(el);
        }})();
        """)

    # ──────────────────────────────────────────────────────────────────────
    # Presets
    # ──────────────────────────────────────────────────────────────────────

    def _on_preset_selected(self, _):
        data = self.preset_combo.currentData()
        if data:
            genre, fstem = data
            self._load_preset(genre, fstem)

    def _load_preset(self, genre: str, file_stem: str):
        if not self.web_view: return
        preset_path = STRUDEL_PRESETS_PATH / genre / f"{file_stem}.js"
        if not preset_path.exists():
            logger.warning(f"Preset not found: {preset_path}")
            return
        code = preset_path.read_text(encoding="utf-8")
        esc  = (code
                .replace("\\", "\\\\")
                .replace("`",  "\\`")
                .replace("$",  "\\$")
                .replace("\r\n", "\\n")
                .replace("\n", "\\n"))
        js = f"""
        (function(){{
            var code=`{esc}`;
            // Method 1: Strudel global repl
            if(window.repl&&window.repl.setCode){{window.repl.setCode(code);return;}}
            // Method 2: CodeMirror EditorView
            if(window.view&&window.view.dispatch){{
                window.view.dispatch({{changes:{{from:0,to:window.view.state.doc.length,insert:code}}}});return;}}
            // Method 3: DOM query for CodeMirror
            var cm=document.querySelector('.cm-content');
            if(cm&&cm.cmView&&cm.cmView.view){{
                var v=cm.cmView.view;
                v.dispatch({{changes:{{from:0,to:v.state.doc.length,insert:code}}}});return;}}
            // Fallback: clipboard
            navigator.clipboard.writeText(code).then(
                ()=>alert('Preset copied — press Ctrl+A, Ctrl+V to paste.'));
        }})();
        """
        self.web_view.page().runJavaScript(js)
        logger.info(f"Loaded preset: {genre}/{file_stem}")

    # ──────────────────────────────────────────────────────────────────────
    # MIDI & Visualizer (delegate to JS helpers if available)
    # ──────────────────────────────────────────────────────────────────────

    def _toggle_midi(self, checked: bool):
        if not self.web_view: return
        js = (
            "if(!window.__midiInputActive){"
            "  navigator.requestMIDIAccess().then(a=>{"
            "    a.inputs.forEach(i=>{ i.onmidimessage=e=>{"
            "      console.log('MIDI',e.data);"
            "    };});"
            "    window.__midiInputActive=true;"
            "    console.log('Kraftbeat MIDI ready');"
            "  });"
            "}"
            if checked else
            "window.__midiInputActive=false;"
        )
        self.web_view.page().runJavaScript(js)

    def _toggle_viz(self, checked: bool):
        if not self.web_view: return
        if checked:
            js = """
            (function(){
                if(document.getElementById('kb-viz'))return;
                var c=document.createElement('canvas');
                c.id='kb-viz';
                c.style='position:fixed;bottom:0;left:0;width:100%;height:120px;z-index:9999;opacity:0.85;background:#0a0a12;';
                document.body.appendChild(c);
                var ctx=c.getContext('2d');
                var ac=new(window.AudioContext||window.webkitAudioContext)();
                var an=ac.createAnalyser(); an.fftSize=1024;
                ac.resume();
                // Tap into the Strudel context
                if(window.getAudioContext){var sac=getAudioContext();var src=sac.createMediaStreamDestination();sac.destination.connect(an);}
                function draw(){
                    requestAnimationFrame(draw);
                    var d=new Uint8Array(an.frequencyBinCount);
                    an.getByteTimeDomainData(d);
                    ctx.clearRect(0,0,c.width,c.height);
                    ctx.strokeStyle='#a78bfa'; ctx.lineWidth=2; ctx.beginPath();
                    for(var i=0;i<d.length;i++){
                        var x=i/d.length*c.width, y=(d[i]/128-1)*c.height/2+c.height/2;
                        i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
                    }
                    ctx.stroke();
                }
                draw();
            })();
            """
        else:
            js = "var el=document.getElementById('kb-viz');if(el)el.remove();"
        self.web_view.page().runJavaScript(js)

    # ──────────────────────────────────────────────────────────────────────
    # External browser
    # ──────────────────────────────────────────────────────────────────────

    def _open_external(self):
        import webbrowser
        url = self.web_view.url().toString() if self.web_view else STRUDEL_WEB_URL
        webbrowser.open(url)

    # ──────────────────────────────────────────────────────────────────────
    # Public compatibility shims (called from main_window.py)
    # ──────────────────────────────────────────────────────────────────────

    def reload_page(self):
        self._reload()

    def open_external(self):
        self._open_external()

    def navigate_to(self, url: str):
        if self.web_view:
            self.web_view.setUrl(QUrl(url))

    def toggle_midi(self, checked: bool):
        self._midi_btn.setChecked(checked)
        self._toggle_midi(checked)

    def toggle_visualizer(self, checked: bool):
        self._viz_btn.setChecked(checked)
        self._toggle_viz(checked)
