from django.forms.models import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response

from ManageData.Serializers import StoreSerializer, ProductSerializer
from ManageData.models import StoreModel, ProductModel



# Create your views here.
class StoreViewSet(viewsets.ViewSet):
    serializer = StoreSerializer
    queryset = StoreModel.objects.all()

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = StoreModel.objects.all()
            if request.data.get('message') == "Load All Stores":
                datalist = [model_to_dict(item) for item in data]
                return Response(data= datalist, status=status.HTTP_200_OK)
            elif request.uuid is not None:
                uuid = serializer.validated_data['UUID']
                return Response(data=data.get(UUID = uuid), status=status.HTTP_200_OK)
            else:
                return Response("No Store Found", status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response("/ root path endpoint")

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        store_id = self.request.query_params.get("store")
        if store_id is not None:
            queryset = queryset.filter(store_id=store_id)
        return queryset
    
from UserAuth.models import UserAccount
from ManageData.models import Cart, CartItem
from ManageData.Serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):
    """
    Handles:
    - GET /api/cart/  (get user cart)
    - POST /api/cart/ (add item)
    - DELETE /api/cart/ (remove item)
    """

    def list(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        data = CartSerializer(cart).data
        return Response(data, status=200)

    def create(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
        )
        if not created:
            item.quantity += quantity
        item.save()

        return Response({"message": "Item added to cart"}, status=200)

    def destroy(self, request):
        user = request.user
        product_id = request.data.get("product")

        cart = Cart.objects.get(user=user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        return Response({"message": "Item removed"}, status=200)
    
from ManageData.models import Order, OrderItem


class OrderViewSet(viewsets.ViewSet):
    """
    - GET /api/orders/   (user order history)
    - POST /api/orders/  (checkout)
    """

    def list(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        data = OrderSerializer(orders, many=True).data
        return Response(data, status=200)

    def create(self, request):
        user = request.user

        # Get user cart
        cart, created = Cart.objects.get_or_create(user=user)
        items = cart.items.all()

        if not items:
            return Response({"error": "Cart is empty"}, status=400)

        # Create order
        order = Order.objects.create(
            user=user,
            total=0
        )

        total_amount = 0

        # Move cart items → order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_amount += item.product.price * item.quantity

        order.total = total_amount
        order.save()

        # Clear cart
        cart.items.all().delete()

        return Response({"message": "Order placed"}, status=200)

