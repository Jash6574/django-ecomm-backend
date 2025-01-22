from django.urls import path
from .views import RetrieveAllUsers,RetrieveUserById

urlpatterns = [
    path('all/', RetrieveAllUsers.as_view(), name='retrieve_users'),
    path('<int:id>/', RetrieveUserById.as_view(), name='retrieve_user_by_id')
]
