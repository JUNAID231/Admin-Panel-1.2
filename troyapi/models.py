from django.db import models
#from django.contrib import auth
# Create your models here.

class User(models.Model):
    firstname = models.CharField (max_length=50)
    lastname = models.CharField (max_length=50)
    emailaddress = models.CharField (max_length=50)
    password = models.CharField(max_length=50)
    user_id = models.AutoField(primary_key=True)
    wallet_id = models.CharField(max_length=50)
    signup_token = models.CharField(max_length=50)
    signup_timestamp = models.DateTimeField(auto_now_add=True)
    suspend = models.CharField(max_length=30, default="False")

    picture = models.ImageField(upload_to='profile_image', max_length=255, default='profile_image/default.jpg')

    signin_token = models.CharField(max_length=50)
    signin_timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        #return '{} {} {}'.format(self.firtname, self.lastname, self.emailaddress, self.signup_token)
        template = '{0.firtname} {0.lastname} {0.emailaddress} {0.signup_token}'
        return template.format(self)
        #return self.emailaddress

class Transaction (models.Model):
    from_walletID = models.IntegerField ()
    to_walletID = models.IntegerField ()
    to_emailaddress = models.CharField(max_length=50)
    amount = models.IntegerField ()
    status = models.CharField (max_length=50, default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    transaction_code = models.CharField(max_length=50)

    def __str__(self):
        return  self.status

class News(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    photo = models.ImageField(upload_to='profile_image', default='default.png')
    auther = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    news_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.auther

class Admin(models.Model):
    firstname = models.CharField (max_length=50)
    lastname = models.CharField (max_length=50)
    emailaddress = models.CharField (max_length=50)
    password = models.CharField(max_length=50)
    admin_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    suspend = models.CharField(max_length=30, default="False")

    def __str__(self):
        return  self.firstname


class ChatUser(models.Model):
    firstname = models.CharField (max_length=50)
    lastname = models.CharField (max_length=50)
    emailaddress = models.CharField (max_length=50)
    password = models.CharField(max_length=50)
    user_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    suspend = models.CharField(max_length=30, default="False")
    picture = models.ImageField(upload_to='profile_image', max_length=255, default='profile_image/default.jpg')

    def __str__(self):
        template = '{0.firtname} {0.lastname} {0.emailaddress} {0.token}'
        return template.format(self)


class Chat (models.Model):
    sender_user_id = models.IntegerField ()
    reeceiver_user_id = models.IntegerField () 
    message = models.TextField ()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    chat_id = models.AutoField(primary_key=True)

    def __str__(self):
        template = '{0.sender_user_id} {0.reeceiver_user_id} {0.message} {0.timestamp}'
        return template.format(self)