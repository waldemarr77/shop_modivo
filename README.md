# Shop Modivo API 🛍️

A robust E-commerce REST API built with Django REST Framework, featuring Celery background tasks, Redis caching, Stripe integration, and Docker support.

## 🌟 Features

- **Authentication**: JWT token-based authentication (`SimpleJWT`).
- **Catalog & Inventory**: Categories, brands, products, and inventory management.
- **Cart & Orders**: Shopping cart functionality and order processing.
- **Payments**: Full Stripe integration with webhooks for automated order status updates.
- **Background Tasks (Celery)**: 
  - Asynchronous welcome emails upon registration.
  - Order confirmation emails.
  - Periodic task (`Celery Beat`) to cancel unpaid pending orders after 24 hours.
- **Caching (Redis)**: Caching for product list endpoint and tracking popular search queries.
- **Dockerized**: Easy setup and deployment with `Docker Compose`.

## 🛠️ Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Cache / Broker**: Redis
- **Task Queue**: Celery, Celery Beat
- **Payments**: Stripe API
- **Containerization**: Docker, Docker Compose

## 🚀 Local Setup (Docker)

1. Create a `.env` file in the root directory based on your environment variables:
   ```env
   # Database
   DB_NAME=shop_modivo_db
   DB_USER=modivo_user
   DB_PASSWORD=supersecret
   
   # Stripe
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   
   # Email
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. The API will be available at `http://127.0.0.1:8000/`.

## 💳 Stripe Webhooks
To test payments locally, use the Stripe CLI to forward events to your local server:
```bash
stripe listen --forward-to 127.0.0.1:8000/api/orders/webhook/stripe/
```