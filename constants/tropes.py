
from typing import List

class BookTropes:
    """Predefiniowane tropy literackie"""
    # Romance tropes
    ENEMIES_TO_LOVERS = "enemies to lovers"
    FRIENDS_TO_LOVERS = "friends to lovers"
    FAKE_DATING = "fake dating"
    SECOND_CHANCE = "second chance romance"
    FORBIDDEN_LOVE = "forbidden love"
    ARRANGED_MARRIAGE = "arranged marriage"
    WORKPLACE_ROMANCE = "workplace romance"
    
    # Fantasy tropes
    CHOSEN_ONE = "chosen one"
    MAGIC_SCHOOL = "magic school"
    DARK_ACADEMIA = "dark academia"
    FAE_ROMANCE = "fae romance"
    DRAGON_RIDERS = "dragon riders"
    COURT_INTRIGUE = "court intrigue"
    
    # General tropes
    FOUND_FAMILY = "found family"
    REDEMPTION_ARC = "redemption arc"
    MORALLY_GRAY = "morally gray characters"
    SLOW_BURN = "slow burn"
    COMING_OF_AGE = "coming of age"
    UNRELIABLE_NARRATOR = "unreliable narrator"
    
    @classmethod
    def get_romance_tropes(cls) -> List[str]:
        return [cls.ENEMIES_TO_LOVERS, cls.FRIENDS_TO_LOVERS, cls.FAKE_DATING, 
                cls.SECOND_CHANCE, cls.FORBIDDEN_LOVE, cls.ARRANGED_MARRIAGE, cls.WORKPLACE_ROMANCE]
    
    @classmethod
    def get_fantasy_tropes(cls) -> List[str]:
        return [cls.CHOSEN_ONE, cls.MAGIC_SCHOOL, cls.DARK_ACADEMIA, 
                cls.FAE_ROMANCE, cls.DRAGON_RIDERS, cls.COURT_INTRIGUE]

    @classmethod
    def get_all(cls) -> List[str]:
        return [value for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, str)]