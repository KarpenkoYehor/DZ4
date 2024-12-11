from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token



app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Налаштування для JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Замініть на ваш секретний ключ
jwt = JWTManager(app)

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Створення таблиці
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Додаємо поле для пароля

    def __repr__(self):
        return f'<User {self.name}>'

# Створення таблиці в базі даних
with app.app_context():
    db.create_all()

# Створення маршруту для тесту
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Маршрут для входу (Login) - генерує JWT токен
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Знайти користувача в базі даних
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:  # Тут ми перевіряємо пароль (на практиці краще використовувати хешування)
        # Генерація токена
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# Маршрут для виходу (Logout) - просто повідомляємо, що вихід успішний
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logout successful"}), 200


# Захищений маршрут (при використанні JWT токена)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="This is a protected route.")

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=5001)
