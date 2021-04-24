from rest_framework.routers import DefaultRouter, Route


class SwitchDetailRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'post': 'create',
                'delete': 'destroy'
            },
            name='{basename}-switch',
            detail=True,
            initkwargs={'suffix': 'switch'}
        ),
    ]


class RouterForTweets(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy'
            },
            name='{basename}-routerForTweets',
            detail=True,
            initkwargs={'suffix': 'routerForTweets'}
        ),
    ]
