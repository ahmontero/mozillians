from django.db import models
from django.core import exceptions, validators
from tower import ugettext as _, ugettext_lazy as _lazy


class MultiURLField(models.TextField):

    default_error_messages = {
        'error_max_num': _lazy(u"Allowed number of urls: %s"),
    }

    def __init__(self, max_fields=None, *args, **kwargs):
        self.max_fields = max_fields
        super(MultiURLField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        value = value.split('\r\n')
        if len(value) > self.max_fields:
            msg = self.error_messages['error_max_num'] % str(self.max_fields)
            raise exceptions.ValidationError(msg)
        url_validator = validators.URLValidator(verify_exists=False)
        for url in value:
            url_validator(url)
        super(MultiURLField, self).validate(value, model_instance)
