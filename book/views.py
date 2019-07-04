import io, datetime, re
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from .models import BookType, Book, UserProfileInfo, RentalBook, Returns
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.db.models import Sum, Count
from django.views.decorators.cache import cache_page
from django.conf import settings
# import testproject.settings
# Create your views here.


def index(request):
    books = Book.objects.all().prefetch_related("book_type")
    return render(request,'book/index.html', { "books" : books })
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'book/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'book/login.html', {})



@cache_page(1800)
def rental(request):
    if request.method == 'POST':
        max_book = 5
        user = request.user
        book = Book.objects.get(pk=request.POST.get('book_id'))
        quantity = request.POST.get('quantity')
        rent = RentalBook(book=book, user_id=user, amount=quantity)
        rent.save()
        rental_number = RentalBook.objects.filter(user_id=user).aggregate(Sum('amount'))
        
        if rental_number['amount__sum'] > max_book:
            delt = RentalBook.objects.filter(book=book, user_id=user, amount=quantity).latest('id')
            delt.delete()
            messages.success(request, "Your book's quantity is not over 5. Rental again or return book.")
            return HttpResponseRedirect(reverse('index'))
        else:
            amount = Book.objects.filter(book_name=book.book_name).values_list('amount',flat=True)[0]
            current_amount = int(amount)-int(quantity)
            Book.objects.filter(book_name=book.book_name).update(amount=current_amount)
            messages.success(request,"You rented successfully.")
            # ren_amnt = RentalBook.objects.filter(book=book, user_id=user).aggregate(Sum('amount'))
            # r = ren_amnt['amount__sum']
            return HttpResponseRedirect(reverse('index'))
            # return render('book/index.html', {'r': r})



def return_book(request):
    if request.method == 'POST':
        user = request.user
        book = Book.objects.get(pk=request.POST.get('book_id'))
        quantity = request.POST.get('quantity')
        ret = Returns(book=book, user_id=user, amount=quantity, returndate=timezone.now())
        ret.save()
        amount = Book.objects.filter(book_name=book.book_name).values_list('amount',flat=True)[0]
        ren_amnt = RentalBook.objects.filter(book=book, user_id=user).aggregate(Sum('amount'))
        # r = ren_amnt['amount__sum']
        if int(quantity) > ren_amnt['amount__sum']:
            delt = Returns.objects.filter(book=book, user_id=user, amount=quantity).latest('id')
            delt.delete()
            messages.success(request, "You can not return more than rental.")
            return HttpResponseRedirect(reverse('index'))
        else:
            current_amount = int(amount)+int(quantity)
            Book.objects.filter(book_name=book.book_name).update(amount=current_amount)
            ren_crr_amnt = int(ren_amnt['amount__sum'])-int(quantity)
            RentalBook.objects.filter(book=book, user_id=user).delete()
            RentalBook(book=book, user_id=user, amount=ren_crr_amnt).save()
            messages.success(request, "You returned book successfully.")
            return HttpResponseRedirect(reverse('index'))
            # return render('book/index.html', {'r': r})


# def display(request):
#     user = request.user
#     book = Book.objects.get(pk=request.POST.get('book_id'))    
#     ren_amnt = RentalBook.objects.filter(book=book, user_id=user).aggregate(Sum('amount'))
#     template = loader.get_template('book/index.html')
#     r = ren_amnt['amount__sum']
#         # return HttpResponseRedirect(reverse('index'))
#     return render(request, 'book/index.html', {'r': r})
class BookList(generic.DetailView):
    model = Book
    template = 'book/index.html'
    def display(request):
        user = request.user
        book = Book.objects.get(pk=request.POST.get('book_id'))    
        ren_amnt = RentalBook.objects.filter(book=book, user_id=user).aggregate(Sum('amount'))
        template = loader.get_template('book/index.html')
        r = ren_amnt['amount__sum']
        # return HttpResponseRedirect(reverse('index'))
        return render(request, template , {'r': r})