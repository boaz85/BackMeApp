# from rest_framework import serializers
# from services import models
#
#
# class ServiceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.ServiceMeta
#         fields = ('name', 'slug', 'provider', 'mediumLogo', 'authUrl', 'completeUrl',
#                   'clientKey', 'permissionsScope')
#
#     mediumLogo = serializers.SerializerMethodField('get_medium_logo_url')
#     authUrl = serializers.ReadOnlyField(source='auth_url')
#     provider = serializers.ReadOnlyField(source='provider_slug')
#     completeUrl = serializers.ReadOnlyField(source='complete_url')
#     clientKey = serializers.ReadOnlyField(source='client_key')
#     permissionsScope = serializers.ReadOnlyField(source='permissions_scope_override')
#
#     def get_medium_logo_url(self, obj):
#         if obj.medium_logo:
#             return obj.medium_logo.url
#         else:
#             return None
