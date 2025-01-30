from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, loan_list_view, loan_create_view, loan_detail_view

router = DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loan")

urlpatterns = [
    # Frontend Routes
    path('', loan_list_view),
    path('loans/', loan_list_view, name='loan-list'),
    path('loans/create/', loan_create_view, name='loan-create-form'),
    path('loans/<int:pk>/', loan_detail_view, name='loan-detail'),

    # API Routes
    path('', include(router.urls)),
]
