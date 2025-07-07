import json,re
from typing import Optional, List
from .gemini_service import GeminiService
from models.book import BookRecommendation
from constants.categories import BookGenres
from constants.tropes import BookTropes
from constants.spice_level import BookSpiceScale
from .book_service_protocol import BookServiceProtocol



class BookService(BookServiceProtocol):
    def __init__(self):
        self.gemini = GeminiService()
    
    def get_book_genre(self, title: str, author: str) -> str:
        """Get precise genre for a book"""
        categories_text = "\n".join(f"- {cat}" for cat in BookGenres.get_all())
        
        prompt = f"""
        Based on the book titled '{title}' by {author}, select the **single most appropriate** genre from the list below.
        Available genres:
        {categories_text}
        
        Return the result as a clean JSON in the following format:
        {{
            "genre": "..."
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return "Unknown"
            
        data = self.gemini._extract_json_from_text(response_text, "genre")
        if data and "genre" in data:
            return data["genre"]
        
        print("Could not extract genre from response:", response_text)
        return "Unknown"
    
    def get_similar_books(self, title: str, author: str) -> List[BookRecommendation]:
        """Get 3 similar book recommendations"""
        prompt = f"""
        You are a literary assistant. Based on the book titled '{title}' by {author}, 
        recommend **exactly 3 other fiction books** that are most similar in genre, themes, and style.
        Only include books that are well-known and similar in tone or target audience.
        
        Return the result as clean JSON:
        {{
            "recommendations": [
                "Title by Author",
                "Title by Author", 
                "Title by Author"
            ]
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return []
            
        data = self.gemini._extract_json_from_text(response_text, "recommendations")
        if data and "recommendations" in data:
            return [BookRecommendation.from_string(book) for book in data["recommendations"]]
        
        print("Could not extract recommendations from response:", response_text)
        return []
    
    
    def get_books_for_trope(self, trope: str, count: int = 5, genre: Optional[str] = None) -> List[BookRecommendation]:
        """Get book recommendations based on a specific trope"""
        recommendations_list = ",\n                ".join(['"Title by Author"'] * count)
        
        genre_constraint = f" within the {genre} genre" if genre else ""
        
        prompt = f"""
        You are a literary assistant. Recommend **exactly {count} fiction books**{genre_constraint} that prominently feature the trope: "{trope}".
        Only include well-known books that clearly showcase this trope.
        
        Return the result as clean JSON:
        {{
            "recommendations": [
                {recommendations_list}
            ]
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return []
            
        data = self.gemini._extract_json_from_text(response_text, "recommendations")
        if data and "recommendations" in data:
            return [BookRecommendation.from_string(book) for book in data["recommendations"]]
        
        print("Could not extract trope recommendations from response:", response_text)
        return []

    def get_book_spice_level(self, title: str, author: str) -> dict:
        """Get spice/steam level for a book on 1-6 pepper scale"""
        prompt = f"""
        You are a literary assistant. Based on the book titled '{title}' by {author}, 
        rate the spice level on a scale of 1-6 peppers 🌶️:
        
        0 🌶️ - No romantic/sexual content
        1 🌶️ - Sweet romance, kisses, hand-holding
        2 🌶️ - Some intimate scenes, gentle passion, fade to black
        3 🌶️ - Explicit sexual content, detailed scenes
        4 🌶️ - Very explicit, frequent sexual scenes
        5 🌶️ - Extremely explicit, multiple partners, kinky content
        
        Return the result as clean JSON:
        {{
            "spice_level": 3,
            "content_warnings": ["warning1", "warning2"]
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return {"spice_level": 0, "content_warnings": []}
            
        # Try to extract complete dict
        pattern = r'\{.*?"spice_level"\s*:\s*\d+.*?\}'
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        
        print("Could not extract spice level from response:", response_text)
        return {"spice_level": 0, "content_warnings": []}


    def get_book_tags(self, title: str, author: str, count: int = 10) -> List[str]:
        """Get tags/tropes for a specific book"""
        prompt = f"""
        You are a literary assistant. Based on the book titled '{title}' by {author}, 
        identify **exactly {count} most prominent tags/tropes** that describe this book.
        Include themes, tropes, content warnings, and notable elements.
        
        Return the result as clean JSON:
        {{
            "tags": [
                "tag1",
                "tag2",
                "tag3"
            ]
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return []
            
        data = self.gemini._extract_json_from_text(response_text, "tags")
        if data and "tags" in data:
            return data["tags"]
        
        print("Could not extract tags from response:", response_text)
        return []
    
    def get_recommendations_from_history(self,
                                   read_books: List,
                                   count: int = 5,
                                   preferred_genres: Optional[List[str]] = None,
                                   exclude_authors: Optional[List[str]] = None) -> List[BookRecommendation]:
        """Get book recommendations based on reading history"""
        
        
        books_summary = "\n".join([
            f"- '{book.title}' by {book.author}"
            for book in read_books
        ])
        
       
        genre_constraint = ""
        if preferred_genres:
            genre_constraint = f"\nFocus on these genres: {', '.join(preferred_genres)}"
        
        
        exclude_constraint = ""
        if exclude_authors:
            exclude_constraint = f"\nExclude books by: {', '.join(exclude_authors)}"
        
       
        recommendations_list = ",\n                ".join(['"Title by Author"'] * count)
        
        prompt = f"""
        You are a literary assistant. Based on the user's reading history, recommend **exactly {count} fiction books** 
        that match their taste and reading patterns.
        
        Books they've read and enjoyed:
        {books_summary}
        {genre_constraint}
        {exclude_constraint}
        
        Analyze their reading patterns and recommend books with similar themes, writing styles, or genres.
        Only include well-known books that are likely to appeal to someone with this reading history.
        
        Return the result as clean JSON:
        {{
            "recommendations": [
                {recommendations_list}
            ]
        }}
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return []
            
        data = self.gemini._extract_json_from_text(response_text, "recommendations")
        if data and "recommendations" in data:
            return [BookRecommendation.from_string(book) for book in data["recommendations"]]
        
        print("Could not extract history-based recommendations from response:", response_text)
        return []
    
    
    
    
    def analyze_reading_patterns(self, read_books: List) -> dict:
        genres = BookGenres.get_all()
        spice_levels = BookSpiceScale.get_all()
        tropes = BookTropes.get_all()
       
        books_summary = "\n".join([
            f"- '{book.title}' by {book.author}"
            for book in read_books
        ])

        prompt = f"""
        You are a literary assistant. Based on the user's reading history, analyze their reading patterns and preferences.

        Books they've read and enjoyed:
        {books_summary}

        Identify their TOP 3 favorite genres, TOP 3 most frequent tropes, and spice tolerance.

        IMPORTANT: Only return the MOST COMMON patterns, not everything you find.

        - Available Genres: {', '.join(genres)}
        - Available Tropes: {', '.join(tropes)}  
        - Spice levels: {', '.join(spice_levels)}

        Return EXACTLY this JSON format:
        {{
            "favorite_genres": ["top_genre_1", "top_genre_2", "top_genre_3"],
            "frequent_tropes": ["top_trope_1", "top_trope_2", "top_trope_3"],
            "spice_tolerance": "most_common_level",
        }}

        Return MAXIMUM 3 items in each array.
        """
        
        response_text = self.gemini._generate_content(prompt)
        if not response_text:
            return {
            "favorite_genres": [],
            "frequent_tropes": [],
            "spice_tolerance": "unknown",
            "average_book_length": 0
        }
            
        result = self.gemini._extract_json_from_text(response_text, "favorite_genres")
  
        if isinstance(result, dict):
            return result
        
        # Fallback
        return {
            "favorite_genres": [],
            "frequent_tropes": [],
            "spice_tolerance": "unknown",
           
        }