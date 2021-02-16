from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetAuthPairToken, GetConfirmCodeView, ReviewViewSet,
                    TitleViewSet, UserViewSet)

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('reviews', ReviewViewSet)
v1_router.register('comments', CommentViewSet)
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet)
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    )


authpatterns = [
    path(
        'email/',
        GetConfirmCodeView.as_view(),
        name='confirmation_code'
    ),
    path(
        'token/',
        GetAuthPairToken.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]

urlpatterns = [
    path('v1/auth/', include(authpatterns)),
    path('v1/', include(v1_router.urls)),
    ]
