# modules/analysis_engine.py
from typing import Dict, List, Tuple
from modules.game_manager import GameManager
from modules.models.base_model import AnalysisModel
from modules.models.zigzag_model import ZigZagModel

class AnalysisEngine:
    """
    Handles all analysis, predictions and models for the Baccarat analyzer
    """
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager
        self.models = {}
        self.confidence = 95  # Default confidence
        
        # Register models
        self.register_model('zigzag', ZigZagModel(game_manager))
        
        # Current prediction
        self.current_prediction = None
    
    def register_model(self, name: str, model: AnalysisModel):
        """Register a new analysis model"""
        self.models[name] = model
    
    def analyze(self) -> Dict[str, Dict]:
        """Run analysis using all registered models"""
        results = {}
        
        # Skip analysis if not enough data
        if len(self.game_manager.get_history()) < 5:
            return results
        
        # Run each model
        for name, model in self.models.items():
            status, prediction = model.analyze()
            confidence = model.get_confidence()
            
            results[name] = {
                'status': status,
                'prediction': prediction,
                'confidence': confidence
            }
        
        # Determine the overall prediction (currently just using zigzag model)
        # This will be expanded as more models are added
        if 'zigzag' in results and results['zigzag']['prediction'] is not None:
            self.current_prediction = results['zigzag']['prediction']
            self.confidence = results['zigzag']['confidence']
        else:
            self.current_prediction = None
        
        return results
    
    def get_current_prediction(self) -> Tuple[str, int]:
        """Get the current prediction and confidence level"""
        return self.current_prediction, self.confidence