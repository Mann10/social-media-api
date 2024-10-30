from django.shortcuts import render
from api.models import Post,Comment,Likes
from api.serializers import PostSerializer,CommentSerializer,UserSerializer,LikesSerializer,LoginSerializer
from django.contrib.auth.models import User
from rest_framework import mixins,generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth import authenticate
from api.permissions import ISPostCreator
 
# Create your views here.

class PostsView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class PostDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[ISPostCreator]
    
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        
        if 'like' in request.data:
            return Response(
                {"detail": "Updating 'like' field directly is not allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
class CommentsView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
    def get(self, request,*args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CommentDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        comment=self.get_object()
        
        if comment.user!= request.user:
            return Response(
                {"detail": "Updating a comment of another user is not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        comment=self.get_object()
        #below we are making sure that the comment belongs to the user who is trying to delete it and the post it belongs to belongs to the user who is trying to delete it
        if comment.user!= request.user and comment.post.user!= request.user:
            return Response(
                {"detail": "Deleting a comment of another user is not allowed."},
                status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
class Register(mixins.CreateModelMixin,generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate input data
        user = serializer.save()  # Save the user instance
        return Response({'detail': 'User created successfully.', 'username': user.username}, status=status.HTTP_201_CREATED)
    
class PostByRespectiveUser(mixins.ListModelMixin, generics.GenericAPIView):
    
    '''
    Get all posts of a specific user.
    '''
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        print(user_id)
        if user_id is not None:
            return Post.objects.filter(user__id=user_id)
        return Post.objects.none()  # Return an empty queryset if no user_id is provided

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        if not queryset.exists():
            return Response({'detail': 'No posts found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CommentsfromPostId(generics.GenericAPIView,mixins.RetrieveModelMixin):
    serializer_class=CommentSerializer
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'No comments found for this post.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LikePost(mixins.CreateModelMixin, generics.GenericAPIView):
    
    serializer_class=LikesSerializer
    def post(self, request, *args, **kwargs):
        post_id=self.kwargs.get('post_id',None)
        
        try:
            post=Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail':'Post not found'},status=status.HTTP_404_NOT_FOUND)
        
        if Likes.objects.filter(post=post,user=request.user).exists():
            return Response({'detail':'User has already liked this post'},status=status.HTTP_400_BAD_REQUEST)
        
        like=Likes.objects.create(post=post,user=request.user)
        post.like+=1
        post.save(update_fields=['like'])
        serializer=self.get_serializer(like)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):
    
    serializer_class=LoginSerializer
    
    def post(self, request, *args, **kwargs):
        ser=self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user=authenticate(**ser.validated_data)
        login(request, user=user)
        return Response({"detail": "Login successful."},status=status.HTTP_200_OK)
            

class FetchLoggedInUsersComments(generics.GenericAPIView):
    """
    It will fetch all comments made by the currently logged in user.
    
    """
    serializer_class=CommentSerializer
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        comments = Comment.objects.filter(user=user)
        
        if not comments.exists():
            return Response({'detail': 'No comments found.'}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)