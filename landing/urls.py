from django.urls import path
from .views import landing_page , admin_review_requests, approve_request ,signup

urlpatterns = [
    path('', landing_page, name='landing_page'),

    path('signup/', signup, name='signup'),

    path('admin_client/review/', admin_review_requests, name='admin_review_requests'),
    path('admin_client/approve/<int:request_id>/', approve_request, name='approve_request'),
]
