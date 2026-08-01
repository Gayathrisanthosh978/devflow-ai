from rest_framework import generics

from apps.accounts.api.serializers.user import UserSerializer


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
