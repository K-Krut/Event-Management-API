from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User
from users.utils import convert_file


class UserRegisterSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    avatar = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'email_notifications', 'avatar_url', 'password', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'write_only': True},
            'id': {'read_only': True}
        }

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=convert_file(validated_data.get('avatar', None))
        )

        return user
