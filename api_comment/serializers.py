from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Article, Comment


class CommentsSerialzier(serializers.ModelSerializer):
    '''
    Сериализатор для комментариев
    '''
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'answers')
        extra_kwargs = {
            'answers': {
                'read_only': True
            }
        }

    def get_answers(self, obj: Comment):
        if obj.get_level() < 3:
            return CommentsSerialzier(obj.answers, many=True).data
        if obj.get_level() == 3:
            return obj.answers.count()


class Comment3rdLevelSerializer(CommentsSerialzier):
    answers = RecursiveField(many=True, read_only=True)


class ArticleSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для статьи
    '''
    author = serializers.CharField(max_length=50, required=True)
    text = serializers.CharField(max_length=120, required=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'author', 'text', 'pub_date', 'comments')

    def get_comments(self, obj: Article):
        return obj.comments_count
