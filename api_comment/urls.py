from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, Comment3rdLvlViewSet, CommentViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article-viewset')
router.register(
    r'article/(?P<article_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments=viewset'
)
router.register(
    r'comments/(?P<comment_id>[^/.]+)/all_comments',
    Comment3rdLvlViewSet,
    basename='comments=viewset'
)

urlpatterns = [
    path('', include(router.urls)),
]
