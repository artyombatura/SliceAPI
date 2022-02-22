from django.urls import path
from rest_framework import routers

from .views import (
    CreateOrderView,
    DeleteCreditCardView,
    DeleteOrderView,
    GetCreditCardsView,
    LastVisitedRestaurantsView,
    LinkCreditCardView,
    LoginView,
    MostPopularRestaurantsView,
    OrderHistoryView,
    RestaurantMenuView,
    RestaurantsList,
    SignUpView,
    UpdateOrderView,
    UpdateUserView,
)

router = routers.DefaultRouter()

router.register("signup", SignUpView, basename="signup")
router.register("update-profile", UpdateUserView, basename="update-profile")
router.register("restaurants", RestaurantsList, basename="restaurants")
router.register(
    "get-restaurant-menu", RestaurantMenuView, basename="get-restaurant-menu"
)
router.register("create-order", CreateOrderView, basename="create-order")
router.register("update-order", UpdateOrderView, basename="update-order")
router.register("delete-order", DeleteOrderView, basename="delete-order")
router.register("get-orders-history", OrderHistoryView, basename="get-orders-history")
router.register(
    "get-last-visited-restaurants",
    LastVisitedRestaurantsView,
    basename="get-last-visited-restaurants",
)
router.register(
    "get-popular-restaurants",
    MostPopularRestaurantsView,
    basename="get-popular-restaurants",
)
router.register(
    "link-credit-card",
    LinkCreditCardView,
    basename="link-credit-card",
)
router.register(
    "get-credit-cards",
    GetCreditCardsView,
    basename="get-credit-cards",
)
router.register(
    "delete-credit-card",
    DeleteCreditCardView,
    basename="delete-credit-card",
)


urlpatterns = router.urls
urlpatterns += [
    path("login/", LoginView.as_view(), name="login"),
]
