from django.shortcuts import render

#for view expense
def index(request):
    return render(request, 'expenses/index.html')

# for add expense
def add_expense(request):
    return render(request, 'expenses/add_expense.html')
