from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)

    class Meta:
        model = Article
        fields = ('id', 'author', 'text', 'pub_date', 'comments')


class CommentsSerialzier(serializers.ModelSerializer):
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)
    answers = ArticleSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'answers')