from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mails(BaseModel):
    mail_address = models.CharField(verbose_name='mail_address',max_length=255)
    
class Blog(models.Model):
    meta_title = models.CharField(verbose_name='meta_title',max_length=255)
    meta_description = models.CharField(verbose_name='meta_description',max_length=255)
    blog_title = models.CharField(verbose_name='blog_title',max_length=255)
    content = RichTextField()
    content_view = models.ImageField(upload_to='blog_images/',null=False,blank=False)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(verbose_name='slug',max_length=500)
    
    def __str__(self):
        return self.blog_title