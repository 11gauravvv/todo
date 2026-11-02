from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    # Using timezone-aware UTC datetime (recommended in modern Python)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route Handler
@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    # Create database tables automatically if they don't exist yet
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)