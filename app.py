from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Створення таблиці
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Створення таблиці в базі даних
with app.app_context():
    db.create_all()

# Додавання нового користувача в базу даних
with app.app_context():
    new_user = User(name="John Doe", email="john@example.com")
    db.session.add(new_user)
    db.session.commit()
    print(f'User {new_user.name} added to the database.')

# Створення маршруту для тесту
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=5001)
