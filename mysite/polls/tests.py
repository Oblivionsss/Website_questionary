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

