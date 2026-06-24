"""
Kraftbeat - Theme Management

Dark and light theme styling with animations and polish.
"""

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


def apply_dark_theme(widget) -> str:
    """Apply dark color scheme to widget. Returns stylesheet."""
    palette = QPalette()
    
    # Base colors
    bg_dark = QColor(30, 30, 35)
    bg_mid = QColor(45, 45, 52)
    fg = QColor(220, 220, 225)
    accent = QColor(100, 140, 255)
    
    palette.setColor(QPalette.ColorRole.Window, bg_dark)
    palette.setColor(QPalette.ColorRole.WindowText, fg)
    palette.setColor(QPalette.ColorRole.Base, bg_mid)
    palette.setColor(QPalette.ColorRole.AlternateBase, bg_dark)
    palette.setColor(QPalette.ColorRole.Text, fg)
    palette.setColor(QPalette.ColorRole.Button, bg_mid)
    palette.setColor(QPalette.ColorRole.ButtonText, fg)
    palette.setColor(QPalette.ColorRole.Highlight, accent)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    widget.setPalette(palette)
    
    return DARK_STYLESHEET


def apply_light_theme(widget) -> str:
    """Apply light color scheme to widget. Returns stylesheet."""
    palette = QPalette()
    
    # Base colors
    bg_light = QColor(245, 245, 250)
    bg_mid = QColor(235, 235, 242)
    fg = QColor(30, 30, 35)
    accent = QColor(80, 120, 220)
    
    palette.setColor(QPalette.ColorRole.Window, bg_light)
    palette.setColor(QPalette.ColorRole.WindowText, fg)
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, bg_mid)
    palette.setColor(QPalette.ColorRole.Text, fg)
    palette.setColor(QPalette.ColorRole.Button, bg_mid)
    palette.setColor(QPalette.ColorRole.ButtonText, fg)
    palette.setColor(QPalette.ColorRole.Highlight, accent)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    widget.setPalette(palette)
    
    return LIGHT_STYLESHEET


# Dark theme stylesheet with polish
DARK_STYLESHEET = """
    /* Main window gradient background */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #1a1a22, stop:1 #252530);
    }
    
    /* Group boxes with subtle glow */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #404050;
        border-radius: 10px;
        margin-top: 14px;
        padding-top: 14px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2d2d38, stop:1 #252530);
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 14px;
        padding: 2px 10px;
        color: #a0a0ff;
    }
    
    /* Polished buttons with gradient and glow effect */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #7a9fff, stop:1 #5070e0);
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        color: white;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #90afff, stop:1 #6080f0);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #5060c0, stop:1 #4050a0);
    }
    QPushButton:disabled {
        background: #404050;
        color: #707080;
    }
    QPushButton:checked {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #60c080, stop:1 #40a060);
    }
    
    /* Modern slider with glow */
    QSlider::groove:horizontal {
        height: 8px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #303040, stop:1 #404050);
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        width: 18px;
        height: 18px;
        background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
            stop:0 #90afff, stop:1 #648cff);
        border-radius: 9px;
        margin: -5px 0;
        border: 2px solid #648cff;
    }
    QSlider::handle:horizontal:hover {
        background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
            stop:0 #b0cfff, stop:1 #7a9fff);
    }
    
    /* Input fields with focus glow */
    QComboBox, QSpinBox, QDoubleSpinBox {
        padding: 8px 12px;
        border: 2px solid #404050;
        border-radius: 6px;
        background: #2a2a35;
        selection-background-color: #648cff;
    }
    QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
        border-color: #606080;
    }
    QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #648cff;
    }
    
    /* Text areas with polish */
    QTextEdit, QLineEdit {
        border: 2px solid #404050;
        border-radius: 8px;
        padding: 10px;
        background: #2a2a35;
        selection-background-color: #648cff;
    }
    QTextEdit:focus, QLineEdit:focus {
        border-color: #648cff;
    }
    
    /* Progress bar with animated look */
    QProgressBar {
        border: 2px solid #404050;
        border-radius: 6px;
        text-align: center;
        background: #252530;
        color: white;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #648cff, stop:0.5 #90afff, stop:1 #648cff);
        border-radius: 4px;
    }
    
    /* List widget polish */
    QListWidget {
        border: 2px solid #404050;
        border-radius: 8px;
        background: #2a2a35;
        padding: 4px;
    }
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }
    QListWidget::item:hover {
        background: #353545;
    }
    QListWidget::item:selected {
        background: #648cff;
        color: white;
    }
    
    /* Tab widget styling */
    QTabWidget::pane {
        border: 1px solid #404050;
        border-radius: 8px;
        background: #1a1a20;
    }
    QTabBar::tab {
        background: #2a2a35;
        color: #909090;
        padding: 10px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }
    QTabBar::tab:hover {
        background: #353545;
        color: #c0c0c0;
    }
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #7a9fff, stop:1 #648cff);
        color: white;
    }
    
    /* Checkbox styling */
    QCheckBox {
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid #404050;
        background: #2a2a35;
    }
    QCheckBox::indicator:checked {
        background: #648cff;
        border-color: #648cff;
    }
    
    /* Tooltip styling */
    QToolTip {
        background: #1a1a22;
        color: #e0e0e5;
        border: 1px solid #648cff;
        border-radius: 4px;
        padding: 6px 10px;
    }
    
    /* Status bar */
    QStatusBar {
        background: #1a1a20;
        color: #a0a0a5;
    }
"""

# Light theme stylesheet - Cool grey tones (easy on eyes)
LIGHT_STYLESHEET = """
    /* Main window and base - cool light grey */
    QMainWindow, QWidget {
        background: #e0e2e6;
        color: #2c2c32;
    }
    
    /* Labels */
    QLabel {
        color: #2c2c32;
        background: transparent;
    }
    
    /* Group boxes - grey gradient */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #b8bcc4;
        border-radius: 10px;
        margin-top: 14px;
        padding-top: 14px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #eef0f4, stop:1 #e2e4e8);
        color: #2c2c32;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 14px;
        padding: 2px 10px;
        color: #4060a0;
    }
    
    /* Buttons - vibrant blue gradient */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #6088ec, stop:1 #4060c0);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #7098fc, stop:1 #5070d0);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4050a0, stop:1 #304080);
    }
    QPushButton:disabled {
        background: #d0d0e0;
        color: #909090;
    }
    QPushButton:checked {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #50b070, stop:1 #309050);
    }
    /* Sliders - cool grey with blue accent */
    QSlider::groove:horizontal {
        height: 8px;
        background: #c8ccd4;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        width: 18px;
        height: 18px;
        background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
            stop:0 #7090d0, stop:1 #5070b0);
        border-radius: 9px;
        margin: -5px 0;
        border: 2px solid #5070b0;
    }
    QSlider::handle:horizontal:hover {
        background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
            stop:0 #80a0e0, stop:1 #6080c0);
    }
    
    /* Combo boxes, spinboxes - grey background */
    QComboBox, QSpinBox, QDoubleSpinBox {
        padding: 8px 12px;
        border: 2px solid #b8bcc4;
        border-radius: 6px;
        background: #eef0f4;
        color: #2c2c32;
        selection-background-color: #4060a0;
    }
    QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
        border-color: #98a0ac;
    }
    QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #4060a0;
    }
    QComboBox::drop-down {
        border: none;
        background: transparent;
    }
    QComboBox QAbstractItemView {
        background: #eef0f4;
        color: #2c2c32;
        border: 1px solid #b8bcc4;
        selection-background-color: #4060a0;
        selection-color: white;
    }
    /* Text areas - grey background */
    QTextEdit, QLineEdit, QPlainTextEdit {
        border: 2px solid #b8bcc4;
        border-radius: 8px;
        padding: 10px;
        background: #eef0f4;
        color: #2c2c32;
        selection-background-color: #4060a0;
    }
    QTextEdit:focus, QLineEdit:focus, QPlainTextEdit:focus {
        border-color: #4060a0;
    }
    
    /* Progress bar */
    QProgressBar {
        border: 2px solid #b8bcc4;
        border-radius: 6px;
        text-align: center;
        background: #d4d8e0;
        color: #2c2c32;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #4060a0, stop:0.5 #6080c0, stop:1 #4060a0);
        border-radius: 4px;
    }
    
    /* List widget - grey */
    QListWidget {
        border: 2px solid #b8bcc4;
        border-radius: 8px;
        background: #eef0f4;
        color: #2c2c32;
        padding: 4px;
    }
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
        color: #2c2c32;
    }
    QListWidget::item:hover {
        background: #d4d8e0;
    }
    QListWidget::item:selected {
        background: #4060a0;
        color: white;
    }
    
    /* Tab widget - grey with blue accents */
    QTabWidget::pane {
        border: 1px solid #b8bcc4;
        border-radius: 8px;
        background: #e8eaee;
    }
    QTabBar::tab {
        background: #d4d8e0;
        color: #404048;
        padding: 10px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }
    QTabBar::tab:hover {
        background: #c8ccd4;
        color: #2c2c32;
    }
    QTabBar::tab:selected {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #6080c0, stop:1 #4060a0);
        color: white;
    }
    
    /* Checkbox - grey with blue check */
    QCheckBox {
        spacing: 8px;
        color: #2c2c32;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid #b8bcc4;
        background: #eef0f4;
    }
    QCheckBox::indicator:hover {
        border-color: #98a0ac;
    }
    QCheckBox::indicator:checked {
        background: #4060a0;
        border-color: #4060a0;
    }
    
    /* Scroll areas */
    QScrollArea {
        background: #e0e2e6;
        border: none;
    }
    QScrollBar:vertical {
        background: #d4d8e0;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background: #b0b4bc;
        border-radius: 5px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background: #98a0ac;
    }
    QScrollBar:horizontal {
        background: #d4d8e0;
        height: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal {
        background: #b0b4bc;
        border-radius: 5px;
        min-width: 30px;
    }
    
    /* Frames - for drop zones etc */
    QFrame {
        background: #e0e2e6;
        color: #2c2c32;
    }
    
    /* Menu and toolbar */
    QMenuBar {
        background: #d4d8e0;
        color: #2c2c32;
    }
    QMenuBar::item:selected {
        background: #4060a0;
        color: white;
    }
    QMenu {
        background: #eef0f4;
        color: #2c2c32;
        border: 1px solid #b8bcc4;
    }
    QMenu::item:selected {
        background: #4060a0;
        color: white;
    }
    
    /* Tooltip */
    QToolTip {
        background: #eef0f4;
        color: #2c2c32;
        border: 1px solid #4060a0;
        border-radius: 4px;
        padding: 6px 10px;
    }
    
    /* Status bar */
    QStatusBar {
        background: #d4d8e0;
        color: #404048;
    }
    
    /* Dock widgets */
    QDockWidget {
        background: #e0e2e6;
        color: #2c2c32;
    }
    QDockWidget::title {
        background: #d4d8e0;
        color: #2c2c32;
        padding: 8px;
    }
    
    /* Matplotlib canvas background */
    MplCanvas {
        background: #eef0f4;
    }
"""
