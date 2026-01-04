# 🍽️ Django Restaurant Ordering System

👨‍💻 Author

Satya Sundar Malik

🔗 **Live Website:**  
https://thesundar.pythonanywhere.com/


A full-stack **Django-based food ordering web application** with cart, offers, checkout, order confirmation, email notifications, and deployment-ready setup.

---

## 🚀 Features

- User authentication (Login / Logout)
- Food menu with categories
- Add to cart (AJAX based)
- Offer-based discounts
- Cart popup with:
  - Item list
  - Quantity
  - Remove button
  - Go to cart page
- Full cart page with grand total
- Checkout & order placement
- Order success popup (SweetAlert)
- Thank You page
- Email notification on successful order
- Admin panel to manage items & orders

---

## 🧠 Project Workflow

1. User selects food from menu
2. Clicks **Add to Cart**
3. Cart popup opens showing items & total
4. User clicks **Go to Cart**
5. Reviews cart & clicks **Proceed to Checkout**
6. Places order
7. Receives confirmation popup & email
8. Cart is cleared automatically

---

## 🛠️ Tech Stack

- **Backend:** Django 5
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (can be switched to PostgreSQL)
- **AJAX:** Fetch API
- **Email:** SMTP (Gmail)
- **Deployment:** PythonAnywhere

---

## 📂 Project Structure

restaurant_project/
│
├── base_app/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│
├── templates/
│ ├── base.html
│ ├── home.html
│ ├── cart.html
│ ├── checkout.html
│ ├── order_success.html
│ ├── thank_you.html
│
├── static/
├── manage.py
└── requirements.txt


---

## ⚙️ Installation (Local Setup)


git clone https://github.com/USERNAME/restaurant-ordering-system.git
cd restaurant-ordering-system
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

📧 Email Configuration

In settings.py:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_app_password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


Use Gmail App Password, not real password.

🌐 Deployment on PythonAnywhere
🔹 Step 1: Create account

👉 https://www.pythonanywhere.com

🔹 Step 2: Upload project

Upload ZIP or

Clone GitHub repo in PythonAnywhere console:

git clone https://github.com/USERNAME/restaurant-ordering-system.git

🔹 Step 3: Create virtualenv
mkvirtualenv restaurantenv --python=python3.10
pip install -r requirements.txt

🔹 Step 4: Configure WSGI

Edit wsgi.py:

import os
import sys

path = '/home/USERNAME/restaurant-ordering-system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_name.settings'

🔹 Step 5: Static files
python manage.py collectstatic


Set:

Static files path

Media files path

🔹 Step 6: Reload web app

🎉 Your site is LIVE!

🏆 Benefits of This Project

Real-world ecommerce workflow

AJAX-based cart system

Clean Django architecture

Resume-ready project

Deployment experience

Strong backend logic

📌 Future Improvements

Online payments (Razorpay / Stripe)

Order tracking

User order history

Ratings & reviews

Invoice PDF

👨‍💻 Author

Satya Malik
 Python Developer
