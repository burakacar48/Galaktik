# Baccarat Analyzer with Martingale System

Modern Baccarat analysis application built with Python and PyQt6. This application helps track Baccarat game results, analyzes patterns, and provides predictions based on different models.

## Features

- Track Player (P) and Banker (B) results in a visual grid
- Analyze patterns with the ZigZag model (additional models can be added)
- Built-in Martingale betting system with customizable parameters
- Simulation capability for testing strategies
- Modern, responsive UI with dark theme

## Installation

1. Ensure you have Python 3.6+ installed.
2. Install PyQt6:
```
pip install PyQt6
```
3. Clone or download this repository.

## Project Structure

```
baccarat-analyzer/
├── main.py                  # Main entry point
├── modules/                 # Core modules
│   ├── __init__.py          # Package initialization
│   ├── main_window.py       # Main UI implementation
│   ├── game_manager.py      # Game state and history management
│   ├── analysis_engine.py   # Analysis and prediction engine
│   ├── martingale_system.py # Betting system implementation
│   ├── models/              # Analysis models
│   │   ├── __init__.py      # Models package initialization
│   │   ├── base_model.py    # Base model abstract class
│   │   ├── zigzag_model.py  # ZigZag pattern analysis
```

## Usage

Run the application using:

```
python main.py
```

- Click the P or B buttons to record game results
- Use the "Simüle Et" button to generate random results for testing
- Use the "Sıfırla" button to reset all data

## Adding New Models

To add a new analysis model:

1. Create a new model class in the `modules/models` directory (inheriting from `AnalysisModel`)
2. Implement the `analyze()` method to return a status and prediction
3. Register the model in the `AnalysisEngine` class by adding it to the models dictionary

Example:

```python
# In modules/models/your_model.py
from modules.models.base_model import AnalysisModel

class YourModel(AnalysisModel):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.name = "Your Model Name"
        
    def analyze(self):
        # Your analysis logic here
        return "Status message", "P"  # or "B" or None
```

Then register it in the analysis engine:

```python
# In modules/analysis_engine.py
from modules.models.your_model import YourModel

# Inside AnalysisEngine.__init__:
self.register_model('your_model', YourModel(game_manager))
```

And add UI elements in the main window to display the results.

## License

MIT License