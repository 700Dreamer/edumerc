# EduQuest Order — API Endpoint Structure (Synced with Backend)

> **Last synced:** 2026-02-22  
> **Backend Repo:** [700Dreamer/edumerc](https://github.com/700Dreamer/edumerc)  
> **Base URL:** `https://edumerc.up.railway.app/api/v1/`  
> **Django App:** `eduquest/`  
> **URL Prefix:** `api/v1/quest/` ✅ (already registered in `config/urls.py`)

---

## Current Backend State (Actual)

The `eduquest` app currently has:

| File             | Status        | Notes                                                 |
| ---------------- | ------------- | ----------------------------------------------------- |
| `models.py`      | ✅ Exists     | `Material` + `MaterialOrder` models                   |
| `serializers.py` | ✅ Exists     | `MaterialSerializer` + `MaterialOrderSerializer`      |
| `views.py`       | ✅ Exists     | `MaterialViewSet` (ReadOnly) + `MaterialOrderViewSet` |
| `urls.py`        | ✅ Exists     | Registers `orders/` and `''` routes                   |
| `config/urls.py` | ✅ Registered | `path('api/v1/quest/', include('eduquest.urls'))`     |

### Current `MaterialOrder` Model

```python
class MaterialOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_orders')
    material  = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='orders')
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ordered_at = models.DateTimeField(auto_now_add=True)
```

### Current `MaterialOrderSerializer`

```python
class MaterialOrderSerializer(serializers.ModelSerializer):
    material_title = serializers.CharField(source='material.title', read_only=True)
    username       = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MaterialOrder
        fields = ['id', 'user', 'username', 'material', 'material_title', 'status', 'ordered_at']
        read_only_fields = ['user', 'status']
```

### Current Endpoints Available

| Method | Endpoint                                       | Description         |
| ------ | ---------------------------------------------- | ------------------- |
| `GET`  | `api/v1/quest/`                                | List all materials  |
| `GET`  | `api/v1/quest/{id}/`                           | Get material detail |
| `GET`  | `api/v1/quest/?session=BOT&material_type=EXAM` | Filter materials    |
| `POST` | `api/v1/quest/orders/`                         | Create a new order  |
| `GET`  | `api/v1/quest/orders/`                         | List user's orders  |

---

## Gap Analysis: What Needs Changing

The current `MaterialOrder` model **only stores a link to a Material** — it doesn't capture:

- ❌ School name / representative / contact details
- ❌ Delivery address and date
- ❌ Selected levels and subjects per level
- ❌ Custom quantities
- ❌ Total sets count
- ❌ Estimated amount / pricing

---

## 🔧 What to Add to the Backend

### Option A — Minimal (Recommended First): Add Extra Fields to `MaterialOrder`

Extend `MaterialOrder` with the school/delivery details and store levels as JSON.  
**No new model needed**, just a migration.

#### Updated `models.py`

```python
# eduquest/models.py
from django.db import models
from django.conf import settings
import uuid

def generate_quest_reference():
    return f"EQ-{uuid.uuid4().hex[:8].upper()}"

class Material(models.Model):
    # ... (unchanged — keep as is)
    MATERIAL_TYPE_CHOICES = (
        ('EXAM', 'Sessional Exam'),
        ('PAST_PAPER', 'Past Paper'),
        ('OTHER', 'Other Material'),
    )
    SESSION_CHOICES = (
        ('BOT', 'Beginning of Term'),
        ('MID', 'Mid Term'),
        ('EOT', 'End of Term'),
        ('NONE', 'None'),
    )
    title         = models.CharField(max_length=255)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES, default='OTHER')
    session       = models.CharField(max_length=10, choices=SESSION_CHOICES, default='NONE')
    description   = models.TextField(blank=True)
    file          = models.FileField(upload_to='materials/', blank=True, null=True)
    price         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.material_type})"


class MaterialOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING',   'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    SESSION_CHOICES = (
        ('BOT', 'Beginning of Term'),
        ('MID', 'Mid Term'),
        ('EOT', 'End of Term'),
    )

    # Core (existing)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_orders')
    material   = models.ForeignKey(Material, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ordered_at = models.DateTimeField(auto_now_add=True)

    # NEW: Order reference
    reference  = models.CharField(max_length=20, unique=True, default=generate_quest_reference)

    # NEW: Session type (BOT/MID/EOT)
    session    = models.CharField(max_length=10, choices=SESSION_CHOICES, blank=True)

    # NEW: School / delivery details
    school_name    = models.CharField(max_length=200, blank=True)
    representative = models.CharField(max_length=200, blank=True)
    location       = models.CharField(max_length=200, blank=True)
    address        = models.CharField(max_length=300, blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    delivery_date  = models.DateField(null=True, blank=True)

    # NEW: Flexible levels + subjects snapshot
    levels_data      = models.JSONField(default=list, blank=True)
    total_sets       = models.PositiveIntegerField(default=0)
    estimated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.reference} — {self.school_name} ({self.status})"
```

#### Updated `serializers.py`

```python
# eduquest/serializers.py
from rest_framework import serializers
from .models import Material, MaterialOrder

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialOrderSerializer(serializers.ModelSerializer):
    material_title = serializers.CharField(source='material.title', read_only=True)
    username       = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MaterialOrder
        fields = [
            'id', 'reference', 'username', 'user',
            'material', 'material_title',
            'session',
            'school_name', 'representative', 'location',
            'address', 'phone', 'email', 'delivery_date',
            'levels_data', 'total_sets', 'estimated_amount',
            'status', 'ordered_at'
        ]
        read_only_fields = ['user', 'status', 'reference', 'ordered_at']
```

#### Updated `views.py`

```python
# eduquest/views.py
from rest_framework import viewsets, permissions
from .models import Material, MaterialOrder
from .serializers import MaterialSerializer, MaterialOrderSerializer

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filterset_fields = ['material_type', 'session']


class MaterialOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialOrderSerializer

    def get_queryset(self):
        return MaterialOrder.objects.filter(user=self.request.user).order_by('-ordered_at')

    def perform_create(self, serializer):
        data = self.request.data
        school = data.get('school', {})

        serializer.save(
            user=self.request.user,
            session=data.get('session', ''),
            school_name=school.get('name', ''),
            representative=school.get('representative', ''),
            location=school.get('location', ''),
            address=school.get('address', ''),
            phone=school.get('phone', ''),
            email=school.get('email', ''),
            delivery_date=school.get('delivery_date') or None,
            levels_data=data.get('levels', []),
            total_sets=data.get('total_sets', 0),
            estimated_amount=data.get('estimated_amount', 0),
            material_id=data.get('material'),
        )
```

> **Note:** `urls.py` does **not** need changing — the router already registers `orders/` correctly.

---

## Frontend — Request Payload (POST `api/v1/quest/orders/`)

```json
{
  "session": "BOT",
  "material": 12,
  "school": {
    "name": "Kampala Parents School",
    "representative": "Jane Nakato",
    "location": "Kampala",
    "address": "Plot 45, Kololo Hill",
    "phone": "0781234567",
    "email": "principal@kps.ac.ug",
    "delivery_date": "2026-03-15"
  },
  "levels": [
    {
      "level": "P.6",
      "subjects": [
        { "name": "Mathematics", "quantity": 75 },
        { "name": "English", "quantity": 75 }
      ]
    },
    {
      "level": "P.7",
      "subjects": [
        { "name": "Mathematics", "quantity": 100 },
        { "name": "Science", "quantity": 100 }
      ]
    }
  ],
  "total_sets": 350,
  "estimated_amount": 700000
}
```

---

## Frontend — Update `src/api/index.js`

```js
export const questApi = {
  getMaterials: (params = {}) => {
    let query = new URLSearchParams(params).toString();
    return apiRequest(`quest/${query ? `?${query}` : ""}`);
  },
  getMaterialDetail: (id) => apiRequest(`quest/${id}/`),
  getOrders: () => apiRequest("quest/orders/"),

  // Updated to send full wizard payload
  placeOrder: (orderData) => apiRequest("quest/orders/", "POST", orderData),
};
```

---

## Frontend — Payload Builder in `EduQuestView.vue`

Replace the `handleFinalSubmit` logic with:

```js
const sessionMap = { beginning: "BOT", mid: "MID", end: "EOT" };

const handleFinalSubmit = async () => {
  isSubmitting.value = true;
  serverMessage.value = "";

  const payload = {
    session: sessionMap[requestType.value],
    material: materials.value[0]?.id ?? null,
    school: {
      name: schoolDetails.value.name,
      representative: schoolDetails.value.representative,
      location: schoolDetails.value.location,
      address: schoolDetails.value.address,
      phone: schoolDetails.value.phone,
      email: schoolDetails.value.email,
      delivery_date: schoolDetails.value.deliveryDate,
    },
    levels: Object.entries(selectedLevels.value).map(([level, data]) => ({
      level,
      subjects: data.subjects,
    })),
    total_sets: totalSets.value,
    estimated_amount: estimatedAmount.value,
  };

  try {
    const resp = await questApi.placeOrder(payload);
    console.log("Order placed:", resp.reference);
    currentStep.value = 5;
  } catch (err) {
    serverMessage.value = "Failed to submit request. Please try again.";
  } finally {
    isSubmitting.value = false;
  }
};
```

---

## Expected Success Response

```json
{
  "id": 7,
  "reference": "EQ-A3F7D91C",
  "username": "jnakato",
  "material": 12,
  "material_title": "P.6 BOT Exam 2026",
  "session": "BOT",
  "school_name": "Kampala Parents School",
  "representative": "Jane Nakato",
  "location": "Kampala",
  "address": "Plot 45, Kololo Hill",
  "phone": "0781234567",
  "email": "principal@kps.ac.ug",
  "delivery_date": "2026-03-15",
  "levels_data": [...],
  "total_sets": 350,
  "estimated_amount": "700000.00",
  "status": "PENDING",
  "ordered_at": "2026-02-22T19:00:00Z"
}
```

---

## Migration Command

After updating `models.py`, run:

```bash
python manage.py makemigrations eduquest
python manage.py migrate
```
