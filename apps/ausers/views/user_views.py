from rest_framework import views, permissions, response, status, generics

from apps.ausers.serializers import UserDetailSerializer, UserUpdateSerializer


class GetUserDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):

        serializer = UserDetailSerializer(request.user)
        # serializer.is_valid(raise_exception=True)
        return response.Response(status=status.HTTP_200_OK, data=serializer.data)


class UpdateUserDetailView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user
