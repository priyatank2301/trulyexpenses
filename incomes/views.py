from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Income,Source
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference



# Create your views here.
@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_incomes(request):
    if request.method =='POST':
        search_str=json.loads(request.body).get('searchText')

        incomes=Income.objects.filter(owner=request.user,amount__istartswith=search_str)|Income.objects.filter(
            owner=request.user,date__istartswith=search_str)|Income.objects.filter(
                owner=request.user,source__icontains=search_str)|Income.objects.filter(
                    owner=request.user,description__icontains=search_str)
        
        data=incomes.values()
        return JsonResponse(list(data),safe=False)


@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    sources = Source.objects.all()
    incomes=Income.objects.filter(owner=request.user)
    paginator=Paginator(incomes,5)
    page_number=request.GET.get('page')
    page_obj= Paginator.get_page(paginator,page_number)
    currency=UserPreference.objects.get(user=request.user).currency
    context={
        'incomes': incomes,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'incomes/index.html',context)


@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_income(request):
    sources = Source.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')  
        source_id = request.POST.get('source')  

        # Validate required fields
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomes/add_income.html', {'sources': sources, 'value': request.POST})

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'incomes/add_income.html', {'sources': sources, 'value': request.POST})
        
        if not source_id:
            messages.error(request, 'Source is required')
            return render(request, 'incomes/add_income.html', {'sources': sources, 'value': request.POST})

        # Fetch the Category object
        source = get_object_or_404(Source, id=source_id)

        # Handle date: use today's date if none is provided
        if not date:
            date = timezone.now().date()  # Get current date

        # Create the expense
        Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=date)
        messages.success(request, 'Income saved successfully')
        return redirect('incomes')  # Ensure 'expenses' is the correct URL name for redirection

    return render(request, 'incomes/add_income.html', {'sources': sources, 'value': {}})

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, 'incomes/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source_id = request.POST['source']

        # Validation checks
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomes/edit_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'incomes/edit_income.html', context)

        if not date:
            date = income.date

        # Fetch the actual Source object using the ID from the form
        source = Source.objects.get(id=source_id)

        # Update the income with the correct values
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source.name 
        income.save()

        messages.success(request, 'Income updated successfully')
        return redirect('incomes')
    
@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income Deleted Successfully')
    return redirect('incomes')


