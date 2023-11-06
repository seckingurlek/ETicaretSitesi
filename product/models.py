from django.db import models

class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    keywords = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    keywords = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    price = models.FloatField()
    amount = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    detail = models.TextField()

    def __str__(self):
        return self.title
