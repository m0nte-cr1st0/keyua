from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from project.blog.models import Category, Article, Author, Vote


class VotingTest(TestCase):

	def setUp(self):
		self.c = Client()

	def test_voting(self):
		author = Author.objects.create(linkedin_url='author', background='image.img')
		article = Article.objects.create(url='article_test', title='article_title', contents='article_text', author_id=1)

		# open page with article
		self.c.get('/blog/article_test/')
		response = self.c.get('/blog/article_test/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# send two post request from same IP
		self.c.post(('/blog/article_test/'), {'rating': 5}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'REMOTE_ADDR':'127.0.0.1'})
		self.c.post(('/blog/article_test/'), {'rating': 4}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'REMOTE_ADDR':'127.0.0.1'})
		vote = Vote.objects.all().first()

		# check allow dublicate of voting from same IP
		self.assertEqual(Vote.objects.all().count(), 1)
		self.assertEqual(vote.rating, 5)
		
		# send post request from another IP
		self.c.post(('/blog/article_test/'), {'rating': 3}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 'REMOTE_ADDR':'127.0.0.2'})
		self.assertEqual(Vote.objects.all().count(), 2)
		self.assertEqual(article.vote_status('127.0.0.1').get('avg_rating'), 4)
		self.assertEqual(article.vote_status('127.0.0.2').get('voted'), 3)
