from django.db import models

class Naver(models.Model):
	name = models.CharField(max_length=48)
	birthdate = models.DateTimeField()
	admission_date = models.DateTimeField()
	job_role = models.CharField(max_length=48)
	user_id = models.IntegerField(default=0)
	def __str__(self):
		return self.name

class Projeto(models.Model):
	name = models.CharField(max_length=48)
	user_id = models.IntegerField(default=1)
	def __str__(self):
		return self.name

class NaverProjeto(models.Model):
	naver_id = models.ForeignKey(Naver, on_delete=models.CASCADE)
	projeto_id = models.ForeignKey(Projeto, on_delete=models.CASCADE)
	def __str__(self):
		return self.naver_id.name + ' / ' + self.projeto_id.name