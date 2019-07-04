from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class BookType(models.Model):
    book_type = models.CharField(max_length=200)

    def __str__(self):
        return self.book_type

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    amount = models.IntegerField(default=10)
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE, null=False)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.book_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True
        was_published_recently.short_description = 'Published recently?'

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username


class RentalBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.IntegerField()
    rental_at = models.DateTimeField(default=timezone.now(), blank=True)

class Returns(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False) 
    returndate = models.DateTimeField(auto_now=False, auto_now_add=False)
    amount = models.IntegerField(default=0)

    # def __unicode__(self):
    #     return self.user_id, self.book, self.returndate