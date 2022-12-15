from flask_testing import LiveServerTestCase
from urllib.request import urlopen
from test_base import BaseTest

class ServerTest(BaseTest, LiveServerTestCase):
    def test_server_is_up_and_running(self):
        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)