import pytest
from unittest.mock import Mock, patch
from services.book_service import BookService
from models.book import BookRecommendation

class TestBookService:
    
    @pytest.fixture
    def book_service(self):
        return BookService()
    
    @pytest.fixture
    def mock_gemini_response(self):
        def _mock_response(json_data):
            mock = Mock()
            mock._generate_content.return_value = f'Some text {json_data} more text'
            mock._extract_json_from_text.return_value = json_data
            return mock
        return _mock_response
    
    def test_get_book_genre_success(self, book_service, mock_gemini_response):
        # Arrange
        expected_genre = "Science Fiction"
        book_service.gemini = mock_gemini_response({"genre": expected_genre})
        
        # Act
        result = book_service.get_book_genre("Dune", "Frank Herbert")
        
        # Assert
        assert result == expected_genre

    def test_get_book_genre_no_response(self, book_service):
        # Arrange
        book_service.gemini._generate_content = Mock(return_value=None)
        
        # Act
        result = book_service.get_book_genre("Unknown Book", "Unknown Author")
        
        # Assert
        assert result == "Unknown"


    def test_get_similar_books_success(self, book_service, mock_gemini_response):
        # Arrange
        recommendations_data = {
            "recommendations": [
                "Foundation by Isaac Asimov",
                "Hyperion by Dan Simmons",
                "Ender's Game by Orson Scott Card"
            ]
        }
        book_service.gemini = mock_gemini_response(recommendations_data)
        
        # Act
        result = book_service.get_similar_books("Dune", "Frank Herbert")
        
        # Assert
        assert len(result) == 3
        assert all(isinstance(book, BookRecommendation) for book in result)

    def test_get_books_for_trope_with_genre(self, book_service, mock_gemini_response):
        # Arrange
        recommendations_data = {
            "recommendations": [
                "Pride and Prejudice by Jane Austen",
                "You've Got Mail by Nora Ephron"
            ]
        }
        book_service.gemini = mock_gemini_response(recommendations_data)
        
        # Act
        result = book_service.get_books_for_trope("enemies-to-lovers", count=2, genre="Romance")
        
        # Assert
        assert len(result) == 2
        book_service.gemini._generate_content.assert_called_once()

    def test_get_book_spice_level_success(self, book_service):
        # Arrange
        response_text = '{"spice_level": 3, "content_warnings": ["explicit content"]}'
        book_service.gemini._generate_content = Mock(return_value=response_text)
        
        # Act
        result = book_service.get_book_spice_level("Fifty Shades", "E.L. James")
        
        # Assert
        assert result["spice_level"] == 3
        assert "explicit content" in result["content_warnings"]

    def test_get_book_tags_success(self, book_service, mock_gemini_response):
        # Arrange
        tags_data = {"tags": ["space opera", "chosen one", "political intrigue"]}
        book_service.gemini = mock_gemini_response(tags_data)
        
        # Act
        result = book_service.get_book_tags("Dune", "Frank Herbert", count=3)
        
        # Assert
        assert len(result) == 3
        assert "space opera" in result

    def test_get_recommendations_from_history(self, book_service, mock_gemini_response):
        # Arrange
        read_books = [BookRecommendation("Dune", "Frank Herbert")]
        recommendations_data = {
            "recommendations": ["Foundation by Isaac Asimov"]
        }
        book_service.gemini = mock_gemini_response(recommendations_data)
        
        # Act
        result = book_service.get_recommendations_from_history(
            read_books, count=1, preferred_genres=["Science Fiction"]
        )
        
        # Assert
        assert len(result) == 1
        assert result[0].title == "Foundation"

    def test_analyze_reading_patterns(self, book_service, mock_gemini_response):
        # Arrange
        read_books = [BookRecommendation("Dune", "Frank Herbert")]
        patterns_data = {
            "favorite_genres": ["Science Fiction"],
            "frequent_tropes": ["chosen one"],
            "spice_tolerance": "mild"
        }
        book_service.gemini = mock_gemini_response(patterns_data)
        
        # Act
        result = book_service.analyze_reading_patterns(read_books)
        
        # Assert
        assert result["favorite_genres"] == ["Science Fiction"]
        assert result["frequent_tropes"] == ["chosen one"]

    def test_get_books_by_mood_simple(self, book_service, mock_gemini_response):
        # Arrange
        recommendations_data = {
            "recommendations": ["The Hobbit by J.R.R. Tolkien"]
        }
        book_service.gemini = mock_gemini_response(recommendations_data)
        
        # Act
        result = book_service.get_books_by_mood("happy", count=1)
        
        # Assert
        assert len(result) == 1
        assert result[0].title == "The Hobbit"