from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.forms import ModelForm, TextInput, Textarea

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
    


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )

    name = models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True,max_length=50)
    subject = models.CharField(blank=True,max_length=20)
    message = models.CharField(blank=True,max_length=255)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    note = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject','message']
        widgets = {
            'name'   : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
            'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
            'email'   : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
            'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
        }

