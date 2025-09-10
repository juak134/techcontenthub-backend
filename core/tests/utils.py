from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

def auth_client(user):
    client = APIClient()
    token = str(RefreshToken.for_user(user).access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
