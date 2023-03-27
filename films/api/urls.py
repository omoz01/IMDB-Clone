from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='StreamPlatformVS'),
# router.register('stream-list', StreamPlatformListVS, basename='StreamPlatformListVS'),

urlpatterns = [
    path('', views.WatchListAV.as_view(), name='movie_list'),

    path('<int:pk>/', views.WatchListDetailAV.as_view(), name='movie_detail'),
    path('', include(router.urls)),
    path('<int:pk>/reviews/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'), #we should get the review for a particular stream video
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('user-reviews/', views.UserReviewGV.as_view(), name='user-review'),
]