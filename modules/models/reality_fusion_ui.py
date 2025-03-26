# modules/reality_fusion_ui.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QProgressBar, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QFont, QKeyEvent
from modules.models.reality_layers_model import RealityLayersModel

class RealityLayersWidget(QWidget):
    """
    UI Component for the Reality Layers Fusion (Digital Shamanism) experience
    
    This widget provides a visual interface for the Reality Layers model,
    including environmental visualizations, ritual phase indicators, and
    interactive elements.
    """
    # Signal for key events
    key_pressed = pyqtSignal(QKeyEvent)
    
    def __init__(self, reality_model: RealityLayersModel):
        super().__init__()
        self.reality_model = reality_model
        
        # UI elements
        self.fusion_bar = None
        self.message_label = None
        self.ritual_indicator = None
        self.color_indicator = None
        self.cosmic_prompt_label = None
        self.activation_button = None
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_visuals)
        self.animation_timer.start(100)  # Update every 100ms
        
        # Pulse effect for ritual indicator
        self.pulse_value = 0
        self.pulse_increasing = True
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QWidget {
                background-color: #1A1F2E;
                color: #FFFFFF;
                font-family: 'Inter', sans-serif;
            }
            QLabel {
                color: #EEEEFF;
            }
            QProgressBar {
                border: 2px solid #3C4154;
                border-radius: 5px;
                text-align: center;
                background-color: #2A2A3A;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                stop:0 #6E48AA, stop:1 #9D50BB);
                border-radius: 3px;
            }
            QFrame {
                border-radius: 8px;
                background-color: #232938;
            }
            QPushButton {
                background-color: #3D3D68;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #4E4E88;
            }
        """)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("✨ Gerçeklik Katmanları Füzyonu ✨")
        title_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #BB9EFF;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        main_layout.addLayout(header_layout)
        
        # Ritual phase indicator
        phase_frame = QFrame()
        phase_frame.setFrameShape(QFrame.Shape.Box)
        phase_layout = QVBoxLayout(phase_frame)
        
        phase_header = QLabel("Ritüel Aşaması")
        phase_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phase_header.setStyleSheet("color: #BB9EFF; font-weight: bold;")
        phase_layout.addWidget(phase_header)
        
        self.ritual_indicator = QLabel("Uyanış Bekleniyor")
        self.ritual_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ritual_indicator.setStyleSheet("""
            background-color: #2E3446; 
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            color: #64B5F6;
        """)
        phase_layout.addWidget(self.ritual_indicator)
        
        main_layout.addWidget(phase_frame)
        
        # Fusion level progress bar
        fusion_frame = QFrame()
        fusion_frame.setFrameShape(QFrame.Shape.Box)
        fusion_layout = QVBoxLayout(fusion_frame)
        
        fusion_header = QLabel("Füzyon Seviyesi")
        fusion_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fusion_header.setStyleSheet("color: #BB9EFF; font-weight: bold;")
        fusion_layout.addWidget(fusion_header)
        
        self.fusion_bar = QProgressBar()
        self.fusion_bar.setRange(0, 100)
        self.fusion_bar.setValue(0)
        self.fusion_bar.setTextVisible(True)
        self.fusion_bar.setFixedHeight(20)
        fusion_layout.addWidget(self.fusion_bar)
        
        main_layout.addWidget(fusion_frame)
        
        # Environmental color indicator
        color_frame = QFrame()
        color_frame.setFrameShape(QFrame.Shape.Box)
        color_layout = QHBoxLayout(color_frame)
        
        color_label = QLabel("Ortam Enerjisi:")
        color_label.setStyleSheet("color: #AAAACC;")
        color_layout.addWidget(color_label)
        
        self.color_indicator = QFrame()
        self.color_indicator.setFixedSize(30, 30)
        self.color_indicator.setStyleSheet("background-color: #000000; border-radius: 15px;")
        color_layout.addWidget(self.color_indicator)
        color_layout.addStretch()
        
        main_layout.addWidget(color_frame)
        
        # Message area
        message_frame = QFrame()
        message_frame.setFrameShape(QFrame.Shape.Box)
        message_layout = QVBoxLayout(message_frame)
        
        message_header = QLabel("Matris Mesajı")
        message_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_header.setStyleSheet("color: #BB9EFF; font-weight: bold;")
        message_layout.addWidget(message_header)
        
        self.message_label = QLabel("Matris uyanıyor... Dijital şamanizm başlıyor.")
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            background-color: #2E3446; 
            border-radius: 8px;
            padding: 15px;
            color: #C8E6FF;
            font-style: italic;
        """)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        message_layout.addWidget(self.message_label)
        
        main_layout.addWidget(message_frame)
        
        # Cosmic prompt
        prompt_frame = QFrame()
        prompt_frame.setFrameShape(QFrame.Shape.Box)
        prompt_layout = QVBoxLayout(prompt_frame)
        
        prompt_header = QLabel("Kozmik Ritüel")
        prompt_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prompt_header.setStyleSheet("color: #BB9EFF; font-weight: bold;")
        prompt_layout.addWidget(prompt_header)
        
        self.cosmic_prompt_label = QLabel("Ekrana odaklanın ve gerçeklik katmanlarının birleşmesini bekleyin...")
        self.cosmic_prompt_label.setWordWrap(True)
        self.cosmic_prompt_label.setStyleSheet("""
            background-color: #2E3446; 
            border-radius: 8px;
            padding: 15px;
            color: #FFD700;
            font-weight: bold;
        """)
        self.cosmic_prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prompt_layout.addWidget(self.cosmic_prompt_label)
        
        main_layout.addWidget(prompt_frame)
        
        # Activation button
        button_layout = QHBoxLayout()
        self.activation_button = QPushButton("Füzyon Başlat")
        self.activation_button.setFixedHeight(50)
        self.activation_button.setStyleSheet("""
            background-color: #3D3D68;
            font-size: 16px;
        """)
        self.activation_button.clicked.connect(self.toggle_fusion)
        button_layout.addWidget(self.activation_button)
        
        main_layout.addLayout(button_layout)
        
    def update_visuals(self):
        """Update visual elements based on the reality model state"""
        # Update fusion level
        fusion_level = self.reality_model.get_fusion_level()
        self.fusion_bar.setValue(fusion_level)
        
        # Update color indicator based on environmental color
        env_color = self.reality_model.get_environmental_color()
        self.color_indicator.setStyleSheet(f"""
            background-color: rgb({env_color.red()}, {env_color.green()}, {env_color.blue()});
            border-radius: 15px;
        """)
        
        # Update ritual phase indicator
        ritual_phase = self.reality_model.get_ritual_phase()
        phase_texts = [
            "Uyanış Bekleniyor", 
            "Uyanış Başladı", 
            "Uyumlanma Sağlandı", 
            "Aşkınlık Gerçekleşti"
        ]
        phase_colors = ["#64B5F6", "#4CAF50", "#FF9800", "#BB9EFF"]
        
        # Create pulse effect for ritual indicator
        if self.pulse_increasing:
            self.pulse_value += 5
            if self.pulse_value >= 100:
                self.pulse_increasing = False
        else:
            self.pulse_value -= 5
            if self.pulse_value <= 0:
                self.pulse_increasing = True
                
        # Calculate pulsing color
        base_color = QColor(phase_colors[ritual_phase])
        pulse_factor = self.pulse_value / 100.0
        pulsed_r = min(255, base_color.red() + int(pulse_factor * 50))
        pulsed_g = min(255, base_color.green() + int(pulse_factor * 50))
        pulsed_b = min(255, base_color.blue() + int(pulse_factor * 50))
        
        self.ritual_indicator.setText(phase_texts[ritual_phase])
        self.ritual_indicator.setStyleSheet(f"""
            background-color: #2E3446; 
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            color: rgb({pulsed_r}, {pulsed_g}, {pulsed_b});
            border: 1px solid rgb({pulsed_r}, {pulsed_g}, {pulsed_b});
        """)
        
        # Update message from model
        if self.reality_model.last_message:
            self.message_label.setText(self.reality_model.last_message)
        
        # Update cosmic prompt occasionally
        if fusion_level > 25 and ritual_phase >= 1 and random.random() < 0.01:  # 1% chance per update
            self.cosmic_prompt_label.setText(self.reality_model.get_cosmic_prompt())
            
    def toggle_fusion(self):
        """Toggle the reality fusion on/off"""
        if not self.reality_model.fusion_active:
            # Start fusion
            self.reality_model.fusion_active = True
            self.activation_button.setText("Füzyon Devam Ediyor...")
            self.activation_button.setStyleSheet("""
                background-color: #9D50BB;
                font-size: 16px;
            """)
            # Boost fusion level
            current_level = self.reality_model.fusion_level
            self.reality_model.fusion_level = min(current_level + 20, 100)
        else:
            # Pause fusion
            self.reality_model.fusion_active = False
            self.activation_button.setText("Füzyon Başlat")
            self.activation_button.setStyleSheet("""
                background-color: #3D3D68;
                font-size: 16px;
            """)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events"""
        # Process in the model
        self.reality_model.process_key_press(event)
        # Emit signal for parent widgets
        self.key_pressed.emit(event)
        # Pass to parent
        super().keyPressEvent(event)
        
    def get_message(self) -> str:
        """Get the current message from the reality model"""
        return self.reality_model.last_message
        
    def set_message(self, message: str):
        """Set a custom message in the reality model"""
        self.reality_model.last_message = message
        self.message_label.setText(message)
        
    def get_fusion_active(self) -> bool:
        """Check if fusion is currently active"""
        return self.reality_model.fusion_active