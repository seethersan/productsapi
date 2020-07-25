from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer, ProfessionSerializer
from users.models import Profession, User

class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        User profile
        Get profile of current logged in user.
        """
        return self.retrieve(request, *args, **kwargs)

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all().order_by('id')
    serializer_class = ProfessionSerializer

class UserViewSet(viewsets.ModelViewSet):
     queryset = User.objects.all().order_by('username')
     serializer_class = UserSerializer