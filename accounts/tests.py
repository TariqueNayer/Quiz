from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
class UserTest(TestCase):
	def test_create_user(self):
		User = get_user_model()
		user = User.objects.create_user(
			username='mytestuser',
			email='mytestuser@email.com',
			password='testpass@1234',
		)

		self.assertEqual(user.username,'mytestuser')
		self.assertEqual(user.email, 'mytestuser@email.com')
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

	def test_create_superuser(self):
		User = get_user_model()
		user = User.objects.create_superuser(
			username='mytestsuperuser',
			email='mytestsuperuser@email.com',
			password='testsuperpass@1234',
		)

		self.assertEqual(user.username,'mytestsuperuser')
		self.assertEqual(user.email, 'mytestsuperuser@email.com')
		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)