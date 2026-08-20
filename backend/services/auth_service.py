"""
Password Authentication System
"""
import json
import os
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class UserService:
    """Handle user registration and login"""
    
    def __init__(self):
        self.db_file = '../data/users.json'
        self._ensure_directories()
        self.users = self._load_users()
    
    def _ensure_directories(self):
        """Create data directories if they don't exist"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
    
    def _load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def get_user_by_email(self, email):
        email = email.strip().lower()
        for user in self.users.values():
            if user.get('email', '').lower() == email:
                return {'status': 'success', 'user': user}
        return {'status': 'error', 'message': 'User not found'}

    def register_email_user(self, name, email, password):
        email = email.strip().lower()
        existing_user = self.get_user_by_email(email)
        if existing_user['status'] == 'success':
            user = existing_user['user']
            if not user.get('password_hash'):
                user['name'] = name.strip()
                user['password_hash'] = generate_password_hash(password)
                user['verified'] = True
                self._save_users()
                return {
                    'status': 'success',
                    'message': 'Password created successfully',
                    'user': self._public_user(user)
                }
            return {'status': 'error', 'message': 'Email address already registered'}
        user = {
            'name': name.strip(),
            'email': email,
            'phone': '',
            'created_at': datetime.now().isoformat(),
            'verified': True,
            'password_hash': generate_password_hash(password)
        }
        self.users[email] = user
        self._save_users()
        return {'status': 'success', 'message': 'User registered successfully', 'user': self._public_user(user)}

    def authenticate_email_user(self, email, password):
        user_result = self.get_user_by_email(email)
        if user_result['status'] != 'success':
            return {'status': 'error', 'message': 'Invalid email or password'}
        user = user_result['user']
        if not user.get('password_hash') or not check_password_hash(user['password_hash'], password):
            return {'status': 'error', 'message': 'Invalid email or password'}
        return {'status': 'success', 'message': 'Login successful', 'user': self._public_user(user)}

    @staticmethod
    def _public_user(user):
        return {key: value for key, value in user.items() if key != 'password_hash'}
    

