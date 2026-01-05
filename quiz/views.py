from django.views.generic import ListView, TemplateView, FormView
from django.shortcuts import get_object_or_404

from .models import Category, Question
from .forms import CategoryQuizForm

# Create your views here.
class HomeView(TemplateView):
	template_name = 'quiz/home.html'

class AboutView(TemplateView):
	template_name = 'quiz/about.html'

class QuizListView(ListView):
	model = Category
	context_object_name = 'Category_list'
	template_name = 'quiz/quiz_list.html'

class QuizView(FormView):
	template_name = "quiz/category_quiz.html"
	form_class = CategoryQuizForm

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

			# MCQ question
			else:
				if user_answer.lower() == question.answer.lower():
					score += 1

		self.request.session["score"] = score
		self.request.session["total"] = total

		return super().form_valid(form)


	def get_success_url(self):
		return "/quiz/result/"

class QuizResultView(TemplateView):
	template_name = "quiz/result.html"

	def get_context_data(self, **kwargs):
		if "score" not in self.request.session:
			return redirect("category_list")
		else:
			context = super().get_context_data(**kwargs)
			context["score"] = self.request.session.get("score")
			context["total"] = self.request.session.get("total")
			context["category"] = self.request.session.get("category")
			return context