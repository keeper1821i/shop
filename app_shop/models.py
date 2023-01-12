from django.contrib.auth.models import User

from app_users.models import Profile
from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('category_name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Subcategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,
                                         related_name='subcategory_product',
                                         blank=True, null=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField(verbose_name='Количество')
    products_in_stock = models.BooleanField(default=True)
    free_delivery = models.BooleanField(default=False)
    number_of_sales = models.IntegerField(default=0, verbose_name='количество продаж')
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class Reviews(models.Model):
    descriptions = models.TextField(verbose_name='Текст комментария')
    review_product = models.ManyToManyField(Product, related_name='product_review')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name='author_article')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']


    def __str__(self):
        return f'Отзыв № {self.id}'
