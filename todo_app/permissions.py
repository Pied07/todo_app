from rest_framework.permissions import BasePermission
from .models import UserProfile
from django.shortcuts import get_object_or_404
from .encrypting_keys import decrypt_key
from django.conf import settings
import requests

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        # Check for API key in the query parameters
        api_key = request.query_params.get('api_key')
        print(api_key,request.user)
        if api_key is None:
            return False
        users = UserProfile.objects.filter(user=request.user)
        for user in users:
            print(user)
            key = user.apikey
            if not key:
                continue
            decrypted_key = decrypt_key(key)
            print(decrypted_key)
            if api_key==decrypted_key:
                return True
            else:
                continue
        return False