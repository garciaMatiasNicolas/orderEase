from rest_framework.serializers import ModelSerializer
from .models import Users, UserInformation


class UserInformationSerializer(ModelSerializer):
    class Meta:
        model = UserInformation
        fields = ('first_name', 'last_name', 'dni', 'phone')


class UserSerializer(ModelSerializer):
    user_information = UserInformationSerializer()

    class Meta:
        model = Users
        exclude = ('created_at',)

    def create(self, validated_data):
        user_info_data = validated_data.pop('user_information', None)
        user = Users.objects.create_user(**validated_data)

        if user_info_data:
            UserInformation.objects.create(user=user, **user_info_data)

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_info_representation = representation.pop('user_information')
        representation.update(user_info_representation)
        return representation
