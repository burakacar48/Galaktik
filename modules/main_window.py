# modules/main_window.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
                           QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from modules.game_manager import GameManager
from modules.analysis_engine import AnalysisEngine
from modules.martingale_system import MartingaleSystem

class BaccaratAnalyzerWindow(QMainWindow):
    """Main window for the Baccarat Analyzer application"""
    def __init__(self, game_manager: GameManager, analysis_engine: AnalysisEngine, 
                 martingale: MartingaleSystem):
        super().__init__()
        
        self.game_manager = game_manager
        self.analysis_engine = analysis_engine
        self.martingale = martingale
        
        # UI elements
        self.grid_layout = None
        self.game_info = None
        self.prediction_icon = None
        self.confidence_value = None
        self.win_streak = None
        self.loss_streak = None
        self.cash_value = None
        self.bet_value = None
        self.step_label = None
        self.current_bet_info = None
        self.model_status = {}
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Baccarat Analyzer - Martingale Düzeltildi!")
        self.setMinimumSize(800, 600)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1A1F2E;
                color: #FFFFFF;
            }
            QPushButton {
                border-radius: 8px;
                font-weight: bold;
                min-height: 40px;
            }
            QLabel {
                color: #FFFFFF;
            }
            QScrollArea, QScrollBar {
                background-color: #232938;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #232938;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #64B5F6;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)
        
        # Left panel (Game History)
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.Box)
        left_panel.setStyleSheet("QFrame { background-color: #232938; border-radius: 10px; }")
        left_layout = QVBoxLayout(left_panel)
        
        # Game history header
        history_header = QLabel("Son Girdiler")
        history_header.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        left_layout.addWidget(history_header)
        
        # Game history grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        left_layout.addWidget(self.grid_widget)
        
        # Game info
        self.game_info = QLabel("Girdi: 0 (Analiz için min 5)")
        self.game_info.setStyleSheet("color: #AAAACC;")
        left_layout.addSpacing(20)  # Add some space
        left_layout.addWidget(self.game_info, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Player and Banker buttons
        buttons_layout = QHBoxLayout()
        
        self.p_button = QPushButton("P")
        self.p_button.setFixedSize(130, 50)
        self.p_button.setStyleSheet("background-color: #3DD598; color: white; font-size: 22px;")
        self.p_button.clicked.connect(lambda: self.add_result('P'))
        
        self.b_button = QPushButton("B")
        self.b_button.setFixedSize(130, 50)
        self.b_button.setStyleSheet("background-color: #F97777; color: white; font-size: 22px;")
        self.b_button.clicked.connect(lambda: self.add_result('B'))
        
        buttons_layout.addWidget(self.p_button)
        buttons_layout.addWidget(self.b_button)
        left_layout.addSpacing(60)  # Add more space before buttons
        left_layout.addLayout(buttons_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.simulate_button = QPushButton("Simüle Et")
        self.simulate_button.setFixedSize(110, 40)
        self.simulate_button.setStyleSheet("background-color: #2E3446; border: 1px solid #3DD598;")
        self.simulate_button.clicked.connect(self.simulate)
        
        self.reset_button = QPushButton("Sıfırla")
        self.reset_button.setFixedSize(110, 40)
        self.reset_button.setStyleSheet("background-color: #2E3446; border: 1px solid #3DD598;")
        self.reset_button.clicked.connect(self.reset_data)
        
        action_layout.addWidget(self.simulate_button)
        action_layout.addWidget(self.reset_button)
        left_layout.addSpacing(20)
        left_layout.addLayout(action_layout)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel, 1)
        
        # Right Panel
        right_panel = QVBoxLayout()
        
        # Prediction center
        prediction_panel = QFrame()
        prediction_panel.setFrameShape(QFrame.Shape.Box)
        prediction_panel.setStyleSheet("QFrame { background-color: #232938; border-radius: 10px; }")
        prediction_layout = QVBoxLayout(prediction_panel)
        
        prediction_header = QLabel("🔥 Tahmin Merkezi 🔥")
        prediction_header.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        prediction_header.setStyleSheet("color: #FF9C40;")
        prediction_layout.addWidget(prediction_header)
        
        pred_content = QHBoxLayout()
        
        self.prediction_icon = QLabel("P")
        self.prediction_icon.setFixedSize(70, 70)
        self.prediction_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prediction_icon.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        self.prediction_icon.setStyleSheet("background-color: #3DD598; border-radius: 8px; color: white;")
        pred_content.addWidget(self.prediction_icon)
        
        confidence_layout = QVBoxLayout()
        confidence_label = QLabel("Güven")
        confidence_label.setStyleSheet("color: #AAAACC;")
        self.confidence_value = QLabel("95%")
        self.confidence_value.setFont(QFont("Inter", 36, QFont.Weight.Bold))
        self.confidence_value.setStyleSheet("color: #3DD598;")
        confidence_layout.addWidget(confidence_label)
        confidence_layout.addWidget(self.confidence_value)
        pred_content.addLayout(confidence_layout)
        
        prediction_layout.addLayout(pred_content)
        
        streak_layout = QHBoxLayout()
        self.win_streak = QLabel("🏆 En Yüksek Kazanç Serisi: 0")
        self.win_streak.setStyleSheet("color: #FFD700;")
        self.loss_streak = QLabel("📉 En Yüksek Kayıp Serisi: 0")
        self.loss_streak.setStyleSheet("color: #F97777;")
        streak_layout.addWidget(self.win_streak)
        streak_layout.addWidget(self.loss_streak)
        prediction_layout.addLayout(streak_layout)
        
        right_panel.addWidget(prediction_panel)
        
        # Martingale Tracking
        martingale_panel = QFrame()
        martingale_panel.setFrameShape(QFrame.Shape.Box)
        martingale_panel.setStyleSheet("QFrame { background-color: #232938; border-radius: 10px; }")
        martingale_layout = QVBoxLayout(martingale_panel)
        
        martingale_header = QLabel("💰 Martingale Takibi 💰")
        martingale_header.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        martingale_header.setStyleSheet("color: #FF79C6;")
        martingale_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        martingale_layout.addWidget(martingale_header)
        
        # Cash info
        cash_layout = QHBoxLayout()
        cash_label = QLabel("Kasa:")
        cash_label.setStyleSheet("color: #AAAACC;")
        self.cash_value = QLabel(f"{self.martingale.cash} TL")
        self.cash_value.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        cash_layout.addWidget(cash_label)
        cash_layout.addStretch()
        cash_layout.addWidget(self.cash_value)
        martingale_layout.addLayout(cash_layout)
        
        # Next bet info
        bet_layout = QHBoxLayout()
        bet_label = QLabel("Sıradaki Bahis:")
        bet_label.setStyleSheet("color: #AAAACC;")
        self.bet_value = QLabel(f"{self.martingale.next_bet} TL")
        self.bet_value.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.bet_value.setStyleSheet("color: #FFD700;")
        bet_layout.addWidget(bet_label)
        bet_layout.addStretch()
        bet_layout.addWidget(self.bet_value)
        martingale_layout.addLayout(bet_layout)
        
        # Step info
        step_layout = QHBoxLayout()
        step_status = self.martingale.get_status()
        self.step_label = QLabel(f"Adım: {step_status['current_step']} / {step_status['max_steps']}")
        self.step_label.setStyleSheet("color: #AAAACC;")
        step_layout.addWidget(self.step_label)
        martingale_layout.addLayout(step_layout)
        
        # Current bet info
        self.current_bet_info = QLabel("Tahmin Yapıldı (2 TL)")
        self.current_bet_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_bet_info.setStyleSheet("background-color: #2E3446; padding: 8px; border-radius: 6px; color: #AAAACC;")
        martingale_layout.addWidget(self.current_bet_info)
        
        right_panel.addWidget(martingale_panel)
        
        # Detailed Analysis Section
        analysis_panel = QFrame()
        analysis_panel.setFrameShape(QFrame.Shape.Box)
        analysis_panel.setStyleSheet("QFrame { background-color: #232938; border-radius: 10px; }")
        analysis_layout = QVBoxLayout(analysis_panel)
        
        analysis_header = QLabel("📊 Detaylı Analiz 📊")
        analysis_header.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        analysis_header.setStyleSheet("color: #64B5F6;")
        analysis_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        analysis_layout.addWidget(analysis_header)
        
        # Analysis content with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Headers
        header_layout = QHBoxLayout()
        model_header = QLabel("Analiz Modeli")
        model_header.setStyleSheet("color: #AAAACC; font-weight: bold;")
        status_header = QLabel("Durum / Başarı")
        status_header.setStyleSheet("color: #AAAACC; font-weight: bold;")
        pred_header = QLabel("Tahmin")
        pred_header.setStyleSheet("color: #AAAACC; font-weight: bold;")
        
        header_layout.addWidget(model_header, 2)
        header_layout.addWidget(status_header, 2)
        header_layout.addWidget(pred_header, 1)
        scroll_layout.addLayout(header_layout)
        
        # ZigZag model row
        zigzag_layout = QHBoxLayout()
        zigzag_name = QLabel("ZigZag Modeli")
        self.zigzag_status = QLabel("Bekleniyor...")
        self.zigzag_pred = QLabel("-")
        self.zigzag_pred.setStyleSheet("color: #3DD598;")
        
        zigzag_layout.addWidget(zigzag_name, 2)
        zigzag_layout.addWidget(self.zigzag_status, 2)
        zigzag_layout.addWidget(self.zigzag_pred, 1)
        scroll_layout.addLayout(zigzag_layout)
        
        # Store model status widgets for easy updating
        self.model_status['zigzag'] = (self.zigzag_status, self.zigzag_pred)
        
        # Add placeholder for future models
        placeholder = QLabel("(Diğer modeller yakında eklenecek...)")
        placeholder.setStyleSheet("color: #AAAACC; font-style: italic; margin-top: 10px;")
        scroll_layout.addWidget(placeholder)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        analysis_layout.addWidget(scroll_area)
        
        right_panel.addWidget(analysis_panel)
        main_layout.addLayout(right_panel, 1)
        
        # Initialize UI
        self.update_ui()
    
    def add_result(self, result):
        """
        Add a new game result (Player or Banker)
        
        Args:
            result: 'P' for Player or 'B' for Banker
        """
        # Add result to game manager
        self.game_manager.add_result(result)
        
        # Update analysis
        if len(self.game_manager.get_history()) >= 5:
            analysis_results = self.analysis_engine.analyze()
            
            # Update martingale system with prediction if available
            prediction, confidence = self.analysis_engine.get_current_prediction()
            if prediction:
                self.martingale.place_bet(prediction)
        
        # Process result for martingale system
        self.martingale.process_result(result)
        
        # Update UI
        self.update_ui()
    
    def update_ui(self):
        """Update all UI elements based on current game state"""
        # Update game history grid
        self.update_grid()
        
        # Update game info
        history = self.game_manager.get_history()
        self.game_info.setText(f"Girdi: {len(history)} (Analiz için min 5)")
        
        # Update stats
        stats = self.game_manager.get_stats()
        self.win_streak.setText(f"🏆 En Yüksek Kazanç Serisi: {stats['longest_p_streak']}")
        self.loss_streak.setText(f"📉 En Yüksek Kayıp Serisi: {stats['longest_b_streak']}")
        
        # Update prediction
        prediction, confidence = self.analysis_engine.get_current_prediction()
        if prediction:
            self.prediction_icon.setText(prediction)
            self.prediction_icon.setStyleSheet(
                f"background-color: {'#3DD598' if prediction == 'P' else '#F97777'}; " +
                "border-radius: 8px; color: white;"
            )
            self.confidence_value.setText(f"{confidence}%")
        else:
            self.prediction_icon.setText("-")
            self.prediction_icon.setStyleSheet("background-color: #2E3446; border-radius: 8px; color: white;")
            self.confidence_value.setText("0%")
        
        # Update martingale info
        martingale_status = self.martingale.get_status()
        self.cash_value.setText(f"{martingale_status['cash']} TL")
        self.bet_value.setText(f"{martingale_status['next_bet']} TL")
        self.step_label.setText(f"Adım: {martingale_status['current_step']} / {martingale_status['max_steps']}")
        
        if martingale_status['prediction']:
            self.current_bet_info.setText(f"Tahmin Yapıldı ({martingale_status['next_bet']} TL)")
        else:
            self.current_bet_info.setText("Tahmin bekleniyor...")
        
        # Update model status
        if len(history) >= 5:
            analysis_results = self.analysis_engine.analyze()
            for model_name, result in analysis_results.items():
                if model_name in self.model_status:
                    status_label, pred_label = self.model_status[model_name]
                    status_label.setText(result['status'])
                    
                    if result['prediction']:
                        pred_label.setText(result['prediction'])
                        pred_label.setStyleSheet(
                            f"color: {'#3DD598' if result['prediction'] == 'P' else '#F97777'};"
                        )
                    else:
                        pred_label.setText("-")
                        pred_label.setStyleSheet("color: #AAAACC;")
    
    def update_grid(self):
        """Update the grid display with the game history"""
        # Clear the grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Get recent history for the 5x5 grid
        display_history = self.game_manager.get_display_history(25)
        if not display_history:
            return
        
        # Fill the grid with the most recent results first
        row, col = 0, 0
        for result in display_history:
            label = QLabel(result)
            label.setFixedSize(50, 50)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Inter", 22, QFont.Weight.Bold))
            
            if result == 'P':
                label.setStyleSheet("background-color: #3DD598; border-radius: 8px; color: white;")
            else:  # 'B'
                label.setStyleSheet("background-color: #F97777; border-radius: 8px; color: white;")
            
            self.grid_layout.addWidget(label, row, col)
            
            # Move to next column, or wrap to next row
            col += 1
            if col >= 5:
                col = 0
                row += 1
    
    def simulate(self):
        """Run a simulation of Baccarat results"""
        self.game_manager.simulate(20)  # Generate 20 results
        self.update_ui()
    
    def reset_data(self):
        """Reset all game data"""
        self.game_manager.reset()
        self.martingale.reset()
        self.update_ui()