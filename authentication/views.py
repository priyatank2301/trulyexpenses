from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import token_generator
from django.urls import reverse
from django.contrib import auth


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
        """messages.success(request,'Registered Successfully..!')
        messages.warning(request,'Registered Successfully..! warning')
        messages.info(request,'Registered Successfully..! info')
        messages.error(request,'Registered Successfully..! error')
        return render(request, 'authentication/register.html')"""

        # Get User Data
        # Validate
        # Create User

        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password must be at least 6 characters')
                    return render(request, 'authentication/register.html',context)
                user=User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()

                #mailsend
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                email_subject='Activate Your TrulyExpenses Account'
                activate_url='http://'+domain+link
                # path_to_view
                email_body = 'Hey ' + user.username + ', Please use the below link to activate your account: \n' + activate_url

                email = EmailMessage(
                email_subject,
                email_body,  # Now this is a single string
                'priyatank2301@gmail.com',
                [email],  # Ensure the recipient email variable is correct
                )

                email.send(fail_silently=False)
                messages.success(request,'Account created successfully')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            # Decode the uidb64 to get the user ID
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # Check if the token is valid for the user
            if not token_generator.check_token(user, token):
                return redirect('login?message=User already activated')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            messages.error(request, 'Activation link is invalid or has expired.')
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
