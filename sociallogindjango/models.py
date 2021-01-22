from django.db import  models
from django.core.validators import MinLengthValidator

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    
    def register(self):
        self.save()

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False
        
    def isExists(self):
        if User.objects.filter(email = self.email):
            return True
        return  False


