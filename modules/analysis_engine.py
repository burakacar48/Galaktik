# modules/analysis_engine.py
from typing import Dict, List, Tuple
from modules.game_manager import GameManager
from modules.models.base_model import AnalysisModel
from modules.models.zigzag_model import ZigZagModel
from modules.models.galactic_pattern_model import GalacticPatternModel

class AnalysisEngine:
    """
    Handles all analysis, predictions and models for the Baccarat analyzer
    """
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager
        self.models = {}
        self.confidence = 95  # Default confidence
        self.metamorphosis_active = False
        
        # Register models
        self.register_model('zigzag', ZigZagModel(game_manager))
        self.register_model('galactic', GalacticPatternModel(game_manager))
        
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
        highest_confidence = 0
        best_prediction = None
        
        for name, model in self.models.items():
            status, prediction = model.analyze()
            confidence = model.get_confidence()
            
            results[name] = {
                'status': status,
                'prediction': prediction,
                'confidence': confidence
            }
            
            # Keep track of the highest confidence prediction
            if confidence > highest_confidence and prediction is not None:
                highest_confidence = confidence
                best_prediction = prediction
            
            # Check for metamorphosis in galactic model
            if name == 'galactic' and isinstance(model, GalacticPatternModel):
                self.metamorphosis_active = model.is_metamorphosis_triggered()
        
        # Set the overall prediction to the highest confidence one
        if best_prediction:
            self.current_prediction = best_prediction
            self.confidence = highest_confidence
        else:
            # Fall back to zigzag if no high confidence prediction
            if 'zigzag' in results and results['zigzag']['prediction'] is not None:
                self.current_prediction = results['zigzag']['prediction']
                self.confidence = results['zigzag']['confidence']
            else:
                self.current_prediction = None
        
        return results
    
    def get_current_prediction(self) -> Tuple[str, int]:
        """Get the current prediction and confidence level"""
        return self.current_prediction, self.confidence
    
    def is_metamorphosis_active(self) -> bool:
        """Check if a metamorphosis event is currently active"""
        return self.metamorphosis_active
    
    def reset_metamorphosis(self):
        """Reset the metamorphosis state"""
        self.metamorphosis_active = False
        if 'galactic' in self.models:
            if isinstance(self.models['galactic'], GalacticPatternModel):
                self.models['galactic'].reset_metamorphosis()