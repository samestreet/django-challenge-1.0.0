from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Naver, Projeto, NaverProjeto
from django.views.decorators.csrf import csrf_exempt

class NaverView(APIView):

	permission_classes = (IsAuthenticated,)

	def get(self, request, naver_id = 0):
		if naver_id != 0:
			data = list(Naver.objects.filter(id=naver_id, user_id=request.user.id).values())
		else:
			data = list(Naver.objects.filter(user_id=request.user.id).values())
		for d in data:
			projetos = []
			nData = list(NaverProjeto.objects.filter(naver_id=d['id']).values())
			for e in nData:
				p = list(Projeto.objects.filter(id=e['projeto_id_id']).values())
				if len(p):
					projetos.append(p[0])
			d['projetos'] = projetos
		return JsonResponse(data, safe=False)

	def put(self, request, naver_id):
		data = Naver.objects.get(id=naver_id)
		if 'name' in request.POST:
			data.name = request.POST['name']
		if 'birthdate' in request.POST:
			data.birthdate = request.POST['birthdate']
		if 'admission_date' in request.POST:
			data.admission_date = request.POST['admission_date']
		if 'job_role' in request.POST:
			data.job_role = request.POST['job_role']
		data.save()
		data = list(Naver.objects.filter(id=naver_id).values())
		for d in data:
			projetos = []
			nData = list(NaverProjeto.objects.filter(naver_id=d['id']).values())
			for e in nData:
				p = list(Projeto.objects.filter(id=e['projeto_id_id']).values())
				if len(p):
					projetos.append(p[0])
			d['projetos'] = projetos
		return JsonResponse(data, safe=False)

	def post(self, request):
		data = Naver()
		if 'name' in request.POST:
			data.name = request.POST['name']
		if 'birthdate' in request.POST:
			data.birthdate = request.POST['birthdate']
		if 'admission_date' in request.POST:
			data.admission_date = request.POST['admission_date']
		if 'job_role' in request.POST:
			data.job_role = request.POST['job_role']
		data.user_id = request.user.id
		data.save()
		last = Naver.objects.last().id
		data = list(Naver.objects.filter(id=last).values())
		return JsonResponse(data, safe=False)

	def delete(self, request, naver_id):
		data = Naver.objects.get(id=naver_id, user_id=request.user.id)
		data.delete()
		return HttpResponse('deleted')

@csrf_exempt
def addProjeto(request):
	if request.method != 'POST':
		return JsonResponse({'error' : 'Método ' + request.method + ' não é permitido'}, safe=False)
	data = NaverProjeto()
	naver_id = request.POST['naver']
	projeto_id = request.POST['projeto']
	naver = Naver.objects.get(id=naver_id)
	projeto = Projeto.objects.get(id=projeto_id)
	data.naver_id = naver
	data.projeto_id = projeto
	data.save()
	last = NaverProjeto.objects.last().id
	data = list(NaverProjeto.objects.filter(id=last).values())
	return JsonResponse(data, safe=False)