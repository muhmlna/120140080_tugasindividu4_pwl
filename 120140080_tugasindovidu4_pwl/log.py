from flask import Flask, request, jsonify
from flask_principal import Principal, Permission, RoleNeed, identity_loaded
from flask_logconfig import LogConfig
import logging

app = Flask(__name__)
app.secret_key = 'rahasia' 

# Konfigurasi logging
LogConfig(app)

principal = Principal(app)

# Definisikan peran
admin_role = RoleNeed('admin')
user_role = RoleNeed('user')

# Membuat izin berdasarkan peran
admin_permission = Permission(admin_role)
user_permission = Permission(user_role)

# Fungsi yang mengidentifikasi peran pengguna
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    user = identity.id
    if user.get('role') == 'admin':
        identity.provides.add(admin_role)
    else:
        identity.provides.add(user_role)

# Dummy data pengguna
users = [
    {'id': 1, 'username': 'admin', 'role': 'admin'},
    {'id': 2, 'username': 'user1', 'role': 'user'},
    {'id': 3, 'username': 'user2', 'role': 'user'},
]

# Logging untuk aktivitas login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    app.logger.info(f'Pengguna {username} melakukan login')
    # Proses autentikasi login
    return jsonify({'message': 'Login berhasil'}), 200

# Logging untuk aktivitas registrasi
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    app.logger.info(f'Pengguna {username} melakukan registrasi')
    # Proses registrasi
    return jsonify({'message': 'Registrasi berhasil'}), 201

# Middleware untuk logging aktivitas akses
@app.after_request
def log_request_info(response):
    username = request.remote_user
    if username:
        app.logger.info(f'Pengguna {username} mengakses {request.path}')
    return response

# Endpoint untuk akses yang memerlukan peran "admin"
@app.route('/admin', methods=['GET'])
@admin_permission.require(http_exception=403)
def admin_panel():
    return jsonify({'message': 'Hanya admin yang dapat mengakses panel ini.'})

# Endpoint untuk akses yang memerlukan peran "user"
@app.route('/user', methods=['GET'])
@user_permission.require(http_exception=403)
def user_dashboard():
    return jsonify({'message': 'Halo, pengguna!'})

if __name__ == '__main__':
    app.run(debug=True)
