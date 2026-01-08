from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from quiz.models import UserScore

# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scores"] = (
            UserScore.objects
            .filter(user=self.request.user)
            .select_related("category")
        )
        return context



