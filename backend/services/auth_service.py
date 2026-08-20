"""
Phone Number + OTP Authentication System
Uses mock OTP for demo (in production, use Twilio/Firebase)
"""
import json
import random
import string
import os
from datetime import datetime, timedelta
import hashlib

try:
    from twilio.rest import Client # pyright: ignore[reportMissingImports]
except ImportError:
    Client = None

class OTPService:
    """Handle OTP generation and verification"""
    
    def __init__(self, otp_validity_minutes=10):
        self.otp_validity = timedelta(minutes=otp_validity_minutes)
        self.otp_store = {}  # In production, use Redis/Database
        self.db_file = '../data/users.json'
        self.otp_log_file = '../data/otp_log.json'
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from = os.getenv('TWILIO_FROM_NUMBER')
        self.twilio_client = None
        if self.twilio_sid and self.twilio_token and self.twilio_from:
            if Client is None:
                raise RuntimeError('Twilio is configured but the twilio package is not installed')
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create data directories if they don't exist"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.otp_log_file), exist_ok=True)
    
    def generate_otp(self, phone_number):
        """Generate and store OTP for a phone number"""
        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        
        # Store OTP with expiry
        self.otp_store[phone_number] = {
            'otp': otp,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + self.otp_validity).isoformat(),
            'attempts': 0,
            'verified': False
        }
        
        if self.twilio_client:
            try:
                self.twilio_client.messages.create(
                    body=f'Your AgriAI verification code is {otp}. It expires in 10 minutes.',
                    from_=self.twilio_from,
                    to=phone_number
                )
            except Exception as exc:
                self.otp_store.pop(phone_number, None)
                raise RuntimeError(f'Unable to send OTP SMS: {exc}') from exc
        else:
            # Development fallback: no SMS is sent without Twilio credentials.
            self._log_otp(phone_number, otp)
        
        result = {
            'status': 'success',
            'message': f'OTP sent to {phone_number}' if self.twilio_client else
                       'Demo OTP generated. No SMS provider is configured; check the server console.',
            'expires_in_seconds': int(self.otp_validity.total_seconds())
        }
        if not self.twilio_client:
            result['otp'] = otp
        return result
    
    def _log_otp(self, phone_number, otp):
        """Log OTP for debugging"""
        log_data = {
            'phone': phone_number,
            'otp': otp,
            'timestamp': datetime.now().isoformat()
        }
        print(f"🔐 OTP for {phone_number}: {otp}")
        
    def verify_otp(self, phone_number, otp):
        """Verify OTP for a phone number"""
        if phone_number not in self.otp_store:
            return {'status': 'error', 'message': 'OTP not found. Please request a new OTP.'}
        
        otp_data = self.otp_store[phone_number]
        
        # Check expiry
        expires_at = datetime.fromisoformat(otp_data['expires_at'])
        if datetime.now() > expires_at:
            return {'status': 'error', 'message': 'OTP has expired. Please request a new OTP.'}
        
        # Check attempts
        if otp_data['attempts'] >= 3:
            return {'status': 'error', 'message': 'Maximum OTP attempts exceeded. Please request a new OTP.'}
        
        # Verify OTP
        if otp_data['otp'] == str(otp):
            otp_data['verified'] = True
            return {'status': 'success', 'message': 'OTP verified successfully'}
        else:
            otp_data['attempts'] += 1
            remaining = 3 - otp_data['attempts']
            return {
                'status': 'error',
                'message': f'Invalid OTP. {remaining} attempts remaining.'
            }
    
    def is_verified(self, phone_number):
        """Check if OTP is verified for phone number"""
        if phone_number in self.otp_store:
            return self.otp_store[phone_number]['verified']
        return False

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

# Test the services
if __name__ == '__main__':
    print("Testing Authentication Services...")
    
    # Test OTP
    otp_service = OTPService()
    result = otp_service.generate_otp('+919876543210')
    print(f"\n1. Generate OTP: {result}")
    
    # Verify OTP
    result = otp_service.verify_otp('+919876543210', result['otp'])
    print(f"2. Verify OTP: {result}")
    
    # Test User Registration
    user_service = UserService()
    result = user_service.register_user('+919876543210', 'John Farmer', 'john@farm.com')
    print(f"3. Register User: {result}")
    
    # Verify User
    result = user_service.verify_user('+919876543210')
    print(f"4. Verify User: {result}")
    
    # Get User
    result = user_service.get_user('+919876543210')
    print(f"5. Get User: {result}")
    
    print("\n✅ All tests passed!")
