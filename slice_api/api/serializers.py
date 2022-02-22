from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from .models import (
    Country,
    CreditCard,
    Dish,
    LastVisitedRestaurants,
    Order,
    OrderDish,
    Photo,
    Restaurant,
    User,
)


class RestaurantSerializer(serializers.ModelSerializer):
    photo_url = serializers.CharField(source="photo.url", allow_null=True)

    class Meta:
        model = Restaurant
        fields = ["id", "photo_url", "name", "description", "address", "phone_number"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "description"]


class DishBaseSerializer(serializers.ModelSerializer):
    photo_url = serializers.CharField(source="photo.url", allow_null=True)

    class Meta:
        model = Dish
        fields = [
            "id",
            "name",
            "description",
            "weight",
            "price",
            "estimated_time",
            "photo_url",
        ]


class ExtendedDishSerializer(DishBaseSerializer):
    dish_type = serializers.CharField(source="dish_type.name")
    country = CountrySerializer()

    class Meta(DishBaseSerializer.Meta):
        fields = DishBaseSerializer.Meta.fields + [
            "dish_type",
            "country",
        ]


class SignUpSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(source="photo.url", required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "email",
            "last_name",
            "password",
            "avatar_url",
        ]

        extra_kwargs = {
            "email": {
                "write_only": True,
            },
            "username": {"write_only": True},
            "first_name": {"write_only": True},
            "last_name": {"write_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.get("photo", None):
                url = validated_data.pop("photo")["url"]
                photo = Photo.objects.create(url=url)
                validated_data["photo"] = photo
            user = User.objects.create_user(**validated_data)
            return user


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(
        source="photo.url", required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "avatar_url"]


class UpdateUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(
        source="photo.url", required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "avatar_url",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "password": {"write_only": True, "required": False},
        }

    def update(self, user, validated_data):
        with transaction.atomic():
            user.email = validated_data.get("email", user.email)
            user.username = validated_data.get("username", user.username)
            user.first_name = validated_data.get("first_name", user.first_name)
            user.last_name = validated_data.get("last_name", user.last_name)

            password = validated_data.get("password", None)
            if password:
                user.password = make_password(password)

            avatar_url = validated_data.get("photo", None)
            if avatar_url:
                photo = Photo.objects.create(url=avatar_url["url"])
                user.photo = photo

            user.save()
            return user


class OrderHistorySerializer(serializers.ModelSerializer):
    dishes = DishBaseSerializer(many=True, read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "date", "status", "restaurant", "dishes"]


class CreateOrderSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(many=True, queryset=Dish.objects.all())

    class Meta:
        model = Order
        fields = ["id", "date", "status", "restaurant", "dishes"]
        read_only_fields = ["id", "status"]

    def validate(self, data):
        for dish in data["dishes"]:
            if dish.restaurant != data["restaurant"]:
                raise serializers.ValidationError(
                    {
                        "Error": f"{dish.name} is not from {data['restaurant'].name} restaurant!"
                    }
                )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            print(validated_data)
            user = self.context["request"].user
            restaurant = validated_data["restaurant"]
            dishes = validated_data["dishes"]
            order = Order.objects.create(user=user, restaurant=restaurant)

            for dish in dishes:
                OrderDish(order=order, dish=dish).save()
            date = validated_data.get("date", None)
            if date:
                order.date = date
                order.status = Order.STATUS_CHOICES[1][1]
            else:
                order.status = Order.STATUS_CHOICES[0][1]

            order.save()
            LastVisitedRestaurants.objects.create(user=user, restaurant=restaurant)
            return order

    def to_representation(self, obj):
        self.fields["restaurant"] = RestaurantSerializer()
        self.fields["dishes"] = ExtendedDishSerializer(many=True)
        return super().to_representation(obj)


class UpdateOrderSerializer(OrderHistorySerializer):
    class Meta(OrderHistorySerializer.Meta):
        read_only_fields = ["id", "date", "restaurant", "dishes"]

    def validate(self, data):
        status = data["status"]
        for choice in Order.STATUS_CHOICES:
            if status == choice[1]:
                return data
        raise serializers.ValidationError(
                    {
                        "Error": f"{status} is not a valid status!"
                    }
                )

    def update(self, order, validated_data):
        with transaction.atomic():
            order.status = validated_data.get("status", order.status)
            order.save()
            return order


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ["id", "number", "expiration_date", "cvv"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = self.context["request"].user
        credit_card = CreditCard.objects.create(user=user, **validated_data)
        return credit_card
