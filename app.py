from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import time

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://postgres:test@34.89.183.4:5432/pr-5-2-2?"
    "sslmode=verify-full&"
    "sslcert=client-cert.pem&"
    "sslkey=client-key.pem&"
    "sslrootcert=server-ca.pem"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Налаштування для JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Замініть на ваш секретний ключ
jwt = JWTManager(app)

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Створення таблиці
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1200), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)  # Додаємо поле для пароля

    def __repr__(self):
        return f'<User {self.name}>'

# Створення таблиці в базі даних
with app.app_context():
    db.create_all()

# Генерація випадкового рядка для тестових даних
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Маршрут для вставки тестових даних
@app.route('/insert_data', methods=['POST'])
@jwt_required()
def insert_data():
    num_users = request.json.get('num_users', 1000)  # За замовчуванням 1000 користувачів
    users = []

    start_time = time.time()

    for i in range(num_users):
        name = generate_random_string(random.randint(1, 1000))
        local_part = generate_random_string(random.randint(1, 30))
        domain = generate_random_string(random.randint(1, 50)) + ".com"
        email = f"{local_part}@{domain}"
        if len(email) > 1200:
            email = email[:1195] + "@com"
        password = generate_random_string(20)

        users.append(User(name=name, email=email, password=password))

        # Масова вставка по 10 000 записів
        if len(users) >= 10000:
            db.session.bulk_save_objects(users)
            db.session.commit()
            users = []
            print(f"{i + 1} записів додано...")

    if users:  # Додаємо залишки
        db.session.bulk_save_objects(users)
        db.session.commit()

    end_time = time.time()
    return jsonify({"msg": f"{num_users} records inserted successfully!", "time_taken": f"{end_time - start_time:.4f} seconds"}), 201

# Маршрут для оновлення даних
@app.route('/update_data', methods=['POST'])
@jwt_required()
def update_data():
    num_users = request.json.get('num_users', 1000)  # За замовчуванням 1000 користувачів

    start_time = time.time()

    for _ in range(num_users):
        user = User.query.first()
        user.name = generate_random_string(random.randint(1, 1000))
        db.session.commit()

    end_time = time.time()
    return jsonify({"msg": f"{num_users} records updated successfully!", "time_taken": f"{end_time - start_time:.4f} seconds"}), 200

# Маршрут для видалення даних
@app.route('/delete_data', methods=['POST'])
@jwt_required()
def delete_data():
    num_users = request.json.get('num_users', 1000)  # За замовчуванням 1000 користувачів

    start_time = time.time()

    for _ in range(num_users):
        user = User.query.first()
        db.session.delete(user)
        db.session.commit()

    end_time = time.time()
    return jsonify({"msg": f"{num_users} records deleted successfully!", "time_taken": f"{end_time - start_time:.4f} seconds"}), 200

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=4000)
