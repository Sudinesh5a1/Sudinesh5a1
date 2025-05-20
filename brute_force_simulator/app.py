from flask import Flask, request, jsonify
import json
from time import time

app = Flask(__name__)

with open('users.json', 'r') as f:
    users = json.load(f)

login_attempts = {}

@app.route('/login', methods=['POST'])
def login():
    ip = request.remote_addr
    now = time()

    if ip not in login_attempts:
        login_attempts[ip] = []

    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < 60]

    if len(login_attempts[ip]) >= 5:
        return jsonify({'status': 'fail', 'message': 'Too many attempts'}), 429

    login_attempts[ip].append(now)

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
