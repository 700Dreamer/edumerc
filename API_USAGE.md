# Edumerk API Documentation

Comprehensive guide for interacting with the Edumerk API modules.

## Authentication
**Base URL**: `/api/v1/auth/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `register/` | POST | Register new user |
| `login/` | POST | Get JWT tokens (access/refresh) |
| `profile/me/` | GET | Current user profile |

---

## EduPedia (Schools)
**Base URL**: `/api/v1/schools/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | List all schools |
| `{slug}/` | GET | School details |
| `{slug}/reviews/` | GET/POST | View or add school reviews |
| `events/` | GET | List all school events |

---

## EduClubs (Clubs)
**Base URL**: `/api/v1/clubs/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | List all clubs |
| `categories/` | GET | List club categories |
| `{id}/curriculum/` | GET | Nested course outline |
| `{id}/projects/` | GET | Practical applications |
| `{id}/role_models/` | GET | Professional mentors |
| `ai/assist/` | POST | Expert context AI queries |

---

## EduShop (Marketplace)
**Base URL**: `/api/v1/shop/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `products/` | GET | List available products |
| `cart/` | GET | View current shopping cart |
| `cart/add_item/` | POST | Add `{product_id, quantity}` |
| `orders/` | GET/POST | View history or checkout |
| `bundles/` | GET | Combo product packages |

---

## EduFundMe (Grants & Support)
**Base URL**: `/api/v1/fundme/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | Active grant listings |
| `applications/` | GET/POST | My grant applications |
| `campaigns/` | GET | School crowdfunding |

---

## EduQuest (Educational Materials)
**Base URL**: `/api/v1/quest/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | List available materials (Exams, Papers) |
| `{id}/` | GET | Material details |
| `orders/` | GET/POST | My material orders |

---

## EduCoach (Tutoring & Sessions)
**Base URL**: `/api/v1/coach/`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `tutors/` | GET | List available tutors |
| `tutors/{id}/slots/` | GET | Bookable time slots |
| `sessions/` | GET/POST | My bookings (Student) |
| `sessions/{id}/initiate-payment/` | POST | Get PesaPal payment link |
| `promote/` | POST | Apply to become a tutor |
| `appointments/` | GET | Tutors: view student bookings |

---

---

> [!TIP]
> Use the `Authorization: Bearer <access_token>` header for all authenticated requests.
