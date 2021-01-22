from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User
from django.views import View
import re 


class Signup(View):
    def get(self, request):
        return render(request,'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        email = postData.get('email')
        password = postData.get('password')
        password2 =postData.get('cpassword')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None
        if password != password2 :
            error_message = 'Password must be same'

        user = User(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password)
        error_message = self.validateUser(user)

        if not error_message:
            print(first_name, last_name, email, password)
            user.password = make_password(user.password)
            user.register()
            success_msg="Registered Successfully !!!"
            data = {
                'success': success_msg,
            }
            return render(request,'signup.html',data)
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request,'signup.html',data)

    def validateUser(self,user):
        error_message = None;
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (not user.first_name):
            error_message = "First Name Required !!"
        elif len(user.first_name) <= 2:
            error_message = 'First Name must be 3 char long or more'
        elif not user.last_name:
            error_message = 'Last Name Required'
        elif len(user.last_name) <= 2:
            error_message = 'Last Name must be 3 char long or more'
        elif len(user.password) < 6:
            error_message = 'Password must be 6 char long'    
        elif len(user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif (re.search(regex,user.email))==False:
            error_message = 'Email is not Valid'    
        elif user.isExists():
            error_message = 'Email Address Already Registered..'
        return error_message