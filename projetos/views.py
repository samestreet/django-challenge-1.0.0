from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from navers.models import Naver, Projeto, NaverProjeto

class ProjetoView(APIView):

	permission_classes = (IsAuthenticated,)

	def get(self, request, projeto_id = 0):
		if projeto_id != 0:
			data = list(Projeto.objects.filter(id=projeto_id, user_id=request.user.id).values())
		else:
			data = list(Projeto.objects.filter(user_id=request.user.id).values())
		for d in data:
			navers = []
			nData = list(NaverProjeto.objects.filter(projeto_id=d['id']).values())
			for e in nData:
				p = list(Naver.objects.filter(id=e['naver_id_id']).values())
				if len(p):
					navers.append(p)
			d['navers'] = navers
		return JsonResponse(data, safe=False)

	def put(self, request, projeto_id):
		data = Projeto.objects.get(id=projeto_id)
		if 'name' in request.POST:
			data.name = request.POST['name']
		data.save()
		data = list(Projeto.objects.filter(id=projeto_id).values())
		for d in data:
			navers = []
			nData = list(NaverProjeto.objects.filter(projeto_id=d['id']).values())
			for e in nData:
				p = list(Projeto.objects.filter(id=e['id']).values())
				if len(p):
					navers.append(p)
			d['navers'] = navers
		return JsonResponse(data, safe=False)

	def post(self, request):
		data = Projeto()
		if 'name' in request.POST:
			data.name = request.POST['name']
		data.user_id = request.user.id
		data.save()
		last = Projeto.objects.last().id
		data = list(Projeto.objects.filter(id=last).values())
		return JsonResponse(data, safe=False)

	def delete(self, request, projeto_id):
		data = Projeto.objects.get(id=projeto_id, user_id=request.user.id)
		data.delete()
		return HttpResponse('deleted')