# modules/models/zigzag_model.py
from typing import Tuple, Optional, List
from modules.models.base_model import AnalysisModel
from modules.game_manager import GameManager

class ZigZagModel(AnalysisModel):
    """
    ZigZag pattern analysis model for Baccarat
    
    This model looks for alternating patterns (zigzags) between Player and Banker
    and predicts that the pattern will continue.
    """
    def __init__(self, game_manager: GameManager):
        super().__init__(game_manager)
        self.name = "ZigZag Modeli"
        self.description = "Analiz player ve banker arasındaki zigzag desenlerini"
        self.min_pattern_length = 3
    
    def analyze(self) -> Tuple[str, Optional[str]]:
        """
        Analyze the game history for zigzag patterns
        
        Returns:
            Tuple containing:
                - Status message (str)
                - Prediction ('P', 'B', or None for no prediction)
        """
        history = self.game_manager.get_history()
        
        # Need at least 5 results for a meaningful analysis
        if len(history) < 5:
            return "Yetersiz veri", None
        
        # Look for zigzag patterns in the recent history
        # A zigzag is when results alternate: P-B-P-B or B-P-B-P
        
        # Check the most recent pattern (last 6 results)
        recent = history[-6:] if len(history) >= 6 else history
        
        # Check if we have a perfect zigzag pattern
        is_zigzag = True
        for i in range(1, len(recent)):
            if recent[i] == recent[i-1]:
                is_zigzag = False
                break
        
        # If we have a zigzag pattern, predict the opposite of the last result
        if is_zigzag and len(recent) >= 3:
            self.confidence = 85  # Base confidence
            # Increase confidence with longer patterns
            self.confidence += min(len(recent) - 3, 3) * 3
            
            # Predict the opposite of the last result to continue the zigzag
            prediction = 'P' if recent[-1] == 'B' else 'B'
            return f"ZigZag x {len(recent)}", prediction
        
        # Check for partial zigzag (last 3-4 results)
        if len(recent) >= 4:
            last_four = recent[-4:]
            if last_four[0] != last_four[1] and last_four[1] != last_four[2] and last_four[2] != last_four[3]:
                self.confidence = 75
                prediction = 'P' if last_four[-1] == 'B' else 'B'
                return "ZigZag x 4", prediction
        
        if len(recent) >= 3:
            last_three = recent[-3:]
            if last_three[0] != last_three[1] and last_three[1] != last_three[2]:
                self.confidence = 65
                prediction = 'P' if last_three[-1] == 'B' else 'B'
                return "ZigZag x 3", prediction
        
        # No clear zigzag pattern found
        self.confidence = 0
        return "ZigZag tespit edilmedi", None