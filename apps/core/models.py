import os
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import make_aware
from django_ckeditor_5.fields import CKEditor5Field

from pytils import translit


def upload_course(instance, filename):
    return os.path.join('media/article/{}'.format(translit.slugify(instance.title)), filename)


def upload_news(instance, filename):
    return os.path.join('media/news/{}'.format(instance.slug), filename)


class User(AbstractUser):
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    location = models.CharField(max_length=30, null=True, blank=True, verbose_name='Страна')
    birth_date = models.DateField(null=True, blank=True, verbose_name='День рождения')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name if not self.first_name is None else ""}'

    def __str__(self):
        return f'{self.id} {self.get_full_name()}'


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=100, verbose_name='Имя тега')
    slug = models.SlugField(verbose_name='url', null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = translit.slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Тег {self.name}'


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, verbose_name='Имя категории')
    slug = models.SlugField(verbose_name='url', null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = translit.slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Категория {self.name}'


class DateTimeAbstractModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.now, null=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', default=timezone.now, null=True)

    def save(self, *args, **kwargs):
        self.updated_at = make_aware(datetime.datetime.now())
        super(DateTimeAbstractModel, self).save(*args, **kwargs)


class Article(DateTimeAbstractModel):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['likes']

    title = models.CharField(max_length=1000, verbose_name='Название')
    title_description = models.CharField(max_length=1000, verbose_name='Описание в заголовке')
    author = models.ForeignKey(User, related_name='author_article', verbose_name='Автор', on_delete=models.SET_NULL,
                               null=True)
    image = models.FileField(verbose_name='Изображение статьи', null=True, blank=True, upload_to=upload_course,
                             max_length=300)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True, verbose_name="URL")
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='articles')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='articles', blank=True)
    likes = models.PositiveIntegerField(verbose_name='Лайки', blank=True, default=0)

    def get_absolute_url(self):
        return f'/article/{self.slug}'

    def __str__(self):
        return self.title


class Comment(DateTimeAbstractModel):
    class Meta:
        verbose_name = 'Комментарий к статье'
        verbose_name_plural = 'Комментарии к статье'

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='comments', on_delete=models.SET_NULL,
                             null=True)
    article = models.ForeignKey(Article, verbose_name='Статья', related_name='comments', on_delete=models.SET_NULL,
                               null=True)
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


class News(DateTimeAbstractModel):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание новости')
    first_body = CKEditor5Field(verbose_name='Первый текст новости', config_name='extends')
    first_image = models.FileField(verbose_name='Первое изображение', upload_to=upload_news, max_length=300)
    second_body = CKEditor5Field(verbose_name='Второй текст новости', config_name='extends')
    second_image = models.FileField(verbose_name='Второе изображение', upload_to=upload_news, null=True, blank=True)
    preview_image = models.FileField(verbose_name='Превью картинка', null=True, blank=True, upload_to=upload_news,
                                     max_length=300)

    slug = models.SlugField(max_length=200, db_index=True, blank=True, unique=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        name = self.title
        self.slug = translit.slugify(name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/news/{self.slug}'

    def __str__(self):
        return self.title
