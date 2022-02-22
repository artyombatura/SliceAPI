import datetime

from django.db.models import Count, F
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import CreditCard, Dish, LastVisitedRestaurants, Order, Restaurant, User
from .serializers import (
    CreateOrderSerializer,
    CreditCardSerializer,
    ExtendedDishSerializer,
    OrderHistorySerializer,
    RestaurantSerializer,
    SignUpSerializer,
    UpdateOrderSerializer,
    UpdateUserSerializer,
    UserSerializer,
)


class RestaurantsList(GenericViewSet, mixins.ListModelMixin):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantMenuView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = ExtendedDishSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get("id")
        queryset = Dish.objects.filter(restaurant_id=restaurant_id)
        return queryset


class SignUpView(GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "User created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"auth_token": token.key, "user": UserSerializer(instance=user).data}
        )


class UpdateUserView(GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class BaseOrderView(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by("-date")
        return queryset


class OrderHistoryView(BaseOrderView, mixins.ListModelMixin):
    serializer_class = OrderHistorySerializer


class DeleteOrderView(BaseOrderView, mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Success": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class CreateOrderView(BaseOrderView, mixins.CreateModelMixin):
    serializer_class = CreateOrderSerializer


class UpdateOrderView(BaseOrderView, mixins.UpdateModelMixin):
    serializer_class = UpdateOrderSerializer


class LastVisitedRestaurantsView(GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = (
            LastVisitedRestaurants.objects.all()
            .filter(user=user)
            .order_by("-date", "restaurant")
        )
        # getting unique restaurants, because SQLite database doesn't supports distinct on queries from django ORM
        unique_restaurant_queryset = []
        for last_visited_restaurant in queryset:
            if last_visited_restaurant.restaurant not in unique_restaurant_queryset:
                unique_restaurant_queryset.append(last_visited_restaurant.restaurant)
        return unique_restaurant_queryset


class MostPopularRestaurantsView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        TOP_RESTAURANT_COUNT = 5

        # get TOP_RESTAURANT_COUNT (or less) most popular restaurants for last 24 hours
        date_from = timezone.now() - datetime.timedelta(days=1)
        top_restaurants_visited_for_24_hours = (
            Restaurant.objects.all()
            .filter(visit__date__gte=date_from)
            .annotate(id__count=Count("visit", distinct=True))
            .order_by("-id__count")
        )[:TOP_RESTAURANT_COUNT]

        top_restaurants_visited_for_24_hours_number = len(
            top_restaurants_visited_for_24_hours
        )

        if top_restaurants_visited_for_24_hours_number == TOP_RESTAURANT_COUNT:
            return top_restaurants_visited_for_24_hours

        elif top_restaurants_visited_for_24_hours_number < TOP_RESTAURANT_COUNT:
            # get TOP_RESTAURANT_COUNT lately visited restaurants
            top_ever_visited_restaurants = (
                Restaurant.objects.all()
                .order_by("-visit__date")
                .annotate(id__count=Count("visit", distinct=True))
                .order_by("-id__count")
            )[:TOP_RESTAURANT_COUNT]
            return top_ever_visited_restaurants


class BaseCreditCardView(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CreditCard.objects.filter(user=user)
        return queryset


class LinkCreditCardView(BaseCreditCardView, mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "Credit card linked successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class GetCreditCardsView(BaseCreditCardView, mixins.ListModelMixin):
    pass


class DeleteCreditCardView(BaseCreditCardView, mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Success": "Credit card deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
