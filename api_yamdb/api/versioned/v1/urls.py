from django.urls import include, path
from rest_framework import routers

from api.versioned.v1.routers import CustomRouter
from users.views import UserViewSet, register, get_token
from api.versioned.v1.views import (
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet
)

router = CustomRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='login'),
]
