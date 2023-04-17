from .models import User
from api.versioned.v1.permissions import IsAdmin
from api.versioned.v1.serializers import (
    RegisterSerializer,
    AdminUserSerializer
)
from api.versioned.v1.serializers import UserSerializer, TokenSerializer
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .utils import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    """Отправка и создание кода."""
    queryset = User.objects.order_by('username').all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def users_profile(self, request):
        """Профайл пользователя."""
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        User.objects.get(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
    except User.DoesNotExist:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    return Response(
        "Код подтверждения отправлен Вам на электронный ящик",
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': str(user)}, status=status.HTTP_200_OK)
