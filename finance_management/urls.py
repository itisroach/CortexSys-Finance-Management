from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Finance Management API",
        default_version="v1",
        description="A Finance Management API For Managing You Finances",
        contact=openapi.Contact(email="rouchashoori@gmail.com"),
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("transactions.urls")),
    path("api/", include("budgets.urls")),
    path(
        "api/documentation/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
]
