from django.views.generic import ListView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.db.models import Q

from .models import (Category, Question, UserScore)
from .forms import CategoryQuizForm

# Create your views here.
@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60), 'dispatch')
class HomeView(TemplateView):
	template_name = 'quiz/home.html'

@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60), 'dispatch')
class AboutView(TemplateView):
	template_name = 'quiz/about.html'
@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60), 'dispatch')
class QuizListView(LoginRequiredMixin, ListView):
	model = Category
	context_object_name = 'Category_list'
	template_name = 'quiz/quiz_list.html'
	login_url = "account_login"
	
@method_decorator(vary_on_cookie, name='dispatch')
@method_decorator(cache_page(60), 'dispatch')
class QuizView(LoginRequiredMixin, FormView):
	template_name = "quiz/category_quiz.html"
	form_class = CategoryQuizForm
	login_url = "account_login"

	def dispatch(self, request, *args, **kwargs):
		
		self.category = get_object_or_404(
			Category,
			id=self.kwargs["category_id"]
		)
		return super().dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["questions"] = Question.objects.filter(category=self.category)
		return kwargs
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["category"] = self.category
		return context


	def form_valid(self, form):
		score = 0
		total = 0
		results = []

		for field_name, user_answer in form.cleaned_data.items():
			question_id = field_name.split("_")[1]
			question = Question.objects.get(id=question_id)

			total += 1
			

			# subjective question
			if not any([
				question.option_a,
				question.option_b,
				question.option_c,
				question.option_d,
			]):
				# simple comparison 
				if user_answer.strip().lower() == question.answer.strip().lower():
					score += 1
					is_correct = True
				else: is_correct = False

			# MCQ question
			else:
				if user_answer.strip().lower() == question.answer.strip().lower():
					score += 1
					is_correct = True
				else: is_correct = False

			results.append({
				"id" : question_id,
				"question": question.text,
				"user_answer": user_answer,
				"correct_answer": question.answer,
				"is_correct": is_correct,
			})

		self.request.session["score"] = score
		self.request.session["total"] = total
		self.request.session["results"] = results

		# store / update highest score
		score_obj, created = UserScore.objects.get_or_create(
			user=self.request.user,
			category=self.category,
			defaults={"highest_score": score, "total_questions": total},
		)

		if not created and score > score_obj.highest_score:
			score_obj.highest_score = score
			score_obj.total_questions = total
			score_obj.save()

		return super().form_valid(form)


	def get_success_url(self):
		return "/quiz/result/"

class QuizResultView(LoginRequiredMixin, TemplateView):
	template_name = "quiz/result.html"
	login_url = "account_login"

	def dispatch(self, request, *args, **kwargs):
		if "score" not in request.session:
			return redirect("quiz_list")
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if "score" not in self.request.session:
			return context
		context["score"] = self.request.session.get("score")
		context["total"] = self.request.session.get("total")
		context["half_total"] = self.request.session.get("total") / 2
		context["category"] = self.request.session.get("category")
		context["results"] = self.request.session["results"]
		return context

class SearchCategoryView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'quiz/quiz_list.html'
	context_object_name = 'Category_list'
	login_url = "account_login"

	def get_queryset(self):
		query = self.request.GET.get('q')
		return Category.objects.filter( Q(name__icontains=query) | Q(description__icontains=query) )