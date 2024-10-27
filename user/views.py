from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ProfileSerializer, FollowSerializer
from .models import Profile, Follow
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
        'posts': reverse('posts-list', request=request, format=format),
        'comments': reverse('comments-list', request=request, format=format),
    })
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token" : token.key,
                "user" : UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token" : token.key,
                "user" : UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else :
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.all()
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user!= self.request.user:
            return Response({'status':'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        profile = self.get_object()
        follower_profile = Profile.objects.get(user=request.user)

        if not Follow.objects.filter(follower=follower_profile, following=profile).exists():
            Follow.objects.create(follower=follower_profile, following=profile)
            return Response({'status': 'Following'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        follower_profile = Profile.objects.get(user=request.user)

        follow_instance = Follow.objects.filter(follower=follower_profile, following=profile).first()
        if follow_instance:
            follow_instance.delete()
            return Response({'status': 'Unfollowed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Not following'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        profile = self.get_object()
        followers = profile.followers.all()  
        serializer = ProfileSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        profile = self.get_object()
        following = profile.following.all()  
        serializer = ProfileSerializer(following, many=True)
        return Response(serializer.data)