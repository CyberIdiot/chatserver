from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# models.py SQLite3 database tables


class AppUser(models.Model):
    UserName = models.CharField(
        max_length=150,
        unique=True,
    )
    Password = models.CharField(max_length=256)
    Email = models.EmailField(blank=True)

    def __str__(self):
        return self.UserName

    @staticmethod
    def user_login(username, password):
        try:
            log_user = AppUser.objects.filter(UserName=username)
            if log_user.Password == password:
                return log_user
            else:
                return None
        except AppUser.DoesNotExist:
            return None

    @staticmethod
    def user_create(username, password, email):
        try:
            user = AppUser.objects.filter(UserName=username)
            return user
        except AppUser.DoesNotExist:
            new_user = AppUser(UserName=username, Password=password, Email=email)
            new_user.save()
            return new_user


class UserProfile(models.Model):
    LinkUser = models.OneToOneField(AppUser, on_delete=models.CASCADE,)
    NickName = models.CharField(max_length=32)
    Birthday = models.CharField(max_length=24)
    Friends = models.ManyToManyField("self", related_name="myFriends")

    def __str__(self):
        return self.NickName


# class Friends(models.Model):
#    UID1 = models.ForeignKey(ChatUser)
#    UID2 = models.ForeignKey(ChatUser)

#    def __str__(self):
#        return self.UID1 + 'to' + self.UID2

class Messages(models.Model):
    MessageFrom = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="MessageFrom")
    MessageTo = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="MessageTo")
    MessageType = models.CharField(max_length=10)
    MessageDate = models.DateTimeField()
    MessageCont = models.CharField(max_length=256)

    def __str__(self):
        return self.MessageCont