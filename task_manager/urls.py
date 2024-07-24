from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from task_manager.views import index

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
