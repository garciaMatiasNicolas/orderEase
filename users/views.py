from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Users
from .serializer import UserSerializer
import threading


class UserViews:

    @staticmethod
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get_all_users(request):
        queryset = Users.objects.all()
        user_serializer = UserSerializer(queryset, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def create_user(request):
        user_serializer = UserSerializer(data=request.data)

        if request.method == 'POST':
            if user_serializer.is_valid():
                user = user_serializer.save()
                email = user.email
                user_pk = user.id
                message = f'''Para confirmar tu mail ingresa a este link: 
                http://localhost:8000/{reverse(viewname="confirm_mail", args=[user_pk])}'''

                def send_email() -> None:
                    send_mail(
                        subject="Confirmación mail OrderEase",
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                    )

                email_thread = threading.Thread(target=send_email)
                email_thread.start()

                return Response({'message': 'user_saved', 'user': user_serializer.data},
                                status=status.HTTP_201_CREATED)

            else:
                return Response({'error': 'bad_request', 'logs': user_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'method_not_allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    @api_view(['PUT', 'DELETE', 'GET'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def detail_user(request, pk):
        user = Users.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data=request.data)

        if user:
            if request.method == 'GET':
                user_data = UserSerializer(user)
                return Response(user_data.data)

            if request.method == 'PUT':
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({'message': 'user_updated', 'user': user_serializer.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'bad_request', 'logs': user_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif request.method == 'DELETE':
                user.delete()
                return Response({'message': 'user_deleted'}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'method_not_allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        else:
            return Response({'error': 'user_not_exists'}, status=status.HTTP_400_BAD_REQUEST)

