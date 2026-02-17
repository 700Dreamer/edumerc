# EduShop API Usage

## Base URL
`/api/v1/shop/`

## Authentication
All cart, wishlist, and order endpoints require a JWT token:
```
Authorization: Bearer <token>
```

---

## Endpoints

### Products
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/shop/products/` | No | List all products |
| `GET` | `/shop/products/{id}/` | No | Product detail |
| `GET` | `/shop/categories/` | No | List categories |
| `GET` | `/shop/bundles/` | No | List bundles |

### Wishlist
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/shop/wishlist/` | Yes | View wishlist |
| `POST` | `/shop/wishlist/toggle_item/` | Yes | Add/remove product |

### Cart
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/shop/cart/` | Yes | View cart |
| `POST` | `/shop/cart/add_item/` | Yes | Add product to cart |

### Orders
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/shop/orders/` | Yes | List user's orders |
| `POST` | `/shop/orders/` | Yes | Checkout (create order from cart) |

---

## Usage Examples

### Toggle Wishlist
```http
POST /api/v1/shop/wishlist/toggle_item/
Content-Type: application/json
Authorization: Bearer <token>

{ "product_id": 5 }
```
**Response:**
```json
{
    "message": "Added to wishlist",
    "wishlist": {
        "id": 1,
        "products": [5],
        "products_details": [
            { "id": 5, "title": "Math Textbook P4", "price": "15000.00" }
        ]
    }
}
```
> Calling the same endpoint again with the same `product_id` will **remove** it.

---

### Add to Cart
```http
POST /api/v1/shop/cart/add_item/
Content-Type: application/json
Authorization: Bearer <token>

{ "product_id": 5, "quantity": 2 }
```
**Response:**
```json
{
    "id": 1,
    "items": [
        {
            "id": 10,
            "product": 5,
            "product_details": { "title": "Math Textbook P4", "price": "15000.00" },
            "quantity": 2
        }
    ],
    "total_items": 2
}
```
> If the product is already in the cart, the quantity is **added** to the existing amount.

---

### Checkout (Create Order)
```http
POST /api/v1/shop/orders/
Content-Type: application/json
Authorization: Bearer <token>

{}
```
**Response:**
```json
{
    "id": 1,
    "total_price": "30000.00",
    "status": "Pending",
    "items": [
        {
            "product": 5,
            "product_details": { "title": "Math Textbook P4" },
            "quantity": 2,
            "price": "15000.00"
        }
    ],
    "transaction": null,
    "transaction_details": null,
    "created_at": "2026-02-17T12:00:00Z"
}
```
> This copies all cart items into the order and **clears the cart**. No request body needed.

---

## Full Shopping Flow
```
1. Browse       →  GET  /shop/products/
2. Save for later → POST /shop/wishlist/toggle_item/   { "product_id": 5 }
3. Add to cart  →  POST /shop/cart/add_item/            { "product_id": 5, "quantity": 2 }
4. Checkout     →  POST /shop/orders/                   (creates order, clears cart)
5. Pay          →  POST /payments/initiate/              { "amount": 30000, "description": "Order #1" }
6. Redirect     →  User pays on PesaPal
7. IPN          →  PesaPal pings backend → status = COMPLETED
```
