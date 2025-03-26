# modules/models/base_model.py
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from modules.game_manager import GameManager

class AnalysisModel(ABC):
    """
    Base class for Baccarat analysis models
    """
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager
        self.confidence = 0
        self.name = "Base Model"
        self.description = "Base model description"
    
    @abstractmethod
    def analyze(self) -> Tuple[str, Optional[str]]:
        """
        Analyze the game history and make a prediction
        
        Returns:
            Tuple containing:
                - Status message (str)
                - Prediction ('P', 'B', or None for no prediction)
        """
        pass
    
    def get_confidence(self) -> int:
        """
        Get the confidence level for the prediction
        
        Returns:
            Confidence level as a percentage (0-100)
        """
        return self.confidence