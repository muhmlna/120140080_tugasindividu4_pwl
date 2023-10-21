import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fungsi untuk mengambil koneksi ke basis data
def get_db_connection():
    conn = sqlite3.connect('dota2.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint untuk menampilkan semua sumber daya Dota 2
@app.route('/dota2', methods=['GET'])
def get_dota2_resources():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dota2')
    dota2_resources = cursor.fetchall()
    conn.close()

    resources = []
    for resource in dota2_resources:
        resources.append({
            'id': resource['id'],
            'hero_name': resource['hero_name'],
            'role': resource['role']
        })

    return jsonify({'dota2_resources': resources})

# Endpoint untuk menambahkan sumber daya Dota 2 baru
@app.route('/dota2', methods=['POST'])
def add_dota2_resource():
    new_resource = request.get_json()
    if 'hero_name' not in new_resource or 'role' not in new_resource:
        return jsonify({'message': 'Lengkapi data sumber daya Dota 2'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dota2 (hero_name, role) VALUES (?, ?)',
                   (new_resource['hero_name'], new_resource['role']))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Sumber daya Dota 2 berhasil ditambahkan'}), 201

# Endpoint untuk menampilkan sumber daya Dota 2 berdasarkan ID
@app.route('/dota2/<int:id>', methods=['GET'])
def get_dota2_resource(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dota2 WHERE id = ?', (id,))
    resource = cursor.fetchone()
    conn.close()

    if resource is None:
        return jsonify({'message': 'Sumber daya Dota 2 tidak ditemukan'}), 404

    return jsonify({
        'id': resource['id'],
        'hero_name': resource['hero_name'],
        'role': resource['role']
    })

# Endpoint untuk memperbarui sumber daya Dota 2 berdasarkan ID
@app.route('/dota2/<int:id>', methods=['PUT'])
def update_dota2_resource(id):
    updated_resource = request.get_json()
    if 'hero_name' not in updated_resource or 'role' not in updated_resource:
        return jsonify({'message': 'Lengkapi data sumber daya Dota 2'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dota2 WHERE id = ?', (id,))
    resource = cursor.fetchone()
    
    if resource is None:
        conn.close()
        return jsonify({'message': 'Sumber daya Dota 2 tidak ditemukan'}), 404

    cursor.execute('UPDATE dota2 SET hero_name = ?, role = ? WHERE id = ?',
                   (updated_resource['hero_name'], updated_resource['role'], id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Sumber daya Dota 2 berhasil diperbarui'})

# Endpoint untuk menghapus sumber daya Dota 2 berdasarkan ID
@app.route('/dota2/<int:id>', methods=['DELETE'])
def delete_dota2_resource(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dota2 WHERE id = ?', (id,))
    resource = cursor.fetchone()

    if resource is None:
        conn.close()
        return jsonify({'message': 'Sumber daya Dota 2 tidak ditemukan'}), 404

    cursor.execute('DELETE FROM dota2 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Sumber daya Dota 2 berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)
