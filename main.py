

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.book_service import BookService
from models.book import BookRecommendation
from routes import book_bp, recommendation_bp, analysis_bp


app = Flask(__name__)
CORS(app)  


book_service = BookService()


# Buletprints registration
app.register_blueprint(book_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(analysis_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Sprawdź czy API działa"""
    return jsonify({"status": "healthy", "message": "Book API is running!"})



@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


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