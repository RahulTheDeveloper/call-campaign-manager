from django.urls import path
from .views import AgentListCreateAPIView, AgentDetailAPIView,AgentDeleteApiView,CampaignRetrieveUpdateAPIView,CampaignListCreateAPIView,CampaignResultListCreateAPIView,CampaignResultRetrieveUpdateAPIView,RegisterAPIView,LogoutAPIView,CampaignResultDeleteAPIView,CampaignDeleteAPIView,LoginUserView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)

urlpatterns = [
     path('auth/register/', RegisterAPIView.as_view()),
     path('auth/login/', LoginUserView.as_view(), name='custom_login'),
     path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("auth/logout/", LogoutAPIView.as_view()),


    path('agents/', AgentListCreateAPIView.as_view(), name='agent-list'),
    path('agents/<uuid:pk>/', AgentDetailAPIView.as_view(), name='agent-detail'),
    path('agents/<uuid:pk>/', AgentDeleteApiView.as_view(), name='agent-deleted'),

    path('campaigns/', CampaignListCreateAPIView.as_view()),
    path('campaigns/<uuid:pk>/', CampaignRetrieveUpdateAPIView.as_view()),
    path('campaigns/<uuid:pk>/',CampaignDeleteAPIView.as_view()),

    # Campaign Results
    path('campaign-results/', CampaignResultListCreateAPIView.as_view()),
    path('campaign-results/<uuid:pk>/', CampaignResultRetrieveUpdateAPIView.as_view()),
    path('campaign-results/<uuid:pk>/',CampaignResultDeleteAPIView.as_view()),


]
