from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя с добавленными полями
    и переопределенным email, требуется как уникальное,
    по нему идентифицируется пользователь
    """
    email = models.EmailField(unique=True, null=False)

    class RoleList(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.CharField(
        max_length=128, choices=RoleList.choices,
        default=RoleList.USER,
        )
    bio = models.TextField(default='')

    @property
    def is_admin(self):
        return (
            self.role == self.RoleList.ADMIN or self.is_superuser
            )

    @property
    def is_moderator(self):
        return (
            self.is_admin or self.role == self.RoleList.MODERATOR
            )

    def get_payload(self):
        """
        Полезная нагрузка для формирования confirmation_code
        """
        return {
            'user_id': self.id,
            'email': self.email,
            'username': self.username,
            }

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Category(models.Model):
    """Categories: films, audio or books"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Genre(models.Model):
    """Genres: comedy, thriller etc"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Title(models.Model):
    """Модель Title"""

    name = models.TextField('name')
    category = models.ForeignKey(
                                Category,
                                on_delete=models.SET_NULL,
                                null=True, related_name='titles',
                                )
    genre = models.ManyToManyField(
                                Genre,
                                blank=True,
                                related_name='genres',
                                )
    description = models.TextField('description', null=True)
    year = models.PositiveIntegerField('year')

    def correct_year(self, year):
        if year > 2020:
            raise ValidationError('Год указан некорректно')


class Review(models.Model):
    """Создание модели Review"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
        )
    text = models.TextField(
        'text',
        null=False,
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
        )
    score = models.PositiveSmallIntegerField(
        verbose_name='score',
        validators=[
            MinValueValidator(1, message='Min value 1'),
            MaxValueValidator(10, message='Max value 10'),
            ],
        null=False,
        )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True,
        )


class Comment(models.Model):
    """Создание модели Comment"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        )
    text = models.TextField('text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True,
        db_index=True,
        )
