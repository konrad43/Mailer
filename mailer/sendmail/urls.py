from django.urls import path
from rest_framework import routers

from sendmail import views

router = routers.DefaultRouter()
router.register(r'mailbox', views.MailboxViewSet, base_name='mailbox')
router.register(r'template', views.TemplateViewSet, base_name='template')

urlpatterns = [
    path('email/', views.EmailList.as_view(), name='email'),
    path('', views.api_root)
]

urlpatterns += router.urls