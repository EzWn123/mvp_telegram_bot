from rest_framework import generics, viewsets
from rest_framework.response import Response
from . import models, serializers


class UserListApiView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get(self, request, token=None, format=None):
        messenger_id = self.request.GET.get('messenger_id')
        if messenger_id:
            queryset = models.User.objects.filter(messenger_id=messenger_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(data=serializer.data)
        return super(UserListApiView, self).get(request, token=None, format=None)


class UserDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
