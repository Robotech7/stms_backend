from django.contrib.auth import password_validation, get_user_model
from rest_framework import serializers

from .models import ProviderProfile


class UserCreateSerializers(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user_model = get_user_model()
        user = user_model(username=username,
                          email=email,
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Пользователь с таким email адресом существует')
        return value

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'first_name': {'required': True, 'trim_whitespace': True},
                        'last_name': {'required': True, 'trim_whitespace': True},
                        'email': {'required': True, 'trim_whitespace': True}}


class UserProfileSerializers(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'groups', 'last_login', 'avatar')
        read_only_fields = ['username', 'groups', 'last_login']


class ProviderProfileSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    user = UserProfileSerializers(read_only=True)

    class Meta:
        model = ProviderProfile
        exclude = ('id',)


class UserPasswordChangeSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=50)
    new_password = serializers.CharField(required=True, max_length=50)
    new_password_confirm = serializers.CharField(required=True, max_length=50)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
