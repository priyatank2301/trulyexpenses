from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Category, Expense
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_expenses(request):
    if request.method =='POST':
        search_str=json.loads(request.body).get('searchText')

        expenses=Expense.objects.filter(owner=request.user,amount__istartswith=search_str)|Expense.objects.filter(
            owner=request.user,date__istartswith=search_str)|Expense.objects.filter(
                owner=request.user,category__icontains=search_str)|Expense.objects.filter(
                    owner=request.user,description__icontains=search_str)
        
        data=expenses.values()
        return JsonResponse(list(data),safe=False)



@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle UserPreference
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Provide a default currency or redirect to set preferences

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_expense(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')  
        category_id = request.POST.get('category')  

        # Validate required fields
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', {'categories': categories, 'value': request.POST})

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', {'categories': categories, 'value': request.POST})
        
        if not category_id:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', {'categories': categories, 'value': request.POST})

        # Fetch the Category object
        category = get_object_or_404(Category, id=category_id)

        # Handle date: use today's date if none is provided
        if not date:
            date = timezone.now().date()  # Get current date

        # Create the expense
        Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')  # Ensure 'expenses' is the correct URL name for redirection

    return render(request, 'expenses/add_expense.html', {'categories': categories, 'value': {}})

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category_id = request.POST['category']

        # Validation checks
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        if not date:
            date = expense.date


        # Fetch the actual Category object using the ID from the form
        category = Category.objects.get(id=category_id)

        # Update the expense with the correct values
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category.name  
        expense.save()

        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Deleted Successfully')
    return redirect('expenses')

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def expense_category_summary(request):
    todays_date = datetime.date.today()
    last_one_month = todays_date - datetime.timedelta(days=30)
    expenses = Expense.objects.filter(owner=request.user, date__gte=last_one_month, date__lte=todays_date)

    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for category in category_list:
        finalrep[category] = get_expense_category_amount(category)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)
@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def stats_view(request):
    return render(request, 'expenses/stats.html')

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="expenses.csv"'

    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    # fetch expenses dinamically
    expenses=Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response


@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expenses.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Write the headers
    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Fetch and write data
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'category', 'date'
    )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response






