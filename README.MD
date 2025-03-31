SecureBite 🛡️🍪
SecureBite is a secure authentication and session management system built with Django and Django REST Framework (DRF). It provides cookie-based authentication with JWT tokens.

🚀 Features
✔️ Secure Cookie-Based Authentication (using HttpOnly and Secure flags)
✔️ JWT Authentication with DRF-SimpleJWT


🛠️ Installation
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/Mbulelo-Peyi/secure_bite.git
cd SecureBite
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Rename .env.example to .env and configure:

env
Copy
Edit
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

5. Apply Migrations & Collect Static Files
bash
Copy
Edit
python manage.py migrate
python manage.py collectstatic --noinput
6. Run the Server
bash
Copy
Edit
python manage.py runserver
⚡ Authentication API Endpoints
Method	Endpoint	Description
POST	/api/auth/login/	Login & receive JWT cookies
POST	/api/auth/logout/	Logout user
GET	/api/auth/user/	Fetch authenticated user data


bash
Copy
Edit
celery -A secure_bite worker --loglevel=info
🛡️ Security Best Practices
✅ Use HTTPS in production (Cookies are Secure=True)
✅ Set SESSION_COOKIE_HTTPONLY=True to prevent XSS attacks
✅ Enable CSRF Protection with Django’s built-in middleware
✅ Store sensitive credentials in environment variables

📜 License
This project is MIT Licensed. Feel free to modify and use it as needed.

🤝 Contributing
Pull requests are welcome! Please follow the contribution guidelines and code of conduct before submitting a PR.

