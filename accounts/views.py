from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from quiz.models import UserScore
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = "account/profile.html"
	login_url = "account_login"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["scores"] = (
			UserScore.objects
			.filter(user=self.request.user)
			.select_related("category")
		)
		return context

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
	login_url = "account_login"
	# This will be the landing page after a successful change
	def get_success_url(self):
		# Setting a flag in the session that expires quickly
		self.request.session['password_changed_successfully'] = True
		return reverse_lazy('password_change_done') 

class PasswordChangeDone(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	template_name = 'account/password_change_done.html'
	login_url = "account_login"

	def test_func(self):
		# Only allow access if this session flag exists
		return self.request.session.get('password_changed_successfully', False)

	def handle_no_permission(self):
		# Redirect users who try to access the URL directly
		return redirect('account_change_password')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Clean up: remove the flag so they can't refresh or revisit later
		if 'password_changed_successfully' in self.request.session:
			del self.request.session['password_changed_successfully']
		return context