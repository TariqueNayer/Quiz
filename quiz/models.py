from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)

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

