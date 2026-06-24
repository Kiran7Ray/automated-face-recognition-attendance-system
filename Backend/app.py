from flask import Flask
from routes.student import student_bp
from routes.attendance import attendance_bp
from routes.embedding import embedding_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(student_bp, url_prefix="/students")
app.register_blueprint(attendance_bp, url_prefix="/attendance")
app.register_blueprint(embedding_bp, url_prefix="/embedding")

if __name__ == "__main__":
    app.run(debug=True)