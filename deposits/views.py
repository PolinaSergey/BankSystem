# from django.shortcuts import render, redirect
# from .models import Deposit
# from django.http import HttpResponse
# from django.contrib import messages
#
#
# def skip_day(request):
#     for deposit in Deposit.objects.all():
#         deposit.increment_balance()
#     messages.success(request, 'Day skipped')
#     return redirect(request.META['HTTP_REFERER'])
#
# def skip_month(request):
#     for deposit in Deposit.objects.all():
#         deposit.increment_balance(30)
#     messages.success(request, 'Month skipped')
#     return redirect(request.META['HTTP_REFERER'])
#
# def revoke(request):
#     for deposit in Deposit.objects.all():
#         deposit.revoke()
#     messages.success(request, 'Revoked!')
#     return redirect(request.META['HTTP_REFERER'])
#
