from this import d
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentsSerialzier
from django.shortcuts import get_object_or_404

class ArticleViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = CommentsSerialzier

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        queryset = get_object_or_404(Article, id=article_id).comments.filter(parent=None).prefetch_related('answers')
        return queryset

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, pk=article_id)
        if 'comment_id' in self.kwargs:
            comment_id = self.kwargs.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            serializer.save(article=article, parent=comment)
        serializer.save(article=article)