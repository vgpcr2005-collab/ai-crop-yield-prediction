"""
Email Verification Authentication System
Uses Gmail SMTP for verification codes
"""
import json
import random
import string
import os
from datetime import datetime, timedelta
import hashlib
import smtplib
from email.message import EmailMessage

class EmailCodeService:
    """Send passwordless verification codes through Gmail SMTP."""

    def __init__(self, validity_minutes=10):
        self.validity = timedelta(minutes=validity_minutes)
        self.codes = {}
        self.sender = os.getenv('GMAIL_ADDRESS')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD')

    def generate_code(self, email):
        email = email.strip().lower()
        code = ''.join(random.choices(string.digits, k=6))
        self.codes[email] = {
            'code': code,
            'expires_at': datetime.now() + self.validity,
            'attempts': 0,
        }

        if self.sender and self.app_password:
            message = EmailMessage()
            message['Subject'] = 'AgriAI email verification code'
            message['From'] = self.sender
            message['To'] = email
            message.set_content(f'Your AgriAI verification code is {code}. It expires in 10 minutes.')
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.sender, self.app_password)
                    smtp.send_message(message)
            except Exception as exc:
                self.codes.pop(email, None)
                raise RuntimeError(f'Unable to send verification email: {exc}') from exc
            return {'status': 'success', 'message': f'Verification code sent to {email}'}

        print(f'Email demo code for {email}: {code}')
        return {
            'status': 'success',
            'message': 'Gmail is not configured. Demo code is shown in the server console.',
            'code': code,
        }

    def verify_code(self, email, code):
        email = email.strip().lower()
        entry = self.codes.get(email)
        if not entry:
            return {'status': 'error', 'message': 'Code not found. Request a new code.'}
        if datetime.now() > entry['expires_at']:
            return {'status': 'error', 'message': 'Code expired. Request a new code.'}
        if entry['attempts'] >= 3:
            return {'status': 'error', 'message': 'Too many attempts. Request a new code.'}
        if entry['code'] != str(code):
            entry['attempts'] += 1
            return {'status': 'error', 'message': 'Invalid verification code.'}
        entry['verified'] = True
        return {'status': 'success', 'message': 'Email verified successfully'}

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
    
    def register_user(self, phone_number, name, email):
        """Register a new user"""
        # Validate phone number
        if not self._validate_phone(phone_number):
            return {'status': 'error', 'message': 'Invalid phone number format'}
        
        # Check if user already exists
        if phone_number in self.users:
            return {'status': 'error', 'message': 'Phone number already registered'}
        
        # Create user
        self.users[phone_number] = {
            'name': name,
            'email': email,
            'phone': phone_number,
            'created_at': datetime.now().isoformat(),
            'verified': False
        }
        
        self._save_users()
        
        return {
            'status': 'success',
            'message': 'User registered successfully',
            'user': self.users[phone_number]
        }
    
    def verify_user(self, phone_number):
        """Mark user as verified after OTP verification"""
        if phone_number not in self.users:
            return {'status': 'error', 'message': 'User not found'}
        
        self.users[phone_number]['verified'] = True
        self.users[phone_number]['verified_at'] = datetime.now().isoformat()
        self._save_users()
        
        return {'status': 'success', 'message': 'User verified successfully'}
    
    def get_user(self, phone_number):
        """Get user details"""
        if phone_number in self.users:
            return {'status': 'success', 'user': self.users[phone_number]}
        return {'status': 'error', 'message': 'User not found'}

    def get_user_by_email(self, email):
        email = email.strip().lower()
        for user in self.users.values():
            if user.get('email', '').lower() == email:
                return {'status': 'success', 'user': user}
        return {'status': 'error', 'message': 'User not found'}

    def register_email_user(self, name, email):
        email = email.strip().lower()
        if self.get_user_by_email(email)['status'] == 'success':
            return {'status': 'error', 'message': 'Email address already registered'}
        user = {
            'name': name.strip(),
            'email': email,
            'phone': '',
            'created_at': datetime.now().isoformat(),
            'verified': False
        }
        self.users[email] = user
        self._save_users()
        return {'status': 'success', 'message': 'User registered successfully', 'user': user}
    
    def update_user_profile(self, phone_number, **kwargs):
        """Update user profile"""
        if phone_number not in self.users:
            return {'status': 'error', 'message': 'User not found'}
        
        # Update allowed fields
        allowed_fields = ['name', 'email', 'location', 'farm_area', 'crops']
        for key, value in kwargs.items():
            if key in allowed_fields:
                self.users[phone_number][key] = value
        
        self._save_users()
        return {'status': 'success', 'user': self.users[phone_number]}
    
    def _validate_phone(self, phone_number):
        """Validate phone number format"""
        # Remove common separators
        cleaned = phone_number.replace(' ', '').replace('-', '').replace('+', '')
        # Check if it's numeric and between 10-15 digits
        return cleaned.isdigit() and 10 <= len(cleaned) <= 15

