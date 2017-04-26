"""User Test."""
import unittest2
from app.test_server import app
from pyquery import PyQuery
from tools import init_users, randomword, remove_users, users


class TestUser(unittest2.TestCase):
    """User Test."""

    def setUp(self):
        self.name = users[0]['name']
        self.email = users[0]['email']
        self.password = users[0]['password']
        self.csrf = ""
        self.client = app.test_client()  # we instantiate a flask test client
        self.users_ids = init_users()
        self.login_user()

    def tearDown(self):
        remove_users()

    def login_user(self):
        data = {'email': self.email,
                'password': self.password}
        response = self.client.get(
            '/auth/login'
        )
        pq = PyQuery(response.data)
        tag = pq('input#csrf_token')
        headers = {}
        if tag:
            self.csrf = tag[0].value
            headers = {'X-CSRFToken': self.csrf}
        if response.status_code == 200:
            login = self.client.post(
                '/auth/login', data=data, headers=headers
            )
            if login.status_code == 302:
                return True

    def test_load_edit_user(self):
        # the test client can request a route
        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/user/edit/%s' % self.users_ids[self.name], headers=headers
        )
        pq = PyQuery(response.data)
        name = pq('input#name')[0].value
        email = pq('input#email')[0].value
        self.assertEqual(email, self.email)
        self.assertEqual(name, self.name)
        self.assertEqual(response.status_code, 200)

    def test_change_edit_user(self):
        # the test client can request a route
        headers = {'X-CSRFToken': self.csrf}
        data = {'email': self.email,
                'name': randomword(8),
                'password': '',
                'active': True,
                'state': "confirmed",
                'rol': 'admin',
                'confirm': '',
                'id': self.users_ids[self.name]}
        response = self.client.post(
            '/user/edit/%s' % self.users_ids[self.name],
            data=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            '/user/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        pq = PyQuery(response.data)
        data = pq('script').text()
        self.assertIn("Elemento Actualizado", data)

    def test_list_users(self):

        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/user/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):

        headers = {'X-CSRFToken': self.csrf}
        response = self.client.get(
            '/user/delete/%s' % self.users_ids['Alejandro'], headers=headers
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            '/user/list', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        pq = PyQuery(response.data)
        data = pq('script').text()
        self.assertIn("Elemento Eliminado", data)


if __name__ == '__main__':
    unittest2.main()
