from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class CategoryNameRelatedField(serializers.PrimaryKeyRelatedField):
    """
    -> this is essentialy a primarykeyrealted field with a small tweak in a to_representation method.
        instead of returning id of the objects, string repr is returned.
    -> to_internal_value uses category_name instead of pk and checks if data is str
    """

    def to_representation(self, value):

        return str(value)  # changed from return value.id

    def to_internal_value(self, data):

        queryset = self.get_queryset()

        try:
            if not isinstance(data, str):
                raise TypeError
            return queryset.get(category_name=data)  # changed from pk
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)
