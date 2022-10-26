from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', user_registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('', Home.as_view(), name='home'),
    path('subscription_add/', AddSubscription.as_view(), name='subscription_add'),
    path('subscriptions/<int:pk>/edit', EditSubscription.as_view(), name='edit_subscription'),
    path('remove_subscription/<int:pk>', RemoveSubscription.as_view(), name='remove_subscription'),
    path('subscription_delete_error', subscription_delete_error, name='subscription_delete_error'),
]
