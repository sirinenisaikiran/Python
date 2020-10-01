from django.test import TestCase

# Create your tests here.
import datetime
from django.test import Client
from books.models import Book

class BookTests(TestCase):

    def setUp(self):
        # django uses separate table test_books in DB  and removes after test
        # hence populate few data in that else test would fail
        Book.objects.create(name="first book", pub_date=datetime.date.today())
        Book.objects.create(name="first book 12", pub_date=datetime.date.today())
        self.c =  Client()

		
    def test_sample(self):
        """First test case"""
        response = self.c.get('http://127.0.0.1:8000/latest/')
        # we can call unittest methods
        self.assertRegexpMatches(response.content.decode('ascii'), "first book")
        

    def test_not_empty(self):
        """Second Test case"""
        book_list = Book.objects.order_by('-pub_date')
        # we can call unittest methods
        self.assertTrue(book_list)