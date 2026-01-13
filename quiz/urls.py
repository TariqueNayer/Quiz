from django.urls import path
from .views import HomeView, AboutView, QuizListView, QuizView, QuizResultView, SearchCategoryView

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('about/', AboutView.as_view(), name='about'),

	path('quiz/list/', QuizListView.as_view(), name='quiz_list'),
	path('quiz/<uuid:category_id>/', QuizView.as_view(), name='quiz'),
	path('quiz/result/', QuizResultView.as_view(), name='result'),
	path('search/', SearchCategoryView.as_view(), name='search_results')
]