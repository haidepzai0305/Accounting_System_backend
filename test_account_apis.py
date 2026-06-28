import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from backend.app import create_app
from backend.models import User, db
from flask_jwt_extended import create_access_token
from datetime import timedelta

app = create_app()

def test_routes():
    with app.app_context():
        # Get or create a test user
        user = User.query.filter_by(username='admin').first()
        if not user:
            # Maybe there are no users, create one
            user = User(username='admin', email='admin@example.com', full_name='Admin', status='active')
            user.set_password('admin123')
            db.session.add(user)
            db.session.commit()
            print("Created test user: admin")
        else:
             print(f"Using existing user: {user.username}")

        # Create token
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        headers = {'Authorization': f'Bearer {token}'}
        
        client = app.test_client()
        
        print("\n--- Testing GET /api/accounts ---")
        response = client.get('/api/accounts', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.get_json()}")
        
        print("\n--- Testing GET /api/accounts/bank ---")
        response = client.get('/api/accounts/bank', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.get_json()}")
        
        print("\n--- Testing GET /api/accounts/bank/details ---")
        response = client.get('/api/accounts/bank/details', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.get_json()}")
        
        print("\n--- Testing GET /api/accounts/chart ---")
        response = client.get('/api/accounts/chart', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.get_json()}")

if __name__ == "__main__":
    test_routes()
