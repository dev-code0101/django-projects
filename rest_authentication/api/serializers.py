from rest_framework import serializers
from .models import Person

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PersonSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = '__all__'

	def validate(self , data):
		if data['age'] < 18:
			raise serializers.ValidationError('')
		return data

	def validate_age(self, data):
		return data

class RegisterSerializer(serializers.Serializer):

	username = serializers.CharField()
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):

		if data['username']:
			if User.objects.filter(username = data['username']).exists():
				raise serializers.ValidationError('Username taken')

		if data['email']:
			if User.objects.filter(email= data['email']).exists():
				raise serializers.ValidationError('Email taken')
		return data

	def create(self, validated_data):
		data = validated_data
		user = User.objects.create(username=data['username'], email=data['email'])
		user.set_password(data['password'])
		user.save()
		Token.objects.get_or_create(user=user)
		return data

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()