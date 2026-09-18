from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Идентификатор', max_length=100, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'размер'
        verbose_name_plural = 'размеры'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Идентификатор', max_length=100, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    color = models.CharField('Цвет', max_length=50)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    descriprion = models.TextField('Описание', blank=True)
    main_image = models.ImageField('Изображение', upload_to='products/main/')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_size'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
    )
    stock = models.IntegerField(default=0)

    def __str__(self):
        return (
            f'{self.size.name} ({self.stock} в наличии) - '
            f'{self.product.name}'
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Название'
    )
    image = models.ImageField(upload_to='products/extra/')
