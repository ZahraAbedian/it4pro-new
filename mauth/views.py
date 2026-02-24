from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import countries, industries, myprofile
from django.db.models.functions import Lower
from django.contrib.auth.models import User
import re
from django.contrib.auth.hashers import check_password 
from django.contrib.auth import authenticate, login, logout

# Create your views here. 



def loginPage(request):  
    if request.method == "POST":  
        input = request.POST.get('input')
        password = request.POST.get('pass')  
        
        user_email = User.objects.filter(email=input).first() 
        
        if user_email:  
            username = user_email.username  
        else:
            username = input

        user = authenticate(username=username, password=password)  

        if user is not None:  
            login(request, user)
            return redirect(request.GET.get('next'))
    
        else:  
            message = "Incorrect username or password"  
            return render(request, "mauth/loginPage.html", {"loginMessage": message})  
        
    else:  
         return render(request, "mauth/loginPage.html")
    

def logoutPage(request):
    logout(request)
    return redirect('/')



def signupPage(request):
    mcountries = countries.objects.all().order_by(Lower('country')).values()
    mindustries = industries.objects.all().order_by(Lower('industry')).values()
    if request.method == "POST":
        # email format
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        if(request.POST['pass'] != request.POST['confpass']):
            mmessage = "password and confirm password are not same!!"   

        elif (re.match(pattern, request.POST['pass']) == None):
            mmessage = '''Minimum eight characters,\nat least one uppercase letter,\none lowercase letter and one number'''

        elif(re.match( '[\w\.-]+@[\w\.-]+\.\w{2,4}' , request.POST['email']) == None):
            mmessage = "the email field should contain '@' and '.' before domain!"

        elif(len(User.objects.filter(email=request.POST['email'])) != 0):
            mmessage = "duplicate email"
        
        elif(len(User.objects.filter(username=request.POST['username'])) != 0):
            mmessage = "choose another username"
            
        elif '@' in request.POST['username']:
            mmessage = "username cannot contain @"

        else:
             u = User.objects.create_user(username = request.POST['username'], email = request.POST['email'], password=request.POST['pass'])
             country_fk = countries.objects.get(id=request.POST['countrySelect'])
             industry_fk = industries.objects.get(id=request.POST['industrySelect'])
             p = myprofile(user=u, company_name=request.POST['companyName'], country=country_fk, industry=industry_fk)
             p.save()
             return redirect('/')
        return render(request, "mauth/signupPage.html", {"countries": mcountries, "industries":mindustries, "signUpMessage": mmessage})
    else:
        
        # print(mcountries[0].country)
        return render(request, "mauth/signupPage.html", {"countries": mcountries, "industries":mindustries})
    