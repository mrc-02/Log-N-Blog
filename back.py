from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect('data.sql')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (data['username'], data['password'])).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, mobile, password) VALUES (?, ?, ?, ?)',
                     (data['username'], data['email'], data['mobile'], data['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        conn.close()
    return jsonify({'message': 'User created'}), 201

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/profile/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (data['username'], data['email'], user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Profile updated'}), 200

@app.route('/api/profile/photo/<int:user_id>', methods=['POST'])
def upload_photo(user_id):
    file = request.files['photo']
    filename = f"user_{user_id}_{file.filename}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    conn = get_db_connection()
    conn.execute('UPDATE users SET profile_photo = ? WHERE id = ?', (filename, user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Photo uploaded', 'photo': filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
