from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'rahasia'  
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

users = {}  # Simpan informasi pengguna di sini

# Endpoint untuk registrasi
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Lengkapi data registrasi'}), 400

    username = data['username']
    if username in users:
        return jsonify({'message': 'Username sudah ada'}), 400

    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    users[username] = password

    return jsonify({'message': 'Registrasi berhasil'}), 201

# Endpoint untuk login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Lengkapi data login'}), 400

    username = data['username']
    password = data['password']

    if username not in users:
        return jsonify({'message': 'Username tidak ditemukan'}), 401

    stored_password = users[username]

    if bcrypt.check_password_hash(stored_password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Password salah'}), 401

# endpoint yang memerlukan token untuk akses
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'Akses ke halaman yang dilindungi berhasil'})

if __name__ == '__main__':
    app.run(debug=True)
