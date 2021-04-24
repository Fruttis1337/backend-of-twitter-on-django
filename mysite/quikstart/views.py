from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet

from .models import Dog, Tweets, Follow
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from mysite.quikstart.serializers import UserSerializer, DogSerializer, TweetSerializer, FollowSerializer, \
    FollowsUserSerializer, FollowerUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class DogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweets.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweets.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(author__username=self.kwargs['parent_lookup_username'])


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    # TODO: Попробуй добавить права на проверку
    def perform_create(self, serializer):
        if not self.queryset.filter(follower=self.request.user,
                                    follows=User.objects.get(username=self.kwargs[
                                        self.lookup_field])).exists() and self.request.user != \
                User.objects.get(username=self.kwargs[self.lookup_field]):
            serializer.save(follower=self.request.user,
                            follows=User.objects.get(username=self.kwargs[self.lookup_field]))
        elif self.queryset.filter(follower=self.request.user,
                                  follows=User.objects.get(username=self.kwargs[
                                      self.lookup_field])).exists():
            self.perform_destroy(self.get_object())

    def get_object(self):
        return self.queryset.filter(follower=self.request.user,
                                    follows__username=self.kwargs[self.lookup_field], )


class FeedViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Tweets.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author__follower__follower=self.request.user)


class UserFollowersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects
    serializer_class = FollowerUserSerializer

    def get_queryset(self):
        return self.queryset.filter(follows__username=self.kwargs['parent_lookup_username'])


class UserFollowsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects
    serializer_class = FollowsUserSerializer

    def get_queryset(self):
        return self.queryset.filter(follower__username=self.kwargs['parent_lookup_username'])
