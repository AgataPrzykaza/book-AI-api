# from services.book_service import BookService
# from models.book  import BookRecommendation

# def main():
#     book_service = BookService()
    
#     # Test pojedynczych funkcji
#     # genre = book_service.get_book_genre("A Court of Thorns and Roses", "Sarah J. Maas")
#     # print("Genre:", genre)
    
#     # similar = book_service.get_similar_books("A Court of Thorns and Roses", "Sarah J. Maas")
#     # print("📚 Similar books:")
#     # for book in similar:
#     #     print(f"  - {book.title} by {book.author}")
    
#     # print("📚 Similar  books for trope:")
#     # books = book_service.get_books_for_trope("enemies to lovers", 5, "Fantasy")
#     # for book in books:
#     #     print(f"  - {book.title} by {book.author}")

#     # spice = book_service.get_book_spice_level("A Court of Mist and Fury", "Sarah J. Maas")
#     # print(f"Spice level: {spice['spice_level']}")
#     # print(f"Warnings: {spice['content_warnings']}")

#     # spice = book_service.get_book_spice_level("A Court of Silver Flames", "Sarah J. Maas")
#     # print(f"Spice level: {spice['spice_level']}")
#     # print(f"Warnings: {spice['content_warnings']}")

#     reading_history = [
#         BookRecommendation(title="A Court of Thorns and Roses", author="Sarah J. Maas"),
#         BookRecommendation(title="A Court of Mist and Fury", author="Sarah J. Maas"),
#         BookRecommendation(title="A Court of Silver Flames", author="Sarah J. Maas"),
#         BookRecommendation(title="Fourth Wing", author="Rebbeca Yarros"),
#     ]

#     recomanded_books = book_service.get_recommendations_from_history(reading_history, 5,["Fantasy","Romantasy"])

#     for book in recomanded_books :
#         print(f"📚 {book.title} by {book.author}")

# if __name__ == "__main__":
#     main()

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.book_service import BookService
from models.book import BookRecommendation
import traceback

# Inicjalizacja Flask
app = Flask(__name__)
CORS(app)  # Pozwala na połączenia z frontendu

# Inicjalizacja serwisu książek
book_service = BookService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Sprawdź czy API działa"""
    return jsonify({"status": "healthy", "message": "Book API is running!"})

@app.route('/api/book/genre', methods=['POST'])
def get_book_genre():
    """Pobierz gatunek książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        genre = book_service.get_book_genre(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "genre": genre
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book/genre/<title>/<author>', methods=['GET'])
def get_book_genre_url(title, author):
    """Pobierz gatunek książki przez URL"""
    try:
        genre = book_service.get_book_genre(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "genre": genre
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book/similar', methods=['POST'])
def get_similar_books():
    """Pobierz podobne książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        similar_books = book_service.get_similar_books(title, author)
        return jsonify({
            "original_book": {"title": title, "author": author},
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in similar_books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book/similar/<title>/<author>', methods=['GET'])
def get_similar_books_url(title, author):
    """Pobierz podobne książki przez URL"""
    try:
        similar_books = book_service.get_similar_books(title, author)
        return jsonify({
            "original_book": {"title": title, "author": author},
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in similar_books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book/spice-level', methods=['POST'])
def get_spice_level():
    """Pobierz poziom pikantności książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        spice_data = book_service.get_book_spice_level(title, author)
        return jsonify({
            "title": title,
            "author": author,
            "spice_level": spice_data.get("spice_level", 0),
            "content_warnings": spice_data.get("content_warnings", [])
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book/tags', methods=['POST'])
def get_book_tags():
    """Pobierz tagi książki"""
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        count = data.get('count', 10)
        
        if not title or not author:
            return jsonify({"error": "Title and author are required"}), 400
        
        tags = book_service.get_book_tags(title, author, count)
        return jsonify({
            "title": title,
            "author": author,
            "tags": tags
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/books/by-trope', methods=['POST'])
def get_books_by_trope():
    """Pobierz książki według tropu"""
    try:
        data = request.get_json()
        trope = data.get('trope')
        count = data.get('count', 5)
        genre = data.get('genre')
        
        if not trope:
            return jsonify({"error": "Trope is required"}), 400
        
        books = book_service.get_books_for_trope(trope, count, genre)
        return jsonify({
            "trope": trope,
            "genre": genre,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/books/by-trope/<trope>', methods=['GET'])
@app.route('/api/books/by-trope/<trope>/<int:count>', methods=['GET'])
@app.route('/api/books/by-trope/<trope>/<int:count>/<genre>', methods=['GET'])
def get_books_by_trope_url(trope, count=5, genre=None):
    """Pobierz książki według tropu przez URL"""
    try:
        books = book_service.get_books_for_trope(trope, count, genre)
        return jsonify({
            "trope": trope,
            "count": count,
            "genre": genre,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in books
            ]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommendations/history', methods=['POST'])
def get_recommendations_from_history():
    """Pobierz rekomendacje na podstawie historii czytania"""
    try:
        data = request.get_json()
        read_books_data = data.get('read_books', [])
        count = data.get('count', 5)
        preferred_genres = data.get('preferred_genres')
        exclude_authors = data.get('exclude_authors')
        
        if not read_books_data:
            return jsonify({"error": "read_books list is required"}), 400
        
        # Konwertuj słowniki na obiekty BookRecommendation
        read_books = []
        for book_data in read_books_data:
            if 'title' in book_data and 'author' in book_data:
                read_books.append(BookRecommendation(book_data['title'], book_data['author']))
            else:
                return jsonify({"error": "Each book must have 'title' and 'author'"}), 400
        
        recommendations = book_service.get_recommendations_from_history(
            read_books, count, preferred_genres, exclude_authors
        )
        
        return jsonify({
            "based_on_books": [
                {"title": book.title, "author": book.author}
                for book in read_books
            ],
            "preferred_genres": preferred_genres,
            "recommendations": [
                {"title": book.title, "author": book.author}
                for book in recommendations
            ]
        })
    
    except Exception as e:
        print(f"Error in history recommendations: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Book API...")
    print("📚 Available endpoints:")
    print("  GET  /api/health")
    print("  POST /api/book/genre")
    print("  GET  /api/book/genre/<title>/<author>")
    print("  POST /api/book/similar")
    print("  GET  /api/book/similar/<title>/<author>")
    print("  POST /api/book/spice-level")
    print("  POST /api/book/tags")
    print("  POST /api/books/by-trope")
    print("  GET  /api/books/by-trope/<trope>")
    print("  GET  /api/books/by-trope/<trope>/<count>")
    print("  GET  /api/books/by-trope/<trope>/<count>/<genre>")
    print("  POST /api/recommendations/history")
    print()
    print("🌍 Example URLs to test:")
    print("  http://localhost:5000/api/book/genre/Wiedźmin/Andrzej%20Sapkowski")
    print("  http://localhost:5000/api/book/similar/Dune/Frank%20Herbert")
    print("  http://localhost:5000/api/books/by-trope/enemies-to-lovers")
    print("  http://localhost:5000/api/books/by-trope/vampire/3/Romance")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)