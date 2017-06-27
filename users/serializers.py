from rest_framework import serializers
from users import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'isLoggedIn')

    isLoggedIn = serializers.SerializerMethodField('get_is_logged_in')

    def get_is_logged_in(self, obj):
        return True