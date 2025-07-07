from typing import Dict, List, Optional
from abc import ABC,abstractmethod

class BookServiceProtocol(ABC):
    @abstractmethod
    def get_book_genre(self, title: str, author: str) -> str:
        """Get precise genre for a book"""
        pass

    @abstractmethod
    def get_similar_books(self, title: str, author: str) -> List[str]:
        """Get 3 similar book recommendations"""
        pass

    
    @abstractmethod
    def get_books_for_trope(self, trope: str, count: int = 5, genre: Optional[str] = None) -> List:
        """Get book recommendations based on ttrope"""
        pass

    @abstractmethod
    def get_book_spice_level(self, title: str, author: str) -> dict: 
        """Get spice level and content warnings for a book"""
        pass

    
    @abstractmethod
    def get_book_tags(self, title: str, author: str, count: int = 10) -> List[str]:
        """Get tags for a book"""
        pass

    @abstractmethod
    def get_recommendations_from_history(self, 
                                       read_books: List,
                                       count: int = 5,
                                       preferred_genres: Optional[List[str]] = None,
                                       exclude_authors: Optional[List[str]] = None) -> List:
        """Get book recommendations based on reading history"""
        pass
    @abstractmethod
    def analyze_reading_patterns(self, read_books: List) -> List:
        """
        Analyze user's reading behavior to detect patterns, preferences, pacing, genre frequency, etc.
        Example return: {
            "favorite_genres": ["Fantasy", "Sci-Fi"],
            "spice_tolerance": "Medium",
            "frequent_tropes": ["found family", "enemies to lovers"]
        }
        """
        pass
    # @abstractmethod
    # def get_books_by_mood(
    #     self,
    #     mood: str,
    #     count: int = 5,
    #     preferred_genres: Optional[List[str]] = None,
    #     spice_level: Optional[str] = None,  # e.g., "low", "medium", "high"
    #     avoid_triggers: Optional[List[str]] = None,  # e.g., ["death", "abuse"]
    #     audience: Optional[str] = None  # e.g., "YA", "Adult", "New Adult"
    # ) -> List[dict]:
    #     """
    #     Recommend books tailored to user's current mood and detailed preferences.
        
    #     Parameters:
    #     - mood: Emotional tone (e.g., "comforting", "heartbreaking", "cozy", "dark")
    #     - count: Number of results to return
    #     - preferred_genres: Limit recommendations to specific genres
    #     - spice_level: Desired romantic/sexual content intensity
    #     - avoid_triggers: Content warnings to avoid
    #     - audience: Intended audience age group
        
    #     Returns:
    #     A list of book recommendations with metadata.
    #     """
    #     pass
