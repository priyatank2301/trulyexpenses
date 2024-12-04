from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense,name="add-expense"),
    path('edit-expense/<int:id>',views.edit_expense,name="edit-expense"),
    path('delete-expense/<int:id>',views.delete_expense,name="delete-expense"),
    path('search-expenses', csrf_exempt(views.search_expenses),name="search-expenses"),
    path('expense-category-summary', csrf_exempt(views.expense_category_summary),name="expense_category_summary"),
    path('stats', csrf_exempt(views.stats_view),name="stats"),
    path('export-csv', csrf_exempt(views.export_csv),name="export-csv"),
    path('export-excel', csrf_exempt(views.export_excel),name="export-excel"),
   
]