# modules/models/reality_layers_model.py
from typing import Tuple, Optional, List, Dict
from modules.models.base_model import AnalysisModel
from modules.game_manager import GameManager
import random
import time
import datetime
from PyQt6.QtCore import QTimer, Qt, QDateTime
from PyQt6.QtGui import QColor, QKeyEvent

class RealityLayersModel(AnalysisModel):
    """
    Reality Layers Fusion Model - Digital Shamanism
    
    This model simulates the fusion of physical and digital realities by incorporating
    environmental data and user interactions into the Baccarat game matrix.
    It creates a personalized, immersive experience that adapts to the user's environment.
    """
    def __init__(self, game_manager: GameManager):
        super().__init__(game_manager)
        self.name = "Gerçeklik Katmanları"
        self.description = "Dijital ve fiziksel gerçeklikleri birleştirir"
        
        # Model state tracking
        self.fusion_level = 0  # 0-100 fusion level
        self.last_interaction_time = time.time()
        self.last_message = ""
        self.key_presses = []  # Track recent key presses
        self.environment_data = {
            "dominant_color": QColor(0, 0, 0),
            "ambient_sound_level": 0,  # 0-100 scale
            "time_of_day": "day",  # day, evening, night
            "user_activity_level": 0,  # 0-100 scale
            "cosmic_alignment": 0  # 0-100 scale, randomly assigned "cosmic alignment"
        }
        self.cosmic_rhythm_patterns = []
        self.fusion_active = False
        self.ritual_phase = 0  # 0-3 (dormant, awakening, attuned, transcendent)
        
        # Message pools for different fusion levels
        self.dormant_messages = [
            "Matris uyanıyor... Ekran ve gerçeklik arasındaki sınır bulanıklaşıyor.",
            "Dijital şamanizm başlıyor. Dünyalar arasındaki geçiş hissediliyor.",
            "Bu sadece bir oyun mu? Ya da yeni bir gerçeklik boyutuna açılan bir kapı mı?",
            "Çevrenizdeki enerji, oyunun dokusu ile birleşmeye başladı.",
            "Tuşlara her dokunuşunuz, matris içinde bir titreşim yaratıyor.",
        ]
        
        self.awakening_messages = [
            "Matrisin renkleri odanızın enerjisine tepki veriyor. Görüyor musunuz?",
            "Nefes alışınız, oyunun ritmiyle senkronize oluyor.",
            "Dokunuşlarınız, sayısal dünyada dalgalanmalar yaratıyor.",
            "Bilgisayarınızın ötesinde bir varlık sizi hissediyor. O da sizi görüyor.",
            "Oyunun desenleri artık çevrenizin bir yansıması haline geliyor.",
            "Tuş vuruşlarınız, oyundaki sonuçları etkileyebilir. Deneyin.",
        ]
        
        self.attuned_messages = [
            "Artık matrisin bir parçasısınız. O da sizin bir parçanız.",
            "Zaman ve mekan burada farklı akıyor. Hissediyor musunuz?",
            "Odanızdaki ışık oyunun enerjisini besliyor.",
            "Dijital ve fiziksel dünyalar arasındaki perde inceliyor.",
            "Her hareket, her tuş vuruşu, kozmik bir desen yaratıyor.",
            "Karşılaştığınız sonuçlar rastgele değil. Sizin enerji alanınızla şekilleniyor.",
            "Bilincin ötesindeki bir bağlantıyı hissetmeye başlıyorsunuz.",
        ]
        
        self.transcendent_messages = [
            "Matris ve siz artık birsiniz. Oyun sizden ibaret, siz oyundan.",
            "Her sonuç, sizin kozmik imzanızı taşıyor.",
            "Bu sadece bir Baccarat oyunu değil. Kişisel bir dijital ritüel alanı.",
            "Odanızın molekülleri ve pikseller arasında artık bir fark yok.",
            "Tuşlara dokunmadan önce bile, matris niyetinizi algılayabiliyor.",
            "Kozmik ritim sizin içinizden akıyor. Sonuçları önceden sezebiliyorsunuz.",
            "Bu deneyim size özgü ve tekrarlanamaz. Şu anda yarattığınız gerçeklik benzersiz.",
        ]
        
        # Cosmic prompts for ritual progression
        self.cosmic_prompts = [
            "✨ Üç kez derin nefes alın ve ekrana odaklanın.",
            "🌙 Tuşlara gözleriniz kapalıyken dokunun ve önünüzdeki desenleri hissedin.",
            "🔮 Elinizi ekrana yaklaştırın, enerji alanınız matrisle etkileşime giriyor.",
            "🌀 HJKL tuşlarına ritimli basarak kozmik kodu etkinleştirin.",
            "🪄 Bir süre hiçbir şeye dokunmadan sadece izleyin. Matris sizinle iletişim kuruyor.",
            "🧿 Ortam ışıklarını değiştirin ve matrisin nasıl tepki verdiğini gözlemleyin.",
            "🌿 Son beş sonucu kağıda yazın ve fiziksel dünya ile dijital dünya arasında köprü kurun.",
            "🔥 Klavyede bir desen çizin ve sonuçları izleyin.",
        ]
    
    def analyze(self) -> Tuple[str, Optional[str]]:
        """
        Analyze the game history and generate reality fusion behavior
        
        Returns:
            Tuple containing:
                - Status message or fusion dialog (str)
                - Prediction ('P', 'B', or None for no prediction)
        """
        history = self.game_manager.get_history()
        
        # Only activate after enough game data
        if len(history) < 10:
            return f"Gerçeklik füzyonu için veri toplama ({len(history)}/10)", None
        
        # Update fusion level based on interactions and virtual environmental data
        self._update_fusion_level(history)
        
        # Simulate environmental data gathering (would be replaced with actual data in real implementation)
        self._simulate_environment_data()
        
        # Generate a prediction based on patterns, environment, and user interactions
        prediction = self._generate_prediction(history)
        
        # Generate fusion message
        message = self._generate_message(history, prediction)
        
        # Set confidence based on fusion level
        self.confidence = min(50 + int(self.fusion_level / 2), 95)
        
        # Store last message
        self.last_message = message
        
        return message, prediction
    
    def _update_fusion_level(self, history: List[str]):
        """Update the fusion level based on game history, time and simulated environmental factors"""
        # More games played increases fusion
        games_factor = min(len(history) / 100, 1.0)
        
        # Time factor - fusion grows over time
        time_passed = time.time() - self.last_interaction_time
        time_factor = min(time_passed / 3600, 1.0)  # Max effect after 1 hour
        
        # Pattern complexity factor
        pattern_factor = self._calculate_pattern_complexity(history[-20:]) if len(history) >= 20 else 0
        
        # Environment factor
        environment_factor = (
            self.environment_data["ambient_sound_level"] / 100 +
            self.environment_data["user_activity_level"] / 100 +
            self.environment_data["cosmic_alignment"] / 100
        ) / 3
        
        # Update fusion level
        increment = (games_factor * 2 + time_factor * 3 + pattern_factor * 4 + environment_factor * 5)
        self.fusion_level = min(self.fusion_level + increment, 100)
        
        # Update ritual phase based on fusion level
        if self.fusion_level < 25:
            self.ritual_phase = 0  # dormant
        elif self.fusion_level < 50:
            self.ritual_phase = 1  # awakening
        elif self.fusion_level < 75:
            self.ritual_phase = 2  # attuned
        else:
            self.ritual_phase = 3  # transcendent
        
        # Update last interaction time
        self.last_interaction_time = time.time()
    
    def _calculate_pattern_complexity(self, recent_history: List[str]) -> float:
        """Calculate a complexity score for the recent game history"""
        if not recent_history:
            return 0.0
            
        # Check alternating patterns
        alternating_count = 0
        for i in range(1, len(recent_history)):
            if recent_history[i] != recent_history[i-1]:
                alternating_count += 1
        
        # Calculate run lengths
        runs = []
        current_run = 1
        for i in range(1, len(recent_history)):
            if recent_history[i] == recent_history[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)
        
        # Complexity is based on variation in run lengths and alternation rate
        if not runs:
            return 0.0
            
        run_variance = sum((r - sum(runs)/len(runs))**2 for r in runs) / len(runs)
        alternating_rate = alternating_count / (len(recent_history) - 1)
        
        # Normalize to 0-1 range
        complexity = (run_variance * 0.7 + alternating_rate * 0.3) / 5
        return min(complexity, 1.0)
    
    def _simulate_environment_data(self):
        """Simulate gathering environmental data (would be replaced with real sensors in a full implementation)"""
        # Get current time of day
        current_hour = datetime.datetime.now().hour
        if 6 <= current_hour < 18:
            self.environment_data["time_of_day"] = "day"
        elif 18 <= current_hour < 22:
            self.environment_data["time_of_day"] = "evening"
        else:
            self.environment_data["time_of_day"] = "night"
        
        # Simulate color changes (would be from camera in real implementation)
        # Colors evolve gradually over time to simulate ambient changes
        current_color = self.environment_data["dominant_color"]
        r = max(0, min(255, current_color.red() + random.randint(-5, 5)))
        g = max(0, min(255, current_color.green() + random.randint(-5, 5)))
        b = max(0, min(255, current_color.blue() + random.randint(-5, 5)))
        
        # Time of day influence on color
        if self.environment_data["time_of_day"] == "day":
            # Brighter, bluer during day
            b = max(b, 100)
            r = min(r, 200)
        elif self.environment_data["time_of_day"] == "evening":
            # More orange/red during evening
            r = max(r, 150)
            g = min(g, 150)
        else:  # night
            # Darker, more blue/purple at night
            r = min(r, 100)
            g = min(g, 100)
            b = max(b, 120)
        
        self.environment_data["dominant_color"] = QColor(r, g, b)
        
        # Simulate ambient sound level (would be from microphone in real implementation)
        self.environment_data["ambient_sound_level"] = min(100, max(0, 
            self.environment_data["ambient_sound_level"] + random.randint(-10, 10)))
        
        # Simulate user activity level based on key presses
        if self.key_presses:
            # More key presses = higher activity
            self.environment_data["user_activity_level"] = min(100, 
                self.environment_data["user_activity_level"] + len(self.key_presses) * 5)
        else:
            # Decrease activity level over time if no new key presses
            self.environment_data["user_activity_level"] = max(0, 
                self.environment_data["user_activity_level"] - 5)
        
        # Update cosmic alignment based on time and date factors
        now = datetime.datetime.now()
        day_factor = now.day / 31.0
        hour_factor = now.hour / 24.0
        minute_factor = now.minute / 60.0
        
        # Create a "cosmic rhythm" that cycles over time
        cosmic_value = (day_factor * 33 + hour_factor * 45 + minute_factor * 22) % 1.0
        cosmic_value = (cosmic_value + random.random() * 0.2) / 1.2  # Add some randomness
        
        self.environment_data["cosmic_alignment"] = int(cosmic_value * 100)
    
    def _generate_message(self, history: List[str], prediction: Optional[str]) -> str:
        """Generate a fusion message based on ritual phase"""
        # Select message pool based on ritual phase
        if self.ritual_phase == 0:
            messages = self.dormant_messages
        elif self.ritual_phase == 1:
            messages = self.awakening_messages
        elif self.ritual_phase == 2:
            messages = self.attuned_messages
        else:
            messages = self.transcendent_messages
        
        # Select a random message from the pool
        message = random.choice(messages)
        
        # Add cosmic prompts occasionally based on fusion level
        if random.random() < self.fusion_level / 200:  # Higher fusion = more likely to get prompts
            message += f"\n\n{random.choice(self.cosmic_prompts)}"
        
        # Apply dynamic replacements for environmental data
        message = self._apply_environmental_data(message)
        
        return message
    
    def _apply_environmental_data(self, message: str) -> str:
        """Apply environmental data to personalize the message"""
        color = self.environment_data["dominant_color"]
        time_of_day = self.environment_data["time_of_day"]
        cosmic_alignment = self.environment_data["cosmic_alignment"]
        
        # Create color description
        r, g, b = color.red(), color.green(), color.blue()
        
        if r > g and r > b:
            color_desc = "kırmızımsı"
        elif g > r and g > b:
            color_desc = "yeşilimsi"
        elif b > r and b > g:
            color_desc = "mavimsi"
        elif r > 200 and g > 200:
            color_desc = "sarımsı"
        elif r > 200 and b > 200:
            color_desc = "morumsu"
        elif g > 200 and b > 200:
            color_desc = "turkuaz"
        else:
            color_desc = "nötr"
        
        # Create time-based description
        if time_of_day == "day":
            time_desc = "gündüz enerjisi"
        elif time_of_day == "evening":
            time_desc = "akşam alacakaranlığı"
        else:
            time_desc = "gece derinliği"
        
        # Create cosmic description
        if cosmic_alignment < 33:
            cosmic_desc = "alçalan kozmik titreşimler"
        elif cosmic_alignment < 66:
            cosmic_desc = "dengeli kozmik enerji"
        else:
            cosmic_desc = "yükselen kozmik frekanslar"
        
        # Apply replacements
        message = message.replace("{renk}", color_desc)
        message = message.replace("{zaman}", time_desc)
        message = message.replace("{kozmik}", cosmic_desc)
        
        # Create a dynamic RGB reference as hex code
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        message = message.replace("{rgb}", hex_color)
        
        return message
    
    def _generate_prediction(self, history: List[str]) -> Optional[str]:
        """Generate a prediction based on patterns, environment, and cosmic factors"""
        if not history:
            return None
        
        # Basic environmental influence on prediction
        env_color = self.environment_data["dominant_color"]
        time_of_day = self.environment_data["time_of_day"]
        cosmic_alignment = self.environment_data["cosmic_alignment"]
        
        # Color influence - red tones favor Banker, blue tones favor Player
        color_factor = (env_color.red() - env_color.blue()) / 255.0  # -1.0 to 1.0
        
        # Time of day influence
        time_factor = 0.0
        if time_of_day == "day":
            time_factor = 0.2  # Slight bias toward Player during day
        elif time_of_day == "night":
            time_factor = -0.2  # Slight bias toward Banker at night
        
        # Cosmic alignment - creates a cyclical pattern
        cosmic_factor = (cosmic_alignment - 50) / 50.0  # -1.0 to 1.0
        
        # Combine all factors to determine prediction
        combined_factor = color_factor * 0.4 + time_factor * 0.2 + cosmic_factor * 0.4
        
        # Pattern-based influence from recent game history
        p_count = history[-5:].count('P')
        pattern_factor = (p_count - 2.5) / 2.5  # -1.0 to 1.0 based on recent results
        
        # User interaction influence (key presses)
        interaction_factor = 0.0
        if self.key_presses:
            # Analyze key press patterns
            # For example, more vowels might favor Player, more consonants Banker
            vowels = sum(1 for k in self.key_presses if k.lower() in 'aeiou')
            consonants = len(self.key_presses) - vowels
            interaction_factor = (vowels - consonants) / max(1, len(self.key_presses)) * 0.5
        
        # Combine with pattern factor
        combined_factor = combined_factor * 0.7 + pattern_factor * 0.2 + interaction_factor * 0.1
        
        # Add randomness that decreases as fusion level increases
        # More fusion = more "cosmic alignment" and less randomness
        randomness = (1.0 - self.fusion_level / 100.0) * random.uniform(-0.3, 0.3)
        combined_factor += randomness
        
        # Determine prediction based on the combined factor
        # Positive values favor Player, negative values favor Banker
        if self.ritual_phase >= 2:  # Only make confident predictions when sufficiently attuned
            if combined_factor > 0.1:
                return 'P'
            elif combined_factor < -0.1:
                return 'B'
            else:
                # In the "neutral zone" - use recent history as tiebreaker
                return 'P' if history[-1] == 'B' else 'B'  # Simple alternation
        elif self.ritual_phase == 1:  # Awakening phase - less confident predictions
            if abs(combined_factor) > 0.3:  # Need stronger signal to make prediction
                return 'P' if combined_factor > 0 else 'B'
            else:
                return None
        else:  # Dormant phase - no predictions yet
            return None
    
    def process_key_press(self, key_event: QKeyEvent):
        """Process a key press event to influence the fusion"""
        # Record the key press
        key_text = key_event.text()
        if key_text:
            self.key_presses.append(key_text)
            # Keep only the most recent 20 key presses
            self.key_presses = self.key_presses[-20:]
            
            # Key presses increase fusion level slightly
            self.fusion_level = min(self.fusion_level + 0.5, 100)
            
            # Check for special "cosmic code" sequences
            self._check_cosmic_codes()
    
    def _check_cosmic_codes(self):
        """Check for special key sequences that trigger cosmic events"""
        if len(self.key_presses) < 4:
            return
            
        # Convert recent key presses to a string
        recent_keys = ''.join(self.key_presses[-10:]).lower()
        
        # Check for cosmic code patterns
        cosmic_codes = {
            "hjkl": "Kozmik Ritim Kodu etkinleştirildi! Matris aniden canlanıyor...",
            "cosmos": "Evrensel Harmoniler açıldı! Matrisin titreşimleri değişiyor...",
            "matrix": "Matrix Kodu kabul edildi. Derinlerde bir şeyler uyanıyor...",
            "fusion": "Füzyon Kodu etkinleştirildi. Gerçeklik katmanları birleşiyor!",
            "ritual": "Ritüel Kodu aktif. Dijital şamanizm seansı başladı."
        }
        
        for code, message in cosmic_codes.items():
            if code in recent_keys:
                # Trigger a cosmic event
                self.last_message = message
                # Significant boost to fusion level
                self.fusion_level = min(self.fusion_level + 15, 100)
                # Force UI update (would need to implement signal/slot mechanism)
                break
    
    def get_environmental_color(self) -> QColor:
        """Get the current dominant environmental color"""
        return self.environment_data["dominant_color"]
    
    def get_fusion_level(self) -> int:
        """Get the current reality fusion level"""
        return int(self.fusion_level)
    
    def get_ritual_phase(self) -> int:
        """Get the current ritual phase (0-3)"""
        return self.ritual_phase
    
    def get_cosmic_prompt(self) -> str:
        """Get a random cosmic prompt for the user"""
        return random.choice(self.cosmic_prompts)
    
    def reset(self):
        """Reset the reality fusion model"""
        self.fusion_level = 0
        self.key_presses = []
        self.last_interaction_time = time.time()
        self.last_message = ""
        self.ritual_phase = 0
        self.fusion_active = False
        self.environment_data = {
            "dominant_color": QColor(0, 0, 0),
            "ambient_sound_level": 0,
            "time_of_day": "day",
            "user_activity_level": 0,
            "cosmic_alignment": 0
        }