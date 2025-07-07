
from typing import List, Optional
# Stałe kategorie i zakresy
class BookGenres:
    """Predefiniowane gatunki książek"""
    FANTASY = "fantasy"
    ROMANCE = "romans"
    THRILLER = "thriller"
    SCI_FI = "science fiction"
    MYSTERY = "kryminał"
    HORROR = "horror"
    HISTORICAL = "powieść historyczna"
    CONTEMPORARY = "literatura współczesna"
    LITERARY = "literatura piękna"
    YOUNG_ADULT = "young adult"
    BIOGRAPHY = "biografia"
    SELF_HELP = "rozwój osobisty"
    BUSINESS = "biznes"
    PHILOSOPHY = "filozofia"
    POETRY = "poezja"
    
    @classmethod
    def get_all(cls) -> List[str]:
        return [value for key, value in cls.__dict__.items() if not key.startswith('_') and isinstance(value, str)]