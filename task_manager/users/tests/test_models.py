from django.urls import reverse

from django.contrib.auth.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserListView(UserTestCase):
    REGISTRATION_URL = reverse('users')

    def test_user_list(self):
        response = self.client.get(self.REGISTRATION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(User.objects.count(), self.user_count)


class TestUserCreateView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('user_create')
        self.redirect_url = reverse('login')

    def test_get_create_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_user_creation(self):
        initial_count = User.objects.count()
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)


class TestUserDeleteView(UserTestCase):
    def test_user_deletion_unauthorized(self):
        response = self.client.get(reverse(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.client.post(reverse(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_self_deletion_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)
        initial_count = User.objects.count()

        response = self.client.get(reverse(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

        response = self.client.post(reverse(
            'user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(User.objects.count(), initial_count - 1)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user1.id)

    def test_other_user_deletion_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)

        response = self.client.get(reverse(
            'user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, user1.username)


class TestUserUpdateView(UserTestCase):
    def test_user_update_unauthorized(self):
        user1 = self.user1

        response = self.client.get(
            reverse('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_self_update_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)

        update_data = {
            'first_name': 'TestName',
            'last_name': 'LTestName',
            'username': 'loin13',
            'password1': 'asdF12',
            'password2': 'asdF12',
        }

        response = self.client.get(
            reverse('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user1.id}),
            update_data
        )

        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users"))

        updated_user = User.objects.get(id=user1.id)
        self.assertEqual(updated_user.username, 'loin13')
        self.assertEqual(updated_user.first_name, 'TestName')
        self.assertEqual(updated_user.last_name, 'LTestName')

    def test_other_user_update_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)

        update_data = {
            'first_name': 'FName112',
            'last_name': 'LName223',
            'username': 'hyrt2',
            'password1': 'ZXCh6',
            'password2': 'ZXCh6',
        }

        response = self.client.get(
            reverse('user_update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user1.id}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, 'oimjmnnname')
