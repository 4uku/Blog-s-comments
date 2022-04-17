from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Article(models.Model):
    '''
    Модель поста. Так как требований к авторизации не было,
    то автор - обычное текстовое поле.
    '''

    author = models.CharField('Автор поста', max_length=50)
    text = models.CharField('Текст поста', max_length=120)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['pub_date']


class Comment(MPTTModel):
    '''
    Модель комментария
    '''

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        related_name='comments')
    author = models.CharField('Автор комментария', max_length=50)
    text = models.CharField('Текст поста', max_length=120)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
        related_name='answers',
        null=True, blank=True)

    class MPTTMeta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        order_insertion_by = ['pub_date']

    def children(self):
        return Comment.objects.filter(parent=self)
