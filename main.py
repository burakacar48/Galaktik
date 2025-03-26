# main.py
import sys
from PyQt6.QtWidgets import QApplication
from modules.main_window import BaccaratAnalyzerWindow
from modules.game_manager import GameManager
from modules.analysis_engine import AnalysisEngine
from modules.martingale_system import MartingaleSystem

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    
    # Create core modules
    game_manager = GameManager()
    martingale = MartingaleSystem(initial_cash=2818, initial_bet=2, max_steps=8)
    analysis_engine = AnalysisEngine(game_manager)
    
    # Create and show the main window
    window = BaccaratAnalyzerWindow(game_manager, analysis_engine, martingale)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()