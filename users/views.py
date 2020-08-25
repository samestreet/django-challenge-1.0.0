from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):

	def create(self, validated_data):
		user = get_user_model().objects.create_user(**validated_data)
		return user

	class Meta:
		model = get_user_model()
		fields = ('username', 'password')

class UserView(APIView):

	permission_classes = (AllowAny,)

	def post(self, request):
		post_data = request.data
		serializer = UserSerializer(data=post_data)
		if serializer.is_valid(raise_exception=True):
			new_user = serializer.save()
			_user = get_user_model().objects.get(id=new_user.id)
			Token.objects.create(user=_user)
			return JsonResponse({'status':'Usuário criado com sucesso'}, safe=False)
		return HttpResponse('Usuário não foi criado')
