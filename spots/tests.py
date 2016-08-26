from django.test import TestCase
from .models import Spot
from rest_auth.models import MyUser
from spots.logic import geo_utils
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from core_features.models import PendingMedia
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from oauth2_provider.models import get_application_model, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
import datetime


Application = get_application_model()

class SpotTestCase(TestCase):
    def setUp(self):
        user = MyUser.objects.create(username='test_pilot',email='test@pilot.com')
        spot = Spot.objects.create(name='Test Spot Berlin',created_by= user,lat=52.48845100,lng=13.37757000)

        PendingMedia.update_pending_media(Spot.MEDIA_TYPE, spot.id, 1)


    def test_spot_is_nearby(self):
        testLat = 52.488428
        testLng = 13.376394
        testRadius = 1000

        my_spot = Spot.objects.get(name='Test Spot Berlin')
        spots_nearby = geo_utils.nearby(testLat,testLng,testRadius)

        self.assertTrue(my_spot in spots_nearby)

class SpotRestTest(APITestCase):

    @staticmethod
    def __create_authorization_header(token):
        return "Bearer {0}".format(token)

    def setUp(self):
        self.user = MyUser.objects.create(username='test_pilot',email='test@pilot.com')

        self.application = Application(
            name="Test Application",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        oauth2_settings._SCOPES = ['spot_guy']

        token = AccessToken.objects.create(user=self.user,
                                         token='123456789',
                                         application=self.application,
                                         expires=timezone.now()+datetime.timedelta(days=1),
                                         scope='spot_guy')
        token = SpotRestTest.__create_authorization_header(token.token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def tearDown(self):
        self.application.delete()
        self.user.delete()

    def test_create_spot(self):

        url = reverse('spot-list')
        data = {'name':'Test New Spot'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
