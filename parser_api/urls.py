from django.urls import path, include
from rest_framework import routers

from parser_api.views import ProductViewSet, ProductExactFieldViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path(
        "products/<int:pk>/<str:field>/",
        ProductExactFieldViewSet.as_view(),
        name="product-exact-field"
    ),
]

app_name = "parser_api"
