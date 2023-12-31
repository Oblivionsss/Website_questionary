from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		all_question = Question.objects.filter(
			pub_date__lte=timezone.now()
			).exclude(choice=None).order_by('-pub_date')[:5]
		return all_question

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""Return recently question."""
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	
	def get_queryset(self):
		"""Return recently question."""
		return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You didn\'t select a choice',
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResposeRedirect after succesfully dealing
		# with POST data. This prevent data from being posted twice if a
		# user hits the Back button
		return HttpResponseRedirect(reverse(
			'polls:results', 
			args=(question.id,))
			)



