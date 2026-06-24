"""
Kraftbeat Voice Lab

Dedicated panel for importing and managing custom voice profiles (cloning)
for use with ACE-Step and other supported audio-to-audio models.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QLineEdit, QFileDialog, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import os
import shutil
from pathlib import Path

VOICES_DIR = os.path.join(os.getcwd(), "models", "voices")

class DragDropArea(QFrame):
    """Area for dragging and dropping audio files."""
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setLineWidth(2)
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #648cff;
                border-radius: 8px;
                background-color: #2a2a35;
            }
        """)
        
        layout = QVBoxLayout(self)
        self.label = QLabel("📥 Drag & Drop Acapella Audio (.wav, .mp3)\nOr Click to Browse")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #808090; font-size: 14px;")
        layout.addWidget(self.label)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    border: 2px dashed #40c040;
                    border-radius: 8px;
                    background-color: #304030;
                }
            """)
            
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #648cff;
                border-radius: 8px;
                background-color: #2a2a35;
            }
        """)
        
    def dropEvent(self, event: QDropEvent):
        self.dragLeaveEvent(event)
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                self.file_dropped.emit(path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a valid audio file.")
                
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.flac *.ogg)"
            )
            if path:
                self.file_dropped.emit(path)


class VoicePanel(QWidget):
    """Voice Lab panel."""
    
    # Emitted when the voice list changes
    voices_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_import_path = None
        self.setup_ui()
        self.refresh_voices()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # Left side: Import
        left_layout = QVBoxLayout()
        
        title = QLabel("🎤 Voice Lab")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(title)
        
        desc = QLabel(
            "Extract voice embeddings for ACE-Step cloning.\n"
            "Provide a clean, 10-15 second vocal recording."
        )
        desc.setStyleSheet("color: #808090; font-style: italic;")
        left_layout.addWidget(desc)
        
        # Drag Drop
        self.drop_area = DragDropArea()
        self.drop_area.file_dropped.connect(self.on_file_dropped)
        left_layout.addWidget(self.drop_area, stretch=2)
        
        # Controls
        controls = QVBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #a0a0b0;")
        controls.addWidget(self.file_label)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Voice Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. My Custom Singer")
        name_layout.addWidget(self.name_input)
        controls.addLayout(name_layout)
        
        self.save_btn = QPushButton("💾 Save Voice Profile")
        self.save_btn.setStyleSheet("background: #648cff; padding: 10px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_voice)
        self.save_btn.setEnabled(False)
        controls.addWidget(self.save_btn)
        
        left_layout.addLayout(controls)
        layout.addLayout(left_layout, stretch=1)
        
        # Right side: Library
        right_layout = QVBoxLayout()
        right_title = QLabel("Saved Profiles")
        right_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(right_title)
        
        self.voice_list = QListWidget()
        self.voice_list.setStyleSheet("background: #1e1e24; border-radius: 4px; padding: 4px;")
        right_layout.addWidget(self.voice_list)
        
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setStyleSheet("background: #c04040;")
        self.delete_btn.clicked.connect(self.delete_voice)
        btn_layout.addStretch()
        btn_layout.addWidget(self.delete_btn)
        right_layout.addLayout(btn_layout)
        
        layout.addLayout(right_layout, stretch=1)
        
    def on_file_dropped(self, path: str):
        self.current_import_path = path
        base = os.path.basename(path)
        self.file_label.setText(f"Selected: {base}")
        
        # Auto-fill name if empty
        if not self.name_input.text().strip():
            name, _ = os.path.splitext(base)
            self.name_input.setText(name)
            
        self.save_btn.setEnabled(True)
        self.drop_area.label.setText("📥 Ready to Save")
        
    def save_voice(self):
        if not self.current_import_path:
            return
            
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Name", "Please provide a name for the voice profile.")
            return
            
        # Ensure dir exists
        os.makedirs(VOICES_DIR, exist_ok=True)
        
        # For cloning, it's best to have wav, but ACE-Step can handle others. 
        # We just copy the file.
        _, ext = os.path.splitext(self.current_import_path)
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        target_file = f"{safe_name}{ext}"
        target_path = os.path.join(VOICES_DIR, target_file)
        
        if os.path.exists(target_path):
            reply = QMessageBox.question(
                self, "Overwrite", "A profile with this name already exists. Overwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
                
        try:
            shutil.copy2(self.current_import_path, target_path)
            QMessageBox.information(self, "Success", f"Voice profile '{name}' saved successfully!")
            
            # Reset
            self.current_import_path = None
            self.file_label.setText("No file selected")
            self.name_input.clear()
            self.save_btn.setEnabled(False)
            self.drop_area.label.setText("📥 Drag & Drop Acapella Audio (.wav, .mp3)\nOr Click to Browse")
            
            self.refresh_voices()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save voice: {e}")
            
    def refresh_voices(self):
        """Reload the list of voices from the directory."""
        self.voice_list.clear()
        if not os.path.exists(VOICES_DIR):
            return
            
        for file in os.listdir(VOICES_DIR):
            if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                self.voice_list.addItem(file)
                
        self.voices_updated.emit()
        
    def delete_voice(self):
        item = self.voice_list.currentItem()
        if not item:
            return
            
        file = item.text()
        path = os.path.join(VOICES_DIR, file)
        
        reply = QMessageBox.question(
            self, "Confirm Deletion", f"Delete voice profile '{file}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path)
                self.refresh_voices()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {e}")
