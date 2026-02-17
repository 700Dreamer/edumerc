from .models import Category, Product, Cart, CartItem, Order, OrderItem, Bundle, Wishlist
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer, BundleSerializer, WishlistSerializer
)
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """GET /shop/categories/{id}/products/ — products in this category"""
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
            item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()
            return Response(CartSerializer(cart).data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=400)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = self.request.user.cart
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = serializer.save(user=self.request.user, total_price=total_price)
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

class BundleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return Wishlist.objects.filter(id=wishlist.id)

    @action(detail=False, methods=['post'])
    def toggle_item(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
                message = "Removed from wishlist"
            else:
                wishlist.products.add(product)
                message = "Added to wishlist"
            
            return Response({
                "message": message,
                "wishlist": WishlistSerializer(wishlist).data
            })
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=400)
