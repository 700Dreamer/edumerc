# Edumerk Complete API Endpoints Directory

This document lists every registered URL endpoint within the Edumerk backend. Use the `Authorization: Bearer <access_token>` header for all endpoints requiring authentication.

---

## 1. Authentication & User Management
**Base URL Path:** `/api/v1/auth/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `login/` | `POST` | `TokenObtainPairView` | Login with username and password to obtain JWT tokens (`access` and `refresh`). |
| `register/` | `POST` | `RegisterView` | Register a new user account. |
| `google/` | `POST` | `GoogleLoginView` | Login or register via Google OAuth. |
| `refresh/` | `POST` | `TokenRefreshView` | Refresh the JWT access token using the refresh token. |
| `profile/me/` | `GET` | `ProfileMeView` | Retrieve the authenticated user's profile details. |
| `profile/update/` | `PUT` / `PATCH` | `ProfileUpdateView` | Update the profile details of the authenticated user. |

---

## 2. EduShop (E-Commerce)
**Base URL Path:** `/api/v1/shop/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `categories/` | `GET` | `CategoryViewSet` | List all product categories. |
| `categories/` | `POST` | `CategoryViewSet` | Create a new product category (Admin). |
| `categories/{id}/` | `GET` | `CategoryViewSet` | Retrieve a specific category. |
| `categories/{id}/` | `PUT` / `PATCH` | `CategoryViewSet` | Update a category (Admin). |
| `categories/{id}/` | `DELETE` | `CategoryViewSet` | Delete a category (Admin). |
| `categories/{id}/products/` | `GET` | `CategoryViewSet` | Retrieve all products in this category. |
| `products/` | `GET` | `ProductViewSet` | List all products. Filterable by query parameter `?category=<category_id>`. |
| `products/` | `POST` | `ProductViewSet` | Create a new product (Admin). |
| `products/{id}/` | `GET` | `ProductViewSet` | Retrieve specific product details. |
| `products/{id}/` | `PUT` / `PATCH` | `ProductViewSet` | Update specific product (Admin). |
| `products/{id}/` | `DELETE` | `ProductViewSet` | Delete specific product (Admin). |
| `cart/` | `GET` | `CartViewSet` | Retrieve current authenticated user's cart. |
| `cart/add_item/` | `POST` | `CartViewSet` | Add item to cart. Request body: `{ "product_id": <int>, "quantity": <int> }`. |
| `orders/` | `GET` | `OrderViewSet` | List current user's order history. |
| `orders/` | `POST` | `OrderViewSet` | Create a new shop order from the user's current cart. |
| `orders/{id}/` | `GET` | `OrderViewSet` | Retrieve specific order details. |
| `bundles/` | `GET` | `BundleViewSet` | List product bundles (Read-Only). |
| `bundles/{id}/` | `GET` | `BundleViewSet` | Retrieve specific product bundle details (Read-Only). |
| `wishlist/` | `GET` | `WishlistViewSet` | Retrieve current user's wishlist. |
| `wishlist/toggle_item/` | `POST` | `WishlistViewSet` | Toggle a product's wishlist status. Request body: `{ "product_id": <int> }`. |

---

## 3. Payments & Wallet Ledger
**Base URL Path:** `/api/v1/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `payments/` | `GET` | `PaymentViewSet` | List all transactions belonging to the current user. |
| `payments/initiate/` | `POST` | `PaymentViewSet` | Initiate a general payment with PesaPal. Request body: `{ "amount": <decimal>, "description": <string> }`. Returns PesaPal redirect URL. |
| `payments/cart_checkout/initiate/` | `POST` | `PaymentViewSet` | Checkout the cart, generate a pending order, and initiate PesaPal payment. Returns PesaPal redirect URL and tracking details. |
| `ipn/handler/` | `GET` | `PesaPalIPNViewSet` | Instant Payment Notification webhook handler called by PesaPal. Processes transaction status changes. |
| `wallet/` | `GET` | `WalletViewSet` | Retrieve current user's wallet info (ledger balance, status). |
| `wallet/topup/` | `POST` | `WalletViewSet` | Initiate a top-up payment order for the user's wallet via PesaPal. Request body: `{ "amount": <decimal> }`. |

---

## 4. EduPedia (Schools Directory)
**Base URL Path:** `/api/v1/schools/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `schools/` | `GET` | `SchoolViewSet` | List registered schools. Filterable by query parameter `?location=<string>`. |
| `schools/` | `POST` | `SchoolViewSet` | Create a new school entry. |
| `schools/{slug}/` | `GET` | `SchoolViewSet` | Retrieve details for a school using its URL slug. |
| `schools/{slug}/` | `PUT` / `PATCH` | `SchoolViewSet` | Update details of a school by slug. |
| `schools/{slug}/` | `DELETE` | `SchoolViewSet` | Delete a school by slug. |
| `schools/{slug}/events/` | `GET` | `SchoolViewSet` | Retrieve events hosted by specific school. |
| `schools/{slug}/reviews/` | `GET` | `SchoolViewSet` | Retrieve reviews left for a school. |
| `schools/{slug}/reviews/` | `POST` | `SchoolViewSet` | Submit a review for a school. |
| `schools/events/` | `GET` | `SchoolEventViewSet` | List all school events. |
| `schools/events/` | `POST` | `SchoolEventViewSet` | Create a school event. |
| `schools/events/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `SchoolEventViewSet` | Manage specific school event. |

---

## 5. EduFundMe (Grants & Support)
**Base URL Path:** `/api/v1/fundme/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `fundme/` | `GET` | `ScholarshipViewSet` | List available scholarships (Read-Only). |
| `fundme/{id}/` | `GET` | `ScholarshipViewSet` | Get specific scholarship details (Read-Only). |
| `fundme/campaigns/` | `GET` | `CampaignViewSet` | List crowdfunding campaigns (Read-Only). |
| `fundme/campaigns/{id}/` | `GET` | `CampaignViewSet` | Get specific campaign details (Read-Only). |
| `fundme/applications/` | `GET` | `ApplicationViewSet` | List authenticated user's scholarship applications. |
| `fundme/applications/` | `POST` | `ApplicationViewSet` | Submit a new scholarship application. |
| `fundme/applications/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `ApplicationViewSet` | Manage specific scholarship application. |

---

## 6. EduQuest (Learning Materials Marketplace)
**Base URL Path:** `/api/v1/quest/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `quest/` | `GET` | `MaterialViewSet` | List curriculum materials. Filterable by query parameter `?material_type=<type>` or `?session=<session>`. |
| `quest/{id}/` | `GET` | `MaterialViewSet` | Get details of specific curriculum material. |
| `quest/orders/` | `GET` | `MaterialOrderViewSet` | List user's material order history. |
| `quest/orders/` | `POST` | `MaterialOrderViewSet` | Place a new educational materials request order. |
| `quest/orders/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `MaterialOrderViewSet` | Manage specific material order details. |
| `quest/orders/{id}/initiate-payment/` | `POST` | `MaterialOrderViewSet` | Initiate PesaPal payment for an APPROVED materials order. |

---

## 7. EduCoach (Tutors & Live Sessions)
**Base URL Path:** `/api/v1/coach/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `tutors/` | `GET` | `CoachViewSet` | List available coaches and tutors. |
| `tutors/{id}/` | `GET` | `CoachViewSet` | Get comprehensive details and availability of specific coach. |
| `tutors/earnings/` | `GET` | `CoachViewSet` | **Coach Only**: View live earnings budget, expected payouts, and withdrawal transactions. |
| `promote/` | `POST` | `PromoteCoachView` | Promote authenticated user to Coach/Tutor status. |
| `availability/` | `GET` | `CoachAvailabilityView` | **Coach Only**: View weekly schedule and hours ranges. |
| `availability/` | `PUT` | `CoachAvailabilityView` | **Coach Only**: Update active weekly hours and ranges. |
| `tutors/{id}/slots/` | `GET` | `SmartSlotView` | Generate available slots for booking. Required query parameters: `?date=YYYY-MM-DD&duration=<int_hours>`. |
| `sessions/` | `GET` | `SessionViewSet` | List relevant sessions (coach views bookings, student views classes booked). |
| `sessions/` | `POST` | `SessionViewSet` | Request booking a coaching session with a tutor. |
| `sessions/my-bookings/` | `GET` | `SessionViewSet` | **Student Only**: List sessions booked by the student. |
| `sessions/my-appointments/` | `GET` | `SessionViewSet` | **Coach Only**: List sessions scheduled with the coach. |
| `sessions/{id}/initiate-payment/` | `POST` | `SessionViewSet` | Initiate payment for a confirmed session via session internal ID. |
| `sessions/initiate-payment-by-booking/{booking_id}/` | `POST` | `SessionViewSet` | Initiate payment for a confirmed session via booking reference UID. |
| `sessions/{id}/attendance/` | `GET` | `SessionViewSet` | Retrieve live virtual class session attendance data from 100ms.live. |
| `appointments/` | `GET` | `SessionViewSet` | Alternate route for coaches to view upcoming bookings. |
| `appointments/{booking_id}/` | `PATCH` | `SessionViewSet` | **Coach Only**: Confirm, cancel or complete booking by reference ID. |
| `classes/` | `GET` | `VirtualClassViewSet` | List live virtual classes. |
| `classes/` | `POST` | `VirtualClassViewSet` | Create a live virtual class session. |
| `classes/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `VirtualClassViewSet` | Manage specific virtual class details. |
| `classes/{id}/enroll/` | `POST` | `VirtualClassViewSet` | Enroll authenticated student to virtual class session. |
| `webhooks/100ms/` | `POST` | `HMSWebhookView` | Webhook endpoint to catch live session open/close and peer join/leave events from 100ms. |

---

## 8. EduClubs (Curriculums & Subjects)
**Base URL Path:** `/api/v1/clubs/`

| Endpoint | HTTP Method | View / Serializer | Description / Request Schema |
| :--- | :---: | :--- | :--- |
| `sections/` | `GET` | `SectionViewSet` | List education system sections (e.g. Primary, Secondary) (Read-Only). |
| `sections/{id}/` | `GET` | `SectionViewSet` | Get specific section details (Read-Only). |
| `levels/` | `GET` | `LevelViewSet` | List educational levels (filters: `section`, ordering: `order`, `name`) (Read-Only). |
| `levels/{id}/` | `GET` | `LevelViewSet` | Get specific level details (Read-Only). |
| `subjects/` | `GET` / `POST` | `SubjectViewSet` | List (filters: `level`, `level__section`) or create subjects. |
| `subjects/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `SubjectViewSet` | Manage a specific subject. |
| `topics/` | `GET` / `POST` | `TopicViewSet` | List (filters: `subject`) or create learning topics. |
| `topics/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `TopicViewSet` | Manage a specific learning topic. |
| `subtopics/` | `GET` / `POST` | `SubtopicViewSet` | List (filters: `topic`) or create subtopics. |
| `subtopics/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `SubtopicViewSet` | Manage specific subtopic details. |
| `lessons/` | `GET` / `POST` | `LessonViewSet` | List (filters: `subtopic`, `is_published`) or create lessons. |
| `lessons/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `LessonViewSet` | Manage a specific lesson and view details. |
| `assessments/` | `GET` / `POST` | `AssessmentViewSet` | List (filters: `lesson`) or manage assessments. |
| `assessments/{id}/` | `GET` / `PUT` / `PATCH` / `DELETE` | `AssessmentViewSet` | Manage specific assessment details. |

---

> [!TIP]
> All endpoints expect JSON payload request formats and return JSON responses. Remember to configure your requests with `Content-Type: application/json` headers.
