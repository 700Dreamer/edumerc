# Frontend Guide: Google OAuth Integration

This guide outlines exactly how to implement the **Google OAuth Sign-In** flow on the frontend (React/Next.js) and connect it securely to our Django backend.

## The Architecture (How it Works)
1. **Frontend Popup**: The user clicks "Sign in with Google" on the frontend. A Google popup appears.
2. **The ID Token**: When the user approves, Google gives the frontend a short-lived string called an `id_token` (sometimes referred to as the `credential`).
3. **The Handoff**: The frontend sends this `id_token` silently to our backend via POST request.
4. **Backend Magic**: The backend verifies the token directly with Google, finds/creates the user, generates our standard internal JWT tokens, and returns them.
5. **Business as Usual**: The frontend uses these returned `access` and `refresh` tokens exactly as it does for regular username/password logins.

---

## Step-by-Step Implementation (React Example)

We highly recommend using the official `@react-oauth/google` library.

### 1. Installation
Install the official Google Identity Services library for React:
```bash
npm install @react-oauth/google
```

### 2. Wrap your Application
In your main entry file (e.g., `main.jsx`, `index.js`, or `App.jsx`), wrap the application in the `GoogleOAuthProvider`. 

**Make sure you use this exact Client ID. The backend will reject any tokens generated from a different ID.**

```jsx
import { GoogleOAuthProvider } from '@react-oauth/google';

// ... other imports

const GOOGLE_CLIENT_ID = "504245756855-t93hdnsqth9p9emg6ecqe7pesbc11qj5.apps.googleusercontent.com";

function Root() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <App />
    </GoogleOAuthProvider>
  );
}
```

### 3. Implement the Login Button
In your Login Component, utilize the `<GoogleLogin />` button provided by the library.

```jsx
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios'; // or use native fetch()

function LoginScreen() {
  
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // 1. Google gives us the ID Token
      const idToken = credentialResponse.credential; 
      
      // 2. We send it to our Django Backend endpoint
      // Adjust the URL to match your environment (e.g., prod API url)
      const response = await axios.post('/api/v1/auth/google/', {
        id_token: idToken
      });

      // 3. The backend returns our standard JWT access/refresh tokens
      const { access, refresh } = response.data;
      
      // 4. Save them exactly how you already handle normal logins!
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Update global auth state and redirect user
      console.log("Successfully logged in via Google!");
      // navigate('/dashboard');
      
    } catch (error) {
      console.error("Backend Google Auth Failed:", error.response?.data || error.message);
      // Handle the error visually for the user
    }
  };

  const handleGoogleError = () => {
    console.log('Google Sign-In popup closed or failed before completion.');
  };

  return (
    <div className="login-container">
      <h2>Log In to EduMerc</h2>
      
      {/* Renders the official Google button */}
      <div className="google-btn-wrapper">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={handleGoogleError}
          shape="rectangular"
          theme="outline" // "filled_blue" or "filled_black" are also nice
          size="large"
        />
      </div>

      {/* Or traditional login forms... */}
    </div>
  );
}

export default LoginScreen;
```

---

## Connecting to the Backend API

Here is the specification for the backend endpoint you are hitting:

### **Endpoint**
`POST /api/v1/auth/google/`

### **Request Body (JSON)**
```json
{
  "id_token": "eyJhbGciOiJSUzI1...<very_long_google_token>"
}
```

### **Success Response (200 OK)**
The response payload is identical to our standard `/api/v1/auth/login/` endpoint.
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiI...",
  "access": "eyJhbGciOiJIUzI1NiI..."
}
```

### **Error Responses (400 Bad Request)**
If the token is expired, invalid, or missing, the backend will return a 400 error.
```json
{
  "error": "id_token is required" 
}
// or
{
  "error": "Invalid token: Token used too early or expired"
}
```

## Summary Checklist for Frontend Dev
- [ ] Installed `@react-oauth/google`
- [ ] Wrapped application in `<GoogleOAuthProvider>` with the correct Client ID.
- [ ] Rendered `<GoogleLogin />` component on the authentication page.
- [ ] Added `fetch` or `axios` call inside `onSuccess` callback to `POST` the token to `/api/v1/auth/google/`.
- [ ] Parsed the returned `access` and `refresh` tokens and updated the application's auth state identically to the native login flow.
