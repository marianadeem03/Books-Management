from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import (
    path,
    include,
    re_path as urls,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [

    urls(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    urls(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),

    path("admin/", admin.site.urls),
    path("auth/", include("auths.urls")),
    path("", include("users.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
