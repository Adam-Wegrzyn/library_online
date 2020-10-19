from django.test import TestCase
from django.urls import reverse
from library.models import Book
from library.forms import Book_add
from django.contrib import auth
from django.contrib.auth import get_user_model



class LibraryTest(TestCase):

    def create_book(self, title='Harry Potter i Kamien Filozoficzny', author='J.K Rowling', date_of_public='1995-12-11', isbn=232132, page_count=300, cover_link='https://ecsmedia.pl/c/harry-potter-i-kamien-filozoficzny-tom-1-w-iext43794838.jpg)', lang='Polish'):
        return Book.objects.create(title=title, author=author,date_of_public=date_of_public, isbn=isbn, page_count=page_count, cover_link=cover_link, lang=lang)

    def setUp(self, username='User', password='Temp123#'):
        User = get_user_model()
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        # self.client.force_login(user)

    def test_login_view(self):

        self.client.login(username='User', password='Temp123#')
        url=reverse('login')
        response = self.client.post(url, {'username':'User', 'password': 'Temp123#'}, follow=True)
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_authenticated)


    def test_index_view(self):
        url=reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

    def test_my_books_view(self):
        user = auth.get_user(self.client)
        if user.is_authenticated:
            url=reverse('my_books')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_add_book_view(self):
        url=reverse('add_book')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_book(self):
        book = self.create_book()
        url=reverse('edit_book', args=(1,))
        book.page_count=500
        book.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.page_count,500)

    def test_import_book_view(self):
        self.client.login(username='User', password='Temp123#')
        url=reverse('import_book')
        response = self.client.get(url, {'keywords': 'harry potter'})
        # response_post= self.client.post()
        self.assertEqual(response.status_code, 200)
        #get first found record and save it
        book_data = response.context['data'][0]['volumeInfo']
        book_data = {'title': book_data['title'], 'author': book_data['authors'][0],'date_of_public':book_data['publishedDate'], 'isbn': book_data['industryIdentifiers'][1]['identifier'], 'page_count': book_data['pageCount'], 'cover_link': book_data['imageLinks']['smallThumbnail'], 'lang': book_data['language']}
        response_post = self.client.post(url, book_data)
        added_book = Book.objects.get(id=1)

        #is book added properly
        self.assertEqual(added_book.title, book_data['title'])
        self.assertEqual(response_post.status_code, 200)

    def test_book_add_form_vaild(self):

        data = {
            'title': 'The Witcher',
            'author': 'Andrzej Sapkowski',
            'date_of_public': '1999-03-04',
            'isbn': 1473232422,
            'page_count': 300,
            'cover_link': 'http://www.google.pl',
            'lang': 'EN'
        }
        form = Book_add(data)
        self.assertTrue(form.is_valid())


    def test_book_add_form_not_vaild(self):

        data = {
            'title': 'The Witcher',
            'author': 'Andrzej Sapkowski',
            'date_of_public': '1999-03-04',
            'isbn': 1473232422,
            'page_count': 300,
            'cover_link': 'invalid link',
            'lang': 'EN'
        }
        form = Book_add(data)
        self.assertFalse(form.is_valid())



