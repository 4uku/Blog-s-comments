from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from .models import Article, Comment
from .serializers import (ArticleSerializer, Comment3rdLevelSerializer,
                          CommentsSerialzier)


class ArticleViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    '''
    GET запрос возвращает список статей.
    POST запрос создает статью. Требуемые поля author и text.
    '''
    queryset = Article.objects.annotate(comments_count=Count('comments'))
    serializer_class = ArticleSerializer

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentsSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        Comment.objects.create(article=article, **serializer.validated_data)
        return Response(status=HTTP_201_CREATED)


class CommentViewSet(GenericViewSet, ListModelMixin):
    '''
    GET запрос с указанием ID статьи вернет все комментарии для статьи
    до 3 уровня вложенности.
    POST запрос add_answer создает комментарий в ответ на комментарий.
    Требуемые поля author и text.
    POST запрос add_comment создает комментарий к статье.
    Требуемые поля author и text.
    '''
    serializer_class = CommentsSerialzier

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        queryset = Comment.objects.filter(
            article_id=article_id,
            parent=None,
            level__lte=3).prefetch_related('answers')
        return queryset

    @action(detail=True, methods=['POST'])
    def add_answer(self, request, article_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentsSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        Comment.objects.create(
            **serializer.validated_data,
            article=comment.article,
            parent=comment)
        return Response(status=HTTP_201_CREATED)


class Comment3rdLvlViewSet(GenericViewSet, ListModelMixin):
    '''
    GET запрос all_comments вернет все комментарии для комментария 3 уровня
    '''
    serializer_class = Comment3rdLevelSerializer

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        queryset = Comment.objects.get(
            id=comment_id).answers.prefetch_related('answers')
        return queryset
