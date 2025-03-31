# SecureBite - Secure Authentication & Session Management

SecureBite is a secure authentication and session management system built with Django and Django REST Framework (DRF). It provides cookie-based authentication with JWT tokens.

## Installation

```bash
pip install rest_framework rest_framework_simplejwt rest_framework_simplejwt.token_blacklist secure_bite


from datetime import timedelta

INSTALLED_APPS = [
    'secure_bite',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'secure_bite.middleware.RefreshTokenMiddleware',
]

CSRF_COOKIE_SECURE = True  
SESSION_COOKIE_SECURE = True 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "secure_bite.authentication.CookieJWTAuthentication",
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    
    'ROTATE_REFRESH_TOKENS': True,                    
    'BLACKLIST_AFTER_ROTATION': True,                 
    'AUTH_COOKIE': 'authToken',                       
    'AUTH_COOKIE_HTTP_ONLY': True,                    
    'AUTH_COOKIE_SECURE': True,                       
    "AUTH_COOKIE_SAMESITE": "Lax"
}

Secure Cookie-Based Authentication (HttpOnly, Secure flags)

JWT Authentication with DRF-SimpleJWT

1. Clone the Repository
git clone https://github.com/Mbulelo-Peyi/secure_bite.git
cd secure_bite

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

5. Apply Migrations & Collect Static Files
python manage.py migrate
python manage.py collectstatic --noinput

6. Run the Server
python manage.py runserver

Method	Endpoint	Description
POST	/api/auth/login/	Login & receive JWT cookies
POST	/api/auth/logout/	Logout user
GET	/api/auth/user/	Fetch authenticated user data


Security Best Practices
-Use HTTPS in production (CSRF_COOKIE_SECURE=True)
-Set SESSION_COOKIE_HTTPONLY=True to prevent XSS attacks
-Enable CSRF Protection with Django’s built-in middleware
-Store sensitive credentials in environment variables

This project is MIT Licensed. Feel free to modify and use it as needed.

Pull requests are welcome! Please follow the contribution guidelines and code of conduct before submitting a PR.

