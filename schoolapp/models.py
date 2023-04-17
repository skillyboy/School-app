from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from datetime import datetime
import datetime


# Create your models here.


class Picture(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')

    class Meta:
        db_table = 'picture'
        managed = True
        verbose_name = ("picture")
        verbose_name_plural = ("pictures")

    def __str__(self):
        return self.user.username
    
class Faculty(models.Model):  
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'faculty'
        verbose_name = 'faculty'
        verbose_name_plural = 'faculties'

class Department(models.Model): 
    facult = models.ForeignKey(Faculty, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()
    paid =  models.BooleanField(default=False)
    available =  models.BooleanField()

    class Meta:
        db_table = 'department'
        managed = True
        verbose_name = ("department")
        verbose_name_plural = ("departments")

    def __str__(self):
        return self.title



class Courses(models.Model): 
    depart = models.ForeignKey(Department, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()
    fee = models.IntegerField()
    paid =  models.BooleanField(default=False)
    available =  models.BooleanField()
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    # note = models.TextField(blank=True, null=True)
    

    class Meta:
        db_table = 'courses'
        managed = True
        verbose_name = ("courses")
        verbose_name_plural = ("courses")

    def __str__(self):
        return self.title
    
class Note(models.Model): 
    content = models.ForeignKey(Courses, on_delete=models.CASCADE , null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()
    chapter = models.IntegerField()
    note = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'note'
        managed = True
        verbose_name = ("note")
        verbose_name_plural = ("notes")

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thecontent = models.ForeignKey(Courses, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    amount = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'wishlist'
        managed = True
        verbose_name = 'wishlist'
        verbose_name_plural = 'Whishlist'

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee = models.IntegerField()
    pay_code = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    order_no = models.CharField(max_length=50)

    def __str__(self):
        return self.username
        
class Mycourse(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='faculty', default='pix.jpg')
    description = models.TextField()
    paid=  models.BooleanField() 

    class Meta:
        db_table = 'mycourse'
        managed = True
        verbose_name = 'mycourse'
        verbose_name_plural = 'mycourses'

    def __str__(self):
        return self.user.username


class Forum(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE , null=True)
    value = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.forum.name

