from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from sub.forms import UserRegisterForm, UserLoginForm, SubscriptionForm
from sub.models import Subscription
from sub.views import user_registration, user_login, user_logout, Home, EditSubscription, AddSubscription,\
    RemoveSubscription, subscription_delete_error


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.username = 'user'
        self.user.password = 'password'
        self.user.save()

    def test_fields(self):
        sub = Subscription()
        sub.team_name = 'test'
        sub.user = User.objects.get(pk=self.user.pk)
        sub.save()

        record = Subscription.objects.get(pk=sub.pk)
        self.assertEqual(record, sub)


class TestForms(TestCase):

    def test_user_register_form_data(self):
        form = UserRegisterForm(data={
            'username': 'user1',
            'password1': 'Asdqwe123!',
            'password2': 'Asdqwe123!',
            'email': 'user@gmail.com',
        })
        self.assertTrue(form.is_valid())

    def test_user_register_form_no_data(self):
        form = UserRegisterForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_user_login_form_no_data(self):
        form = UserLoginForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_subscription_form_data(self):
        form = SubscriptionForm(data={
            'team_name': 'sub1',
        })
        self.assertTrue(form.is_valid())

    def test_subscription_form_no_data(self):
        form = SubscriptionForm(data={
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestView(TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = 'default_user'
        self.user.password = 'poiLJK789'
        self.user.email = 'user@gmail.com'
        self.user.save()

        self.sub = Subscription()
        self.sub.title = 'test'
        self.sub.user = self.user
        self.sub.save()

    def test_index(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sub/subscriptions.html')

    def test_user_registration_GET(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sub/registration.html')

    def test_user_registration_POST(self):
        response = self.client.post(reverse('registration'), {
            'username': 'user1',
            'password1': 'poiLJK789',
            'password2': 'poiLJK789',
            'email': 'user@gmail.com',
        }, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_user_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sub/login.html')

    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_add_subscription_GET(self):
        url = reverse('subscription_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sub/subscription_add.html')

    def test_edit_subscription_GET(self):
        url = reverse('subscription_edit', args=[self.sub.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sub/subscription_edit.html')


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, Home)

    def test_registration_url_resolves(self):
        url = reverse('registration')
        self.assertEqual(resolve(url).func, user_registration)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, user_logout)

    def test_add_subscription_url_resolves(self):
        url = reverse('subscription_add')
        self.assertEqual(resolve(url).func.view_class, AddSubscription)

    def test_remove_subscription_url_resolves(self):
        url = reverse('remove_subscription', args=[1])
        self.assertEqual(resolve(url).func.view_class, RemoveSubscription)

    def test_subscription_delete_error_url_resolves(self):
        url = reverse('subscription_delete_error')
        self.assertEqual(resolve(url).func, subscription_delete_error)

    def test_edit_subscription_url_resolves(self):
        url = reverse('subscription_edit', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditSubscription)

