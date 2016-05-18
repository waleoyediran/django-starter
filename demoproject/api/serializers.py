
import time
import datetime

import pytz
from django.contrib.auth.models import User
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    def to_internal_value(self, data):
        return datetime.datetime.fromtimestamp(int(data), tz=pytz.timezone('Africa/Lagos'))

    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')