# Authentication and User Profile API Usage

This document outlines the usage of the authentication and profile API endpoints.

## 1. Authentication Endpoints

### **Register a New User**
- **URL**: `/auth/register/`
- **Method**: `POST`
- **Body** (JSON):
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "STUDENT"
}
```
*Note: Roles can be `STUDENT`, `TEACHER`, `PARENT`, or `ADMIN`.*

### **Login (Get JWT Tokens)**
- **URL**: `/auth/login/`
- **Method**: `POST`
- **Body** (JSON):
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```
- **Response**: Returns `access` and `refresh` tokens.

### **Refresh Token**
- **URL**: `/auth/refresh/`
- **Method**: `POST`
- **Body**: `{"refresh": "YOUR_REFRESH_TOKEN"}`

---

## 2. User Profile Endpoints
*Note: All profile endpoints require the `Authorization: Bearer <access_token>` header.*

### **Get My Profile**
- **URL**: `/profile/me/`
- **Method**: `GET`
- **Response**: Returns current user details and their profile data.

### **Update Profile**
- **URL**: `/profile/update/`
- **Method**: `PATCH`
- **Body** (JSON - all fields optional):
```json
{
  "bio": "New bio text",
  "preferences": {
     "theme": "dark",
     "notifications": true
  }
}
```

---

## 3. Testing
A verification script is available at `verify_auth.py`. 

### Running tests:
1. Start the server:
   ```bash
   python manage.py runserver
   ```
2. Run the script:
   ```bash
   python verify_auth.py
   ```
