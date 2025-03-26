# modules/models/galactic_pattern_model.py
from typing import Tuple, Optional, List
from modules.models.base_model import AnalysisModel
from modules.game_manager import GameManager

class GalacticPatternModel(AnalysisModel):
    """
    Galactic Pattern Analysis Model for Baccarat
    
    This model searches for cosmic patterns and rare sequences in the game history.
    When extremely rare patterns are detected, it triggers a "metamorphosis" event.
    """
    def __init__(self, game_manager: GameManager):
        super().__init__(game_manager)
        self.name = "Galaktik Desen Modeli"
        self.description = "Kozmik bağlantılar ve nadir desenleri analiz eder"
        self.metamorphosis_triggered = False
        self.fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        self.golden_patterns = ['PBPPBPPP', 'BPPBPPPB']  # Golden ratio-inspired patterns
        
    def analyze(self) -> Tuple[str, Optional[str]]:
        """
        Analyze the game history for cosmic patterns
        
        Returns:
            Tuple containing:
                - Status message (str)
                - Prediction ('P', 'B', or None for no prediction)
        """
        history = self.game_manager.get_history()
        
        # Need at least 8 results for a meaningful analysis
        if len(history) < 8:
            return "Yetersiz veri", None
        
        # Convert history to a binary representation (P=1, B=0)
        binary_history = [1 if result == 'P' else 0 for result in history]
        
        # Check for rare pattern types
        status, prediction, confidence = self.check_patterns(history, binary_history)
        
        # Set the confidence level
        self.confidence = confidence
        
        return status, prediction
    
    def check_patterns(self, history: List[str], binary_history: List[int]) -> Tuple[str, Optional[str], int]:
        """
        Check for various cosmic patterns in the history
        
        Returns:
            Tuple containing:
                - Status message
                - Prediction ('P', 'B', or None)
                - Confidence level (0-100)
        """
        # Check for Fibonacci pattern in runs
        if self.check_fibonacci_pattern(history[-8:]):
            self.metamorphosis_triggered = True
            # Predict based on the next Fibonacci number's parity
            next_fib = (self.fibonacci_sequence[7] + self.fibonacci_sequence[6]) % 2
            prediction = 'P' if next_fib == 1 else 'B'
            return "🌌 Fibonacci Kozmik Desen", prediction, 95
        
        # Check for golden ratio inspired patterns
        recent_str = ''.join(history[-8:])
        for pattern in self.golden_patterns:
            if pattern in recent_str:
                self.metamorphosis_triggered = True
                # Predict based on pattern continuation
                prediction = pattern[len(recent_str) % len(pattern)]
                return "✨ Altın Oran Kozmik Desen", prediction, 92
        
        # Check for perfect symmetry
        if self.check_symmetry(history[-8:]):
            # Predict based on symmetry continuation
            mid_point = len(history) // 2
            if len(history) % 2 == 0:  # Even length
                prediction = history[mid_point-1]
            else:  # Odd length
                prediction = 'P' if history[mid_point] == 'B' else 'B'
            return "🪞 Simetrik Kozmik Desen", prediction, 88
        
        # Check for repeating cycles (3-cycle)
        cycle_result = self.check_cycles(history)
        if cycle_result:
            cycle_length, next_val = cycle_result
            prediction = next_val
            return f"🔄 {cycle_length}-Devir Döngüsü", prediction, 85
        
        # Check for balanced distribution (close to 50/50)
        p_count = history[-12:].count('P')
        b_count = len(history[-12:]) - p_count
        if 0.45 <= p_count / len(history[-12:]) <= 0.55:
            # If balanced, predict to maintain balance
            if p_count > b_count:
                return "⚖️ Denge Göstergesi", 'B', 75
            else:
                return "⚖️ Denge Göstergesi", 'P', 75
                
        # Check for trend following (momentum)
        if len(history) >= 5:
            trend = self.detect_trend(history[-5:])
            if trend:
                return "📈 Momentum Göstergesi", trend, 70
        
        # No special pattern detected
        return "Galaktik desen tespit edilmedi", None, 0
    
    def check_fibonacci_pattern(self, recent_history: List[str]) -> bool:
        """Check if recent results follow a Fibonacci-like pattern in runs"""
        if len(recent_history) < 8:
            return False
            
        # Count consecutive runs of P and B
        runs = []
        current_run = 1
        for i in range(1, len(recent_history)):
            if recent_history[i] == recent_history[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)
        
        # Check if run lengths match Fibonacci sequence
        if len(runs) < 3:
            return False
            
        # Check if any 3 consecutive runs form a Fibonacci sequence
        for i in range(len(runs) - 2):
            if runs[i] + runs[i+1] == runs[i+2]:
                return True
                
        return False
    
    def check_symmetry(self, recent_history: List[str]) -> bool:
        """Check for perfect symmetry in recent results"""
        size = len(recent_history)
        mid = size // 2
        
        # For even length sequences
        if size % 2 == 0:
            first_half = recent_history[:mid]
            second_half = recent_history[mid:]
            # Check if second half is mirror of first half
            for i in range(mid):
                if first_half[i] != second_half[mid-i-1]:
                    return False
            return True
        # For odd length sequences
        else:
            first_half = recent_history[:mid]
            second_half = recent_history[mid+1:]
            # Check if second half is mirror of first half
            for i in range(mid):
                if first_half[i] != second_half[mid-i-1]:
                    return False
            return True
    
    def check_cycles(self, history: List[str]) -> Optional[Tuple[int, str]]:
        """Check for repeating cycles in history"""
        if len(history) < 9:  # Need at least 9 results to detect a 3-cycle
            return None
            
        # Check for 3-cycles
        recent = history[-9:]
        if recent[0:3] == recent[3:6] and recent[3:6] == recent[6:9]:
            # Predict the next value based on the cycle
            return 3, recent[0]
            
        # Check for 2-cycles
        if len(history) >= 6:
            recent = history[-6:]
            if recent[0:2] == recent[2:4] and recent[2:4] == recent[4:6]:
                return 2, recent[0]
                
        return None
    
    def detect_trend(self, recent_history: List[str]) -> Optional[str]:
        """Detect if there's a clear trend in recent results"""
        p_count = recent_history.count('P')
        b_count = len(recent_history) - p_count
        
        # If there's a strong trend (>60% in one direction)
        if p_count / len(recent_history) >= 0.6:
            return 'P'  # Continue P trend
        elif b_count / len(recent_history) >= 0.6:
            return 'B'  # Continue B trend
            
        return None
    
    def is_metamorphosis_triggered(self) -> bool:
        """Check if a metamorphosis event has been triggered"""
        return self.metamorphosis_triggered
    
    def reset_metamorphosis(self):
        """Reset the metamorphosis trigger"""
        self.metamorphosis_triggered = False