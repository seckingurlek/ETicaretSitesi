from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.

class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    keywords = models.CharField(max_length=250)
    company = models.CharField(max_length=50)
    adress = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=50)
    email= models.CharField(blank=True,max_length=50)
    smtpemail= models.CharField(blank=True,max_length=30)
    smtppassword= models.CharField(blank=True,max_length=10)
    smtpport= models.CharField(blank=True,max_length=5)
    smtpserver= models.CharField(blank=True,max_length=20)
    icon = models.ImageField(blank=True,upload_to='images/')
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    aboutus= RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS)
    def __str__(self):
        return self.title

