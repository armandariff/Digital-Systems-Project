from typing import Any

from django.db.models import Field
from django.core import validators
from django.core.exceptions import ValidationError


class CommaSapratedIntegerField(Field):
    def __init__(self, dedup=None, min_length=None, max_length=None, *args: Any, **kwargs: Any) -> None:
        self.dedup = dedup
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(*args, **kwargs)
        
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))
    
    def to_python(self, value: Any) -> Any:
        if value in validators.EMPTY_VALUES:
            return []
        try:
            value = [int(item.strip()) for item in value.split(',')]
            if self.dedup:
                value = list(set(value))
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'])
        
        return value
    
    def clean(self, value: Any, model_instance) -> Any:
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value