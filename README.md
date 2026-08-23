# Sneakify Studio — Production Backend API

High-performance REST API backend for Sneakify 3D Sneaker Customization Studio, built with **Django 5**, **Django REST Framework (DRF)**, **PostgreSQL (Neon)**, **Cloudinary**, and **WhiteNoise**.

---

## 🛠️ Tech Stack & Architecture

- **Framework**: Django 5.x & Django REST Framework
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Database**: PostgreSQL (Hosted on **Neon**) with connection pooling via `dj-database-url`
- **Media Storage**: Cloudinary (for 3D customizer snapshots & product galleries)
- **Static Files**: WhiteNoise
- **API Documentation**: OpenAPI 3.0 & Swagger UI via `drf-spectacular`
- **Deployment**: Render Web Service

---

## 🚀 Quick Start (Local Setup)

### 1. Create and activate a virtual environment
```bash
python -m venv env
# Windows
.\env\Scripts\activate
# Linux/macOS
source env/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

### 4. Run database migrations & seed data
```bash
python manage.py migrate
python manage.py seed_catalog
```

### 5. Start development server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) to view interactive Swagger API documentation.

---

## 🌐 API Endpoints Reference

### 🔐 Authentication & Profile (`/api/v1/auth/`)
- `POST /api/v1/auth/register/` — Register new user account
- `POST /api/v1/auth/login/` — Obtain JWT access & refresh tokens
- `POST /api/v1/auth/token/refresh/` — Refresh access token
- `GET/PUT /api/v1/auth/profile/` — User profile & shipping addresses
- `POST /api/v1/auth/change-password/` — Change user password

### 👟 Sneakers Catalog (`/api/v1/sneakers/`)
- `GET /api/v1/sneakers/` — Filter catalog by category, gender, price, customizable
- `GET /api/v1/sneakers/{slug}/` — Product detail with sizes, images & reviews
- `GET /api/v1/sneakers/bestsellers/` — Trending bestsellers
- `GET /api/v1/sneakers/featured/` — Curated spotlight sneakers
- `GET /api/v1/sneakers/categories/` — Categories list

### 🎨 3D Customizer (`/api/v1/customizer/`)
- `POST /api/v1/customizer/designs/` — Save 3D design configuration and snapshot
- `GET /api/v1/customizer/designs/{id}/` — Hydrate 3D customizer canvas
- `GET /api/v1/customizer/designs/user/` — Authenticated user's custom designs
- `POST /api/v1/customizer/designs/{id}/like/` — Upvote community design
- `GET /api/v1/customizer/community/` — Public community creations feed

### 🛒 Shopping Cart (`/api/v1/cart/`)
- `GET /api/v1/cart/` — Retrieve active cart items and subtotal
- `POST /api/v1/cart/add/` — Add standard sneaker or 3D custom design to cart
- `PATCH/DELETE /api/v1/cart/items/{id}/` — Update quantity or delete item
- `POST /api/v1/cart/clear/` — Clear all items in cart

### 📦 Orders & Tracking (`/api/v1/orders/`)
- `POST /api/v1/orders/checkout/` — Convert active cart into order
- `GET /api/v1/orders/my-orders/` — User's complete order history
- `GET /api/v1/orders/{order_number}/` — Detailed order status and breakdown
- `GET /api/v1/orders/track/{tracking_id}/` — Public live tracking endpoint

### 💳 Payments (`/api/v1/payments/`)
- `POST /api/v1/payments/razorpay/create-order/` — Initialize Razorpay transaction
- `POST /api/v1/payments/razorpay/verify/` — Verify signature and advance order status

### ⭐ Reviews & Wishlist (`/api/v1/reviews/`)
- `GET/POST /api/v1/reviews/sneakers/{id}/` — Sneaker reviews
- `GET /api/v1/reviews/wishlist/` — User wishlist
- `POST /api/v1/reviews/wishlist/toggle/` — Add/remove from wishlist

---

## ☁️ Deployment on Render

1. Create a **Web Service** on [Render](https://render.com).
2. Connect your backend GitHub repository.
3. Configure the following settings:
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3`
4. Add environment variables in Render dashboard:
   - `DJANGO_ENV=production`
   - `DJANGO_SECRET_KEY=<your-secret-key>`
   - `DATABASE_URL=<your-neon-postgres-url>`
   - `CLOUDINARY_CLOUD_NAME=<your-cloud-name>`
   - `CLOUDINARY_API_KEY=<your-api-key>`
   - `CLOUDINARY_API_SECRET=<your-api-secret>`
   - `CORS_ALLOWED_ORIGINS=https://sneakify-studio.vercel.app`
