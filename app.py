from datetime import datetime, timezone
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Model
class Todo(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  date_created = db.Column(
      db.DateTime, default=lambda: datetime.now(timezone.utc)
  )

  def __repr__(self) -> str:
    return f'{self.sno} - {self.title}'


# Route Handler: Home (Create & Read)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
  if request.method == 'POST':
    title = request.form.get('title', '').strip()
    desc = request.form.get('desc', '').strip()

    if title and desc:
      todo = Todo(title=title, desc=desc)
      db.session.add(todo)
      db.session.commit()
      return redirect('/')

  allTodo = Todo.query.all()
  return render_template('index.html', allTodo=allTodo)


# Route Handler: Delete
@app.route('/delete/<int:sno>')
def delete(sno):
  todo = Todo.query.filter_by(sno=sno).first()
  if todo:
    db.session.delete(todo)
    db.session.commit()
  return redirect('/')


# Route Handler: Update (Edit Form & Submit)
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  todo = Todo.query.filter_by(sno=sno).first()

  if request.method == 'POST':
    title = request.form.get('title', '').strip()
    desc = request.form.get('desc', '').strip()

    if todo and title and desc:
      todo.title = title
      todo.desc = desc
      db.session.commit()
      return redirect('/')

  return render_template('update.html', todo=todo)


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True)