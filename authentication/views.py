from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages


class UsernameValidationView(View):
    def post(self, request):
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            
            # Extract the username from the data
            username = data.get('username')  # Correctly extract the username
            
            # Check if the username is valid
            if not username or not str(username).isalnum():
                return JsonResponse({'username_error': 'Username should contain only alphanumeric characters'}, status=400)
            
            # Check if username exits in database or not
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'This Username Already Exists,   Please Choose Other'}, status=409)
            


            return JsonResponse({'username_valid': True})
        
        except json.JSONDecodeError:
            # If the JSON is invalid
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
class EmailValidationView(View):
    def post(self, request):
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            
            # Extract the username from the data
            email = data.get('email') 
            
            # Check if the username is valid
            if not validate_email (email):
                return JsonResponse({'email_error': 'Email Is Invalid'}, status=400)
            
            # Check if username exits in database or not
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_error': 'This Email Already Exists,   Please Choose Other'}, status=409)
            


            return JsonResponse({'email_valid': True})
        
        except json.JSONDecodeError:
            # If the JSON is invalid
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        messages.success(request,'Registered Successfully..!')
        messages.warning(request,'Registered Successfully..! warning')
        messages.info(request,'Registered Successfully..! info')
        messages.error(request,'Registered Successfully..! error')
        return render(request, 'authentication/register.html')

