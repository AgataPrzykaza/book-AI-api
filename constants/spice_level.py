from typing import List
class BookSpiceScale:
    """Skala spice od 0 do 5 🌶️"""

    SCALE = {
        0: "No romantic/sexual content",
        1: "Sweet romance, kisses, hand-holding",
        2: "Some intimate scenes, gentle passion, fade to black",
        3: "Explicit sexual content, detailed scenes",
        4: "Very explicit, frequent sexual scenes",
        5: "Extremely explicit, multiple partners, kinky content"
    }

    @classmethod
    def get_description(cls, level: int) -> str:
        return cls.SCALE.get(level, "Unknown")

    @classmethod
    def is_valid_level(cls, level: int) -> bool:
        return level in cls.SCALE

    @classmethod
    def get_all_levels(cls) -> List[dict]:
        return [{"level": k, "description": v} for k, v in cls.SCALE.items()]
    
    @classmethod
    def get_all(cls) -> List[str]:
        """Zwraca listę opisów poziomów do join()"""
        return [f"{k}: {v}" for k, v in cls.SCALE.items()]