from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter
from mysite.quikstart import views
from mysite.quikstart.views import redirect_view
from mysite.router import SwitchDetailRouter, RouterForTweets

tweets_router = RouterForTweets()
switch_router = SwitchDetailRouter()

router = ExtendedDefaultRouter()
router.register(r'users', views.UserViewSet).register(
    r'tweets', views.UserTweetsViewSet, 'user-tweets', ['username'])
router.register(r'users', views.UserViewSet).register(
    r'followed', views.UserFollowersViewSet, 'user-followers', ['username'])
router.register(r'users', views.UserViewSet).register(
    r'follows', views.UserFollowsViewSet, 'user-follows', ['username'])
router.register(r'dogs', views.DogViewSet)
router.register(r'tweets', views.TweetsViewSet)
router.register(r'feed', views.FeedViewSet)
switch_router.register(f'follow', views.FollowViewSet)
tweets_router.register(f'tweets', views.TweetsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', redirect_view),
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
