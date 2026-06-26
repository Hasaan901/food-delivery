# 🛍️ Food Delivery — Django Web Application

A full-stack food delivery management system built with Django. Supports three user roles (Customer, Driver, Admin) with real-time order tracking and automatic Gmail confirmation emails on every order.

![Django](https://img.shields.io/badge/Django-6.0.6-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🚀 Features

| Feature | Description |
|---|---|
| 👤 **3 User Roles** | Customer, Driver, Admin — each with their own dashboard |
| 📦 **Order Management** | Place, track, assign and update delivery orders |
| 📧 **Email Confirmation** | Styled HTML email sent to customer Gmail on every order |
| 🍕 **Restaurant Catalog** | Browse restaurants and food items by category |
| 🚗 **Auto Driver Assignment** | Random available driver assigned on order creation |
| 🔐 **Secure Auth** | Login, Register, Logout with role-based access control |
| ⚙️ **Admin Panel** | Full CRUD for users and orders |

---

## 📸 Screenshots

### Customer Dashboard
> Browse restaurants, place orders, track status in real time

### Admin Dashboard
> Manage all orders, users, and driver assignments

### Driver Dashboard
> View assigned orders, update pickup and delivery status

---

## 🛠️ Tech Stack

- **Backend:** Django 6.0.6 (Python 3.14)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Email:** Gmail SMTP via Django's `EmailMultiAlternatives`
- **Auth:** Django built-in auth with custom `AbstractUser`
- **Config:** `python-decouple` for environment variables

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Hasaan901/food-delivery.git
cd food-delivery
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your values:
```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
```

> **Getting a Gmail App Password:**
> Google Account → Security → 2-Step Verification → App Passwords → Generate

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Visit → **http://127.0.0.1:8000/**

---

## 👥 User Roles & Access

| Role | Default Redirect | Capabilities |
|---|---|---|
| **Customer** | `/customer/dashboard/` | Browse restaurants, place orders, view history |
| **Driver** | `/driver/dashboard/` | View assigned orders, update status (Picked Up / Delivered) |
| **Admin** | `/admin-ops/dashboard/` | Full CRUD on users and orders, assign drivers |

---

## 📁 Project Structure

```
food-delivery/
├── delivery_project/        # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/                 # Main Django app
│   ├── models.py            # CustomUser, Order, Restaurant, FoodItem
│   ├── views.py             # All views + email confirmation logic
│   ├── urls.py              # URL patterns
│   ├── templates/tracker/   # HTML templates
│   └── static/tracker/      # Images & static assets
├── .env.example             # Environment variable template
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 📧 Email Confirmation Setup

When a customer places an order, a styled HTML confirmation email is automatically sent to their registered Gmail, including:
- Order ID, items, delivery address
- Total price and current status
- Assigned rider name

Powered by Django's `EmailMultiAlternatives` + Gmail SMTP.

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `EMAIL_HOST_USER` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail App Password (16 chars) |

Never commit your `.env` file — it is listed in `.gitignore`.

---

## 📦 Dependencies

```
Django==6.0.6
python-decouple==3.8
certifi==2026.6.17
asgiref==3.11.1
sqlparse==0.5.5
django-stubs==6.0.6
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Hasaan Ahmad**
- GitHub: [@Hasaan901](https://github.com/Hasaan901)
- Email: hasaanahmad021@gmail.com
