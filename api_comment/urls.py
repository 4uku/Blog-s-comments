from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='article-viewset')
router.register(r'articles/(?P<article_id>^[\d+]$)', CommentViewSet, basename='comment-viewset')


urlpatterns = [
    path('', include(router.urls))
]
