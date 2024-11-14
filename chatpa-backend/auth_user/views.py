from rest_framework import status
from rest_framework.response import Response
from auth_user.serializers import UserSerializer
from rest_framework.views import APIView

class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)