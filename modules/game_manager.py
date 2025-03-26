# modules/game_manager.py
from typing import List, Tuple

class GameManager:
    """
    Manages the game state, history and statistics
    """
    def __init__(self):
        self.history: List[str] = []  # 'P' for Player, 'B' for Banker
        self.reset()
    
    def reset(self):
        """Reset all game data"""
        self.history.clear()
        
    def add_result(self, result: str):
        """
        Add a new game result
        
        Args:
            result: 'P' for Player or 'B' for Banker
        """
        if result not in ['P', 'B']:
            raise ValueError("Result must be 'P' or 'B'")
        
        self.history.append(result)
        return len(self.history)
    
    def get_history(self) -> List[str]:
        """Return full history"""
        return self.history.copy()
    
    def get_display_history(self, count: int = 25) -> List[str]:
        """
        Get the most recent results for display
        
        Args:
            count: Number of results to return (default 25 for 5x5 grid)
            
        Returns:
            List of most recent results
        """
        return self.history[-count:] if len(self.history) > 0 else []
    
    def get_stats(self) -> dict:
        """Calculate various statistics from the game history"""
        if not self.history:
            return {
                'total': 0,
                'p_count': 0,
                'b_count': 0,
                'p_percentage': 0,
                'b_percentage': 0,
                'longest_p_streak': 0,
                'longest_b_streak': 0,
                'current_streak': {'type': None, 'count': 0}
            }
        
        p_count = self.history.count('P')
        b_count = self.history.count('B')
        total = len(self.history)
        
        # Calculate streaks
        longest_p_streak = 0
        longest_b_streak = 0
        current_streak = 1
        
        for i in range(1, len(self.history)):
            if self.history[i] == self.history[i-1]:
                current_streak += 1
            else:
                # End of streak
                if self.history[i-1] == 'P':
                    longest_p_streak = max(longest_p_streak, current_streak)
                else:
                    longest_b_streak = max(longest_b_streak, current_streak)
                current_streak = 1
        
        # Check the last streak
        if self.history[-1] == 'P':
            longest_p_streak = max(longest_p_streak, current_streak)
            current_streak_type = 'P'
        else:
            longest_b_streak = max(longest_b_streak, current_streak)
            current_streak_type = 'B'
        
        return {
            'total': total,
            'p_count': p_count,
            'b_count': b_count,
            'p_percentage': round(p_count / total * 100, 1) if total > 0 else 0,
            'b_percentage': round(b_count / total * 100, 1) if total > 0 else 0,
            'longest_p_streak': longest_p_streak,
            'longest_b_streak': longest_b_streak,
            'current_streak': {'type': current_streak_type, 'count': current_streak}
        }
    
    def simulate(self, count: int = 100):
        """
        Run a simulation of Baccarat results
        
        Args:
            count: Number of simulated results to generate
        """
        import random
        
        # Baccarat has slightly higher odds for Banker (50.68%)
        # The 1.35% tie probability is ignored and redistributed for this simulation
        for _ in range(count):
            r = random.random()
            if r < 0.4932:  # Player probability
                self.add_result('P')
            else:  # Banker probability
                self.add_result('B')