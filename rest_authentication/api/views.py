from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer, RegisterSerializer, LoginSerializer

from rest_framework.views import APIView

from rest_framework import generics
from rest_framework import mixins

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from rest_framework import viewsets, status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def index(request):
	courses = {
		'courses': ['flask', 'django', 'FastApi']
	}
	return Response(courses)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):

	if request.method == 'GET':
		ppl = Person.objects.all()
		serializer = PersonSerializer(ppl, many = True)

	elif request.method == 'POST':
		serializer = PersonSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
		else:
			return Response(serializer.errors)

	elif request.method == 'PUT':
		serializer = PersonSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
		else:
			return Response(serializer.errors)

	elif request.method == 'PATCH':
		data = request.data
		obj = Person.objects.get(id=data['id'])
		#extract id from request
		serializer = PersonSerializer(obj, data = data, partial = True)
		if serializer.is_valid():
			serializer.save()
		else:
			return Response(serializer.errors)

	else:
		id = request.data['id']
		obj = Person.objects.get(id=id)
		obj.delete()
		return Response({"message": f'ID: {id} deleted'})

	return Response(serializer.data)


class PersonAPIView(APIView):

	def get(self, request):
		pass

	def post(self, request):
		pass

class GenericPerson(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
					mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

	serializer_class = PersonSerializer

	queryset = Person.objects.all()

	authentication_classes = [TokenAuthentication]

	permission_classes = [IsAuthenticated]

	def get(self, request):
		return self.list(request)

	lookup_field = 'id'

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)

	def post(self, request,id):
		return self.create(request)

	def put(self, request, id=None):
		return self.update(request, id)

	def delete(self, request, id):
		return self.destroy(request, id)

class PersonViewset(viewsets.ModelViewSet):

	serializer_class = PersonSerializer
	queryset = Person.objects.all()

	def list(self, request):
		search = request.GET.get('search')
		qs = self.queryset

		if search:
			qs = qs.filter(name__startswith = search)

		serializer = PersonSerializer(qs, many = True)
		return Response({'status':200
						,'data'  :serializer.data})

class RegisterAPI(APIView):

	def post(self, request):
		data = request.data
		serializer = RegisterSerializer(data = data)

		if not serializer.is_valid():
			return Response({ 'message' : serializer.errors },
							status=status.HTTP_400_BAD_REQUEST )

		serializer.save()

		return Response({ 'message':"User Created" }, status= status.HTTP_200_OK)

class LoginAPI(APIView):

	def post(self, request):
		username = request.data['username']
		password = request.data['password']

		user = authenticate(request,username=username,password=password)
		print(user)
		if not user:
			return Response({ 'message' : 'HTTP_401_UNAUTHORIZED' },
							status=status.HTTP_401_UNAUTHORIZED )

		token = Token.objects.get(user=user)
		print(token)

		return Response({ 'message':"User Logged in",'token':token.key}, status= status.HTTP_200_OK)