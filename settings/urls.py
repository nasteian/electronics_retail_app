from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.views import (
    RetailObjectViewSet,
    RetailObjectStatisticsViewSet,
    ProductObjectViewSet,
    SendEmailView,
)

router = DefaultRouter()
router.register(r"retail_object", RetailObjectViewSet, basename="retail_object")
router.register(r"product", ProductObjectViewSet, basename="product")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token", TokenObtainPairView.as_view()),
    path("api/token/refresh", TokenRefreshView.as_view()),
    path("api/token/verify", TokenVerifyView.as_view()),
    path(
        "retail_object/statistics",
        RetailObjectStatisticsViewSet.as_view({"get": "list"}),
    ),
    path("retail_object/send_email", SendEmailView.as_view(), name="send"),
]

urlpatterns += router.urls
