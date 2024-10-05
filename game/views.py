from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Users
from .Serializer  import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from . models import Exoplanet

@api_view(['POST'])
def unlock_exoplanet(request, id=None):
    if id is None:
        return Response({'error': 'User ID not provided'}, status=400)

    code = request.data.get('code')

    if not code:
        return Response({'error': 'Code is required'}, status=400)

    # Get the user profile
    user_profile = get_object_or_404(Users, pk=id)

    try:
        # Validate the unlock code
        exoplanet = Exoplanet.objects.get(code=code)
    except Exoplanet.DoesNotExist:
        return Response({'error': 'Invalid exoplanet code'}, status=400)

    # Check if the user has already unlocked this exoplanet
    if exoplanet in user_profile.unlocked_exoplanets.all():
        return Response({'message': 'Exoplanet already unlocked'}, status=200)

    # Unlock the exoplanet for the user
    user_profile.unlocked_exoplanets.add(exoplanet)
    return Response({'message': f'Unlocked {exoplanet.name}'}, status=200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        username = self.request.data.get('userName')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'},status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            # firstName=self.request.data.get('firstName'),
            # lastName=self.request.data.get('lastName'),
            email=self.request.data.get('email'),
            password=self.request.data.get('password'),

        )
        serializer.save(user=user)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username_or_email = request.data.get('userName')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if it's an email
    if '@' in username_or_email:
        try:
            user_profile = Users.objects.filter(email=username_or_email).first()
            if not user_profile:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            username_or_email = user_profile.username
        except Users.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_profile = Users.objects.filter(userName=username_or_email).first()
    # Authenticate user
    user = authenticate(username=username_or_email, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)

        return Response({'success': True, 'token': token.key , 'id' : user_profile.id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'success': True, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except AttributeError:
        return Response({'error': 'Token not found or invalid'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@permission_classes([AllowAny])
@api_view(['GET'])
def test(request):
    return HttpResponse("hello")
@permission_classes([AllowAny])
@api_view(['POST'])
def test2(request):
    return HttpResponse("hello from point 2")