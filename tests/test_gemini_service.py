import pytest
from unittest.mock import Mock, patch
from services.gemini_service import GeminiService

def test_generate_content_success():
    # Arrange
    service = GeminiService()
    mock_response = Mock()
    mock_response.text = "This is a fantasy book with magic themes"
    
    # Mock the API call
    with patch.object(service.client.models, 'generate_content', return_value=mock_response):
        # Act
        result = service._generate_content("Tell me about Dune")
        
        # Assert
        assert result == "This is a fantasy book with magic themes"

def test_generate_content_failure():
    service = GeminiService()
    
    # Mock API failure
    with patch.object(service.client.models, 'generate_content', side_effect=Exception("API Error")):
        result = service._generate_content("Tell me about Dune")
        assert result is None

def test_extract_json_from_text():
    service = GeminiService()
    
    # Test data
    text = 'Some text {"genre": "fantasy", "other": "data"} more text'
    
    # Act
    result = service._extract_json_from_text(text, "genre")
    
    # Assert
    assert result == {"genre": "fantasy", "other": "data"}

def test_extract_json_not_found():
    service = GeminiService()
    text = "No JSON here"
    
    result = service._extract_json_from_text(text, "genre")
    assert result is None