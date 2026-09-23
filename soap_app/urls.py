from rest_framework.routers import DefaultRouter

from .views import SoapTransactionListView

router = DefaultRouter()
router.register(r'api/transactions', SoapTransactionListView, basename='soap-transactions')
urlpatterns = router.urls
