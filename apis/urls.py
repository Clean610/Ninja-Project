from django.urls import path
from apis.views.v1 import schools

urlpatterns = [
    path('v1/', schools.api.urls),
]
