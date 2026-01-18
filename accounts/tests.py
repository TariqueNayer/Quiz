from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quiz.models import UserScore, Category

User = get_user_model()

# Create your tests here.
class UserTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='mytestuser',
			email='mytestuser@email.com',
			password='testpass@1234',
		)
		self.superuser = User.objects.create_superuser(
			username='mytestsuperuser',
			email='mytestsuperuser@email.com',
			password='testsuperpass@1234',
		)
	def test_create_user(self):

		self.assertEqual(self.user.username,'mytestuser')
		self.assertEqual(self.user.email, 'mytestuser@email.com')
		self.assertTrue(self.user.is_active)
		self.assertFalse(self.user.is_staff)
		self.assertFalse(self.user.is_superuser)

	def test_create_superuser(self):
	

		self.assertEqual(self.superuser.username,'mytestsuperuser')
		self.assertEqual(self.superuser.email, 'mytestsuperuser@email.com')
		self.assertTrue(self.superuser.is_active)
		self.assertTrue(self.superuser.is_staff)
		self.assertTrue(self.superuser.is_superuser)

class ProfileViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='profileuser', 
			email='profileuser0@gmail.com',
			password='profileuserpass@1234',
		)
		self.cat = Category.objects.create(name="Python")
		self.score = UserScore.objects.create(
			user= self.user,
			category= self.cat,
			highest_score=8,
			total_questions=10,
		)
		self.url = reverse('profile')

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(self.url)
		self.assertRedirects(
			response,
			f"{reverse('account_login')}?next={self.url}"
		)

	def test_profile_view_logged_in(self):
		self.client.login(username="profileuser", password="profileuserpass@1234")
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "account/profile.html")
		self.assertIn("scores", response.context)
		self.assertContains(response, self.user.username)

	def test_profile_view_shows_only_user_scores(self):
		other_user = User.objects.create_user(
			username="other",
			password="pass1234"
		)
		UserScore.objects.create(
			user=other_user,
			category=self.cat,
			highest_score=5,
			total_questions=10,
		)

		self.client.login(username="profileuser", password="profileuserpass@1234")
		response = self.client.get(self.url)

		scores = response.context["scores"]
		self.assertEqual(scores.count(), 1)
		self.assertEqual(scores.first(), self.score)

		self.assertNotContains(response, other_user.username)

