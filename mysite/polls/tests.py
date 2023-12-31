import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice


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
		pub_date is old (days and more ago).
		"""
		time = timezone.now() - datetime.timedelta(days=1,seconds=1)
		old_questions = Question(pub_date=time)
		self.assertIs(old_questions.was_publishied_recently(), False)
	
	def test_was_published_recently_with_recent_question(self):
		"""
		was_publishied_recently() return True for question whose
		recently pub_date.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_questions = Question(pub_date=time)
		self.assertIs(recent_questions.was_publishied_recently(), True)


def create_question(question_text, days):
	"""
	Create a question with the given `question_text` and published the
	given number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		"""
		If not questions exist, an appropriate message is displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		"""
		Question with a pub_date in the past are displayed on the index page.
		"""
		question = create_question(question_text="Past question.", days=-30)
		question.choice_set.create(choice_text="qq", votes=0)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question],
		)
	
	def test_future_question_and_past_question(self):
		"""
		Even if both past and future questions exist, only past questions
		are displayed.
		"""
		question1 = create_question(question_text="Past question.", days=-30)
		question1.choice_set.create(choice_text="qq", votes=0)
		question2 = create_question(question_text="Future question.", days=30)
		question2.choice_set.create(choice_text="qq", votes=0)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question1],
		)

	def test_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		question1 = create_question(question_text="Past question 1.", days=-30)
		question1.choice_set.create(choice_text="qq", votes=0)
		question2 = create_question(question_text="Past question 2.", days=-5)
		question2.choice_set.create(choice_text="qq", votes=0)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question2, question1],
		)

	def test_no_choices_question(self):
		"""
		If not choices exist for questioni, no polls avavilable.
		"""
		create_question(question_text="Some question.", days=-3)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
	
	def test_choices_question(self):
		"""
		If question have choices, question are displayed 
		"""
		question = create_question(question_text="Some question.", days=-3)
		question.choice_set.create(choice_text="qq", votes=0)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question],
		)


class QuestionDetaulViewTests(TestCase):
	def test_future_question(self):
		"""The detail view get status code 404 for the future question """
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
	
	def test_past_question(self):
		"""The detail view get question with past pub date """
		question = create_question(question_text="past", days=-33)
		response = self.client.get(reverse('polls:detail', args=(question.id, )))
		self.assertContains(response, question.question_text)
	

class QuestionResultsViewTest(TestCase):
	def test_future_question(self):
		"""The results view of a question with a pub_date in the future
        returns a 404 not found"""
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('polls:results', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
	
	def test_past_question(self):
		"""The results view get question with past pub date """
		question = create_question(question_text="past", days=-2)
		response = self.client.get(reverse('polls:results', args=(question.id, )))
		self.assertContains(response, question.question_text)