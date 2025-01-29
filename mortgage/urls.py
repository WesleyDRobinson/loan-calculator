from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet

router = DefaultRouter()
router.register(r"loans", LoanViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
