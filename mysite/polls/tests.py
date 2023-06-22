import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		was_publishied_recently() return False for questions whose
		pub_date is in the Future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_questions = Question(pub_date=time)
		self.assertIs(future_questions.was_publishied_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_publishied_recently() return False for question whose
		pub_date is old (days and more ago)
		"""
		time = timezone.now() - datetime.timedelta(days=1,seconds=1)
		old_questions = Question(pub_date=time)
		self.assertIs(old_questions.was_publishied_recently(), False)
	
	def test_was_published_recently_with_recent_question(self):
		"""
		was_publishied_recently() return True for question whose
		recently pub_date
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_questions = Question(pub_date=time)
		self.assertIs(recent_questions.was_publishied_recently(), True)
