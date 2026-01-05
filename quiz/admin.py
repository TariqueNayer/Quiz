from django.contrib import admin
from .models import (Category, Question)

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
	list_display = [
		'text',
		'answer',
		'category',
	]
admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)