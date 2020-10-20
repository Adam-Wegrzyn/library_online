from django.shortcuts import render
from django.contrib import messages
from .forms import Book_add
from .models import Book
from .filters import BookFilter
import requests
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from datetime import datetime as dt
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request,'library/index.html')


def my_books(request):
    books = request.user.book.all()
    books_filter = BookFilter(request.GET, queryset=books)

    context = {
        # 'books': books,
        'books_filter': books_filter
    }
    return render(request, 'library/my_books.html', context)

def delete_book(request, book_pk):
        book_to_del = Book.objects.get(pk =book_pk)
        book_to_del.delete()

        return HttpResponseRedirect(reverse('my_books'))

def add_book(request):
    form = Book_add
    books = Book.objects.all()

    if request.method == 'POST':
        form = Book_add(request.POST)
        # request.user.book.add(form)
        if form.is_valid():
            data = form.cleaned_data
            new_book = Book(title=data['title'], author=data['author'], date_of_public=data['date_of_public'], isbn=data['isbn'], page_count=data['page_count'], cover_link=data['cover_link'], lang=data['lang'])
            new_book.save()
            request.user.book.add(new_book)

            messages.success(request, 'New book has been successfully added to your library!')
        else:
            print('not valid')
            print(form.errors)
    context = {
        'form': form,
        'books': books
    }
    return render(request, 'library/add_book.html', context)



def edit_book(request, book_pk):
    book_instance = Book.objects.get(pk=book_pk)
    form = Book_add(instance=book_instance)
    if request.method == 'POST':
        form = Book_add(request.POST, instance=book_instance)

        if form.is_valid():
            form.save()
            form = Book_add()
            request.user.book.add(book_instance)
            print(book_instance)
            messages.success(request, 'Book has been successfully edited!')
        else:
            print('not valid', form.errors)

    context = {
        'form': form
    }
    return render(request, 'library/edit_book.html', context)

def import_book(request):
    form = Book_add
    # get keywords from search bar for API
    keywords = ''
    if request.method =='GET':

        if request.GET.get('keywords',''):
            # format keywords for query string parameters
            keywords = '+'.join(request.GET['keywords'].split(' '))

    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {

        'q': keywords
    }

    if request.method == 'POST':
        updated_request = request.POST.copy()
        date_of_public = str(request.POST['date_of_public'])
        # some books from API have only year, adding day and month for proper date format
        if len(date_of_public) == 4:
            date_of_public = dt.strptime(date_of_public + '-01-01', '%Y-%m-%d')
        updated_request['date_of_public'] = date_of_public
        form = Book_add(updated_request)

        if form.is_valid():
            data = form.cleaned_data

            new_book = Book(title=data['title'], author=data['author'], date_of_public=data['date_of_public'],
                            isbn=data['isbn'], page_count=data['page_count'], cover_link=data['cover_link'],
                            lang=data['lang'])
            new_book.save()

            #relate logged user to the book instance
            request.user.book.add(new_book)
            messages.success(request, 'New book has been successfully added to your library!')
    response = (requests.get(url, params))
    data = response.json()

    #get needed value (list) from 'items' key in json response
    data = data.get('items', '')
    context = {
        'form': form,
        'data': data
    }

    return render(request, 'library/import_book.html', context)


#API view
#url = /api
class LibraryApi(viewsets.ModelViewSet):

        queryset = Book.objects.all()
        serializer_class = BookSerializer
        filter_fields = '__all__'
        permission_classes= (IsAuthenticated,)


