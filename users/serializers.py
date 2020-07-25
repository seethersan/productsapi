from rest_framework import serializers

from users.models import User, Profession


class UserSerializer(serializers.ModelSerializer):
    """ Used to retrieve user info """
    professions = serializers.PrimaryKeyRelatedField(queryset=Profession.objects.all(), many=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'professions': {'required': False}}

class ProfessionSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Profession
        fields = ('id', 'name', 'users')