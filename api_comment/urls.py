from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article-viewset')
router.register(r'article/(?P<article_id>[^/.]+)/comments', CommentViewSet, basename='comment-viewset')
router.register(r'article/(?P<article_id>[^/.]+)/(?P<comment_id>[^/.]+)/comments', CommentViewSet, basename='comment-viewset')


urlpatterns = [
    path('', include(router.urls))
]
