from django.contrib.auth.models import User
from .models import Dog, Tweets, Follow
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_name', 'first_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class DogSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Dog
        fields = ['url', 'name', 'owner']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweets
        fields = ['id', 'url', 'text', 'photo', 'created', 'author']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []


class FollowsUserSerializer(serializers.HyperlinkedModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follows', 'followed']


class FollowerUserSerializer(serializers.HyperlinkedModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'followed']
