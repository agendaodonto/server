from django.conf.urls import url

from app.testing.reset import ResetAPI

urlpatterns = [
    url(r'^$', ResetAPI.as_view(), name='reset-api'),
]
