from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
import json
import os
from datetime import datetime
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database setup
def init_db():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            service_area TEXT NOT NULL,
            service_type TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Admin credentials (in production, use environment variables)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/admin')
def admin():
    return send_from_directory('public', 'admin.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.route('/api/quote', methods=['POST'])
def submit_quote():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'service_area', 'service_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Save to database
        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quotes (name, email, phone, service_area, service_type, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            data['service_area'],
            data['service_type'],
            data.get('message', '')
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Quote request submitted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/admin/quotes', methods=['GET'])
def get_quotes():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quotes ORDER BY created_at DESC')
    quotes = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    quote_list = []
    for quote in quotes:
        quote_list.append({
            'id': quote[0],
            'name': quote[1],
            'email': quote[2],
            'phone': quote[3],
            'service_area': quote[4],
            'service_type': quote[5],
            'message': quote[6],
            'status': quote[7],
            'created_at': quote[8]
        })
    
    return jsonify(quote_list)

@app.route('/admin/quotes/<int:quote_id>', methods=['PUT'])
def update_quote_status(quote_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE quotes SET status = ? WHERE id = ?', (status, quote_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Status updated successfully'})

if __name__ == '__main__':
    print("🚀 Starting PrimeFlow Mechanical website server...")
    print("📱 Main website: http://localhost:5000")
    print("🔧 Admin panel: http://localhost:5000/admin")
    print("👤 Admin login: admin / admin123")
    print("")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000) 