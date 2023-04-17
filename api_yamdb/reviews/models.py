from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User

LENGTH = 15


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', db_index=True)
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Автор')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанр'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    name = models.CharField(max_length=256, verbose_name='Имя', db_index=True)
    year = models.SmallIntegerField(
        verbose_name='Год',
        db_index=True,
        validators=(validate_year,),
    )

    class Meta:
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'
