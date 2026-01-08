from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model() # For UserScore.

# Create your models here.
class Category(models.Model):
	id = models.UUIDField( 
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	name = models.CharField(max_length=100)

	description = models.CharField(max_length=200, blank=True)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

class Question(models.Model):
	text = models.CharField(max_length=500)
	answer = models.TextField()
	option_a = models.TextField(blank=True)
	option_b = models.TextField(blank=True)
	option_c = models.TextField(blank=True)
	option_d = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

class UserScore(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="category_scores"
	)
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		related_name="user_scores"
	)
	highest_score = models.PositiveIntegerField(default=0)
	total_questions = models.PositiveIntegerField(default=0)
	last_attempted = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("user", "category")
		ordering = ["-highest_score"]

	def __str__(self):
		return f"{self.user} - {self.category} : {self.highest_score}"

