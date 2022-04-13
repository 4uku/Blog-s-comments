from rest_framework import serializers
from .models import Article, Comment
from rest_framework_recursive.fields import RecursiveField

class CommentsSerialzier(serializers.ModelSerializer):
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)
    answers = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'answers')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'author', 'text', 'pub_date', 'comments')
    
    def get_comments(self, obj: Article):
        return obj.comments.count()
