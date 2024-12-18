from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import AllowAny


# API Views
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
   # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]  # Temporarily disable authentication

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# User Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.profile.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            user.profile.avatar = request.FILES['avatar']
        user.profile.save()
        return redirect('profile')
    return render(request, 'profile.html', {'user': request.user})



