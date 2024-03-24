# app.py

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email and password:
        # Save email and password to users.json
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        users.append({'email': email, 'password': password})

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)

        # Save email and mystic points to mystic_points.json
        try:
            with open('mystic_points.json', 'r') as f:
                mystic_points = json.load(f)
        except FileNotFoundError:
            mystic_points = {}

        mystic_points[email] = 0  # Initialize mystic points as 0

        with open('mystic_points.json', 'w') as f:
            json.dump(mystic_points, f, indent=2)

        return 'Registration successful'
    else:
        return 'Email and password are required', 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email and password:
        # Check if email and password match an entry in users.json
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            # If login successful, update total earnings with mystic points
            try:
                with open('mystic_points.json', 'r') as f:
                    mystic_points = json.load(f)
            except FileNotFoundError:
                mystic_points = {}

            total_earnings = mystic_points.get(email, 0)  # Get mystic points for the user

            return jsonify({'success': True, 'total_earnings': total_earnings})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    else:
        return 'Email and password are required', 400

if __name__ == '__main__':
    app.run(debug=True)
