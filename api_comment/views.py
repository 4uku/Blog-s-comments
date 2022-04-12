from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentsSerialzier
from django.shortcuts import get_object_or_404

class ArticleViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = CommentsSerialzier

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, pk=article_id)
        return Comment.objects.filter(article=article)
