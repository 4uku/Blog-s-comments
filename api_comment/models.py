from django.db import models


class Post(models.Model):
    '''
    Модель поста. Так как требований к авторизации не было,
    то автор - обычное текстовое поле.
    '''
    author = models.CharField('Автор поста', max_length=50)
    text = models.CharField('Текст поста', max_length=120)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)