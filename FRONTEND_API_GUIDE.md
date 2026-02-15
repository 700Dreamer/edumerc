# Frontend API Integration Guide

Welcome to the Edumerk API guide. This document provides everything you need to integrate the backend with the frontend application.

## 🚀 Getting Started
**Base URL**: `http://localhost:8000/api/v1/`
**Content-Type**: `application/json`

---

## 🔐 Users & Authentication (JWT)
We use JSON Web Tokens for security. All endpoints except Register and Login require the `Authorization` header.

### 1. Register User
`POST /auth/register/`
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "STUDENT" // Options: STUDENT, TEACHER, PARENT
}
```

### 2. Login (Get Tokens)
`POST /auth/login/`
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```
**Response**:
```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi..."
}
```

### 3. Get My Profile
`GET /auth/profile/me/`
**Response**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "role": "STUDENT",
  "profile": {
    "bio": "Excited to learn!",
    "avatar": "url_to_image"
  }
}
```

---

## 🏫 EduPedia (School Directory)
**Prefix**: `/schools/`

### List Schools
`GET /`
**Parameters**: `location` (optional)

### School Details
`GET /{slug}/`
Returns full details including images, administrators, and events.

### School Reviews
- `GET /{slug}/reviews/`: List all reviews.
- `POST /{slug}/reviews/`: Add a review (Rating 1-5).

---

## ♣️ EduClubs (Learning Clubs)
**Prefix**: `/clubs/`

### List Clubs
`GET /`

### Club Categories
`GET /categories/`

### Specific Club Content
- `GET /{id}/curriculum/`: Get the course roadmap.
- `GET /{id}/projects/`: View practical applications/projects.
- `GET /{id}/role_models/`: View mentors associated with the club.

### AI Assist
`POST /ai/assist/`
```json
{
  "query": "How do I build a simple circuit?",
  "expert_context": "Electronics Expert"
}
```

---

## 🛍️ EduShop (Marketplace)
**Prefix**: `/shop/`

### Products
`GET /products/`

### Shopping Cart
- `GET /cart/`: View your items.
- `POST /cart/add_item/`:
  ```json
  { "product_id": 1, "quantity": 1 }
  ```

### Orders
- `GET /orders/`: Order history.
- `POST /orders/`: Checkout currently active cart.

---

## 💰 EduFundMe (Financial Support)
**Prefix**: `/fundme/`

### Scholarships
`GET /`

### Scholarship Applications
`POST /applications/`
```json
{
  "scholarship": 1,
  "statement": "I am passionate about STEM...",
  "attachments": [file]
}
```

### Crowdfunding Campaigns
`GET /campaigns/`

---

## 📚 EduQuest (Materials & Exams)
**Prefix**: `/quest/`

### List Materials
`GET /`
**Parameters**: `material_type` (EXAM, PAST_PAPER), `session` (BOT, MID, EOT)

### Order Material
`POST /orders/` (Requires Auth)
```json
{
  "material": 1
}
```

---

## 💡 Frontend Integration Pro-Tips
- **Headers**: Always set `Authorization: Bearer <access_token>` after login.
- **Refresh Flow**: If a request returns `401`, call `POST /auth/refresh/` with your refresh token to get a new access token.
- **Slugs**: Use `slug` fields for URLs to improve SEO (e.g., `/schools/st-marys-academy`).
- **Media**: Image/File fields return absolute URLs.

---

> [!IMPORTANT]
> Ensure the Django server is running and the database is seeded (`python manage.py seed_data`).
