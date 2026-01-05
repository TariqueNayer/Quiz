from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import HomeView, AboutView
from quiz.models import Category, Question

# Create your tests here.
class HomePageTests(SimpleTestCase):
	def setUp(self):
		url= reverse('home')
		self.response = self.client.get(url)

	def test_url_exist_at_correct_location(self):
		self.assertEqual(self.response.status_code, 200)

	def test_correct_template_used(self):
		self.assertTemplateUsed(self.response, 'quiz/home.html')

	def test_template_contains_correct_html(self):
		self.assertContains(self.response, 'Home')

	def test_template_does_not_contains_incorrect_html(self):
		self.assertNotContains(self.response, 'About')

	def test_homepage_url_resolves_homepageview(self):
		view = resolve("/")
		self.assertEqual(view.func.__name__, HomeView.as_view().__name__)

class AboutPageTests(SimpleTestCase):
	def setUp(self):
		url= reverse('about')
		self.response = self.client.get(url)

	def test_url_exist_at_correct_location(self):
		self.assertEqual(self.response.status_code, 200)

	def test_correct_template_used(self):
		self.assertTemplateUsed(self.response, 'quiz/about.html')

	def test_template_contains_correct_html(self):
		self.assertContains(self.response, 'About')

	def test_template_does_not_contains_incorrect_html(self):
		self.assertNotContains(self.response, 'Home')

	def test_homepage_url_resolves_homepageview(self):
		view = resolve("/about/")
		self.assertEqual(view.func.__name__, AboutView.as_view().__name__)

class QuizListViewTest(TestCase):
	def setUp(self):
		self.category1 = Category.objects.create(name="Python")
		self.category2 = Category.objects.create(name="Django")

	def test_quiz_list_view_status_code(self):
		response = self.client.get(reverse("quiz_list"))
		self.assertEqual(response.status_code, 200)

	def test_quiz_list_view_template_used(self):
		response = self.client.get(reverse("quiz_list"))
		self.assertTemplateUsed(response, "quiz/quiz_list.html")

	def test_quiz_list_view_context(self):
		response = self.client.get(reverse("quiz_list"))
		self.assertIn("Category_list", response.context)

class QuizViewGETTest(TestCase):
	def setUp(self):
		self.category = Category.objects.create(name="Python")

		self.question = Question.objects.create(
			category=self.category,
			text="What is Python?",
			answer="language"
		)
		self.response = self.client.get(
			reverse("quiz", kwargs={"category_id": self.category.id})
		)

	def test_quiz_view_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_quiz_view_template_used(self):
		self.assertTemplateUsed(self.response, "quiz/category_quiz.html")

	def test_quiz_view_context_contains_category(self):
		self.assertEqual(self.response.context["category"], self.category)

class QuizViewPOSTTest(TestCase):
	def setUp(self):
		self.category = Category.objects.create(name="Python")

		self.question = Question.objects.create(
			category=self.category,
			text="What is Python?",
			answer="Language",
			option_a="",
			option_b="",
			option_c="",
			option_d=""
		)

	def test_quiz_view_post_subjective_correct_answer(self):
		post_data = {
			f"question_{self.question.id}": "language"
		}

		response = self.client.post(
			reverse("quiz", kwargs={"category_id": self.category.id}),
			data=post_data,
			follow=True
		)

		session = self.client.session
		self.assertEqual(session["score"], 1)
		self.assertEqual(session["total"], 1)

	def test_quiz_view_post_mcq_correct_answer(self):
		mcq = Question.objects.create(
			category=self.category,
			text="Capital of France?",
			option_a="Paris",
			option_b="London",
			option_c="Berlin",
			option_d="Rome",
			answer="a"
		)

		post_data = {
			f"question_{mcq.id}": "a"
		}

		response = self.client.post(
			reverse("quiz", kwargs={"category_id": self.category.id}),
			data=post_data,
			follow=True
		)

		session = self.client.session
		self.assertEqual(session["score"], 1)
		self.assertEqual(session["total"], 1)

