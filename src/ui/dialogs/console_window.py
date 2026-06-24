
import logging
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QMetaObject, Q_ARG

class StreamRedirector(QObject):
    """Redirects stream output to a signal (thread-safe)."""
    text_written = pyqtSignal(str)
    
    def write(self, text):
        # Filter out empty writes (often happens with print)
        if text and text.strip():
            self.text_written.emit(text)
            
    def flush(self):
        pass

    def isatty(self):
        return False

class ConsoleWindow(QWidget):
    """Detached console window for application logs."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kraftbeat Console")
        self.resize(800, 600)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Consolas", 10))
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a10;
                color: #a0a0b0;
                border: none;
                padding: 8px;
            }
        """)
        layout.addWidget(self.console_output)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #202025; border-top: 1px solid #303040;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        
        clear_btn = QPushButton("Clear Console")
        clear_btn.clicked.connect(self.console_output.clear)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #404050;
                color: #e0e0e0;
                border: none;
                padding: 4px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #505060; }
            QPushButton:pressed { background-color: #303040; }
        """)
        toolbar_layout.addWidget(clear_btn)
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar)
        
        self.log_handler = None
        self.stdout_redirector = None
        self.stderr_redirector = None

    def append_text(self, text):
        """Thread-safe append text."""
        cursor = self.console_output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text + "\\n")
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()

    def setup_logging(self):
        """Connect application logging and stdout/stderr to this console window."""
        try:
            # Import here to avoid circular dependencies if any
            from ui.workers import QTextEditLogger
            
            # --- 1. Python Logging ---
            root_logger = logging.getLogger()
            
            # Remove previous handlers if any (to avoid duplicates)
            for h in root_logger.handlers[:]:
                if isinstance(h, QTextEditLogger) and h.widget == self.console_output:
                    root_logger.removeHandler(h)
            
            # Create new handler
            self.log_handler = QTextEditLogger(self.console_output)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
            self.log_handler.setFormatter(formatter)
            root_logger.addHandler(self.log_handler)
            root_logger.setLevel(logging.INFO)
            
            # --- 2. Stdout/Stderr Redirection ---
            # Restore original streams first if we already redirected (cleanup)
            if hasattr(sys.stdout, 'text_written'):
                 sys.stdout = sys.__stdout__
            if hasattr(sys.stderr, 'text_written'):
                 sys.stderr = sys.__stderr__

            self.stdout_redirector = StreamRedirector()
            self.stdout_redirector.text_written.connect(self.append_text)
            sys.stdout = self.stdout_redirector
            
            self.stderr_redirector = StreamRedirector()
            self.stderr_redirector.text_written.connect(self.append_text)
            sys.stderr = self.stderr_redirector
            
            logging.info("Console window attached to logger, stdout, and stderr.")

            
        except ImportError as e:
            sys.__stderr__.write(f"Error: Could not import QTextEditLogger for console window: {e}\n")
        except Exception as e:
            sys.__stderr__.write(f"Error setting up console logging: {e}\n")

    def closeEvent(self, event):
        """Hide instead of close to preserve logs."""
        event.ignore()
        self.hide()
