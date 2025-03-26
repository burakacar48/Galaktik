# modules/martingale_system.py
from typing import Tuple

class MartingaleSystem:
    """
    Implements the Martingale betting system for Baccarat
    """
    def __init__(self, initial_cash: int = 1000, initial_bet: int = 2, max_steps: int = 8):
        self.initial_cash = initial_cash
        self.initial_bet = initial_bet
        self.max_steps = max_steps
        
        self.reset()
    
    def reset(self):
        """Reset the Martingale system to initial state"""
        self.cash = self.initial_cash
        self.next_bet = self.initial_bet
        self.current_step = 1
        self.last_result = None
        self.prediction = None
    
    def place_bet(self, prediction: str):
        """
        Place a bet on the predicted outcome
        
        Args:
            prediction: 'P' for Player or 'B' for Banker
        """
        if prediction not in ['P', 'B']:
            return
        
        self.prediction = prediction
        # Cash is deducted when the result comes in
    
    def process_result(self, result: str) -> bool:
        """
        Process the result of a game
        
        Args:
            result: 'P' for Player or 'B' for Banker
            
        Returns:
            bool: True if we won, False otherwise
        """
        self.last_result = result
        
        # If no prediction was made, nothing to do
        if not self.prediction:
            return False
        
        # Check if we won
        won = (result == self.prediction)
        
        # Update cash based on result
        if won:
            # Player pays 1:1, Banker pays 0.95:1 (5% commission)
            if self.prediction == 'P':
                self.cash += self.next_bet
            else:  # Banker
                self.cash += int(self.next_bet * 0.95)
                
            # Reset the betting sequence
            self.current_step = 1
            self.next_bet = self.initial_bet
        else:
            # We lost
            self.cash -= self.next_bet
            
            # Double the bet for next round, if not at max step
            if self.current_step < self.max_steps:
                self.current_step += 1
                self.next_bet *= 2
            else:
                # Reset if we hit the max step
                self.current_step = 1
                self.next_bet = self.initial_bet
        
        # Clear the prediction for the next round
        prev_prediction = self.prediction
        self.prediction = None
        
        return won and prev_prediction == result
    
    def get_status(self) -> dict:
        """Get the current status of the Martingale system"""
        return {
            'cash': self.cash,
            'next_bet': self.next_bet,
            'current_step': self.current_step,
            'max_steps': self.max_steps,
            'prediction': self.prediction
        }