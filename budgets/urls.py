from .views import BudgetViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"budgets", BudgetViewset, "budgets")

urlpatterns = router.urls
