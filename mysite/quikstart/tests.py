from django.contrib.auth.models import User
from django.test import TestCase

from mysite.quikstart.models import Follow


class UsersTestList(TestCase):

    def test_request_list_users_usernames(self):
        User.objects.create(username='kelly')
        User.objects.create(username='jhon')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        username = {row['username'] for row in response.json()['results']}
        self.assertEqual(username, {'kelly', 'jhon'})

    def test_request_list_users(self):
        User.objects.create(username='kelly')
        User.objects.create(username='jhon')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {'email': '',
                 'first_name': '',
                 'last_name': '',
                 'url': 'http://testserver/v1/users/jhon/',
                 'username': 'jhon'},
                {'email': '',
                 'first_name': '',
                 'last_name': '',
                 'url': 'http://testserver/v1/users/kelly/',
                 'username': 'kelly'}
            ]
        })

    def test_unknown_url(self):
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code, 404)

    def test_request_list_users_null(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tom')
        self.user3 = User.objects.create(username='Mo')
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exists(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    # TODO: Написать проверку на duplicate и на подписку на самого себя
    #       дописать сами эти тесты
    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Follow.objects.get(follower=self.user1, follows=self.user3))

    def test_delete_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    def test_yourself_follow(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(Follow.objects.count(), 0)

    def test_unfollow_follow_not_exist_fail(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(Follow.objects.count(), 0)
