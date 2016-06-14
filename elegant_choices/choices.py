# -*- coding: utf-8 -*-

"""Utilities for creating annotated enumerations"""

from copy import deepcopy

import six

from .exceptions import MissingChoiceException


class Choice(int):

    """Single enum value representation"""

    name = None

    def __new__(cls, value, label, meta=None):
        """Store additional attributes in the choice

        :param value: the database value
        :type value: int
        :param label: the human-readable label
        :type label: str
        :param meta: a dictionary for storing extra metadata
        :type meta: dict or None
        :returns: a new choice instance
        :rtype: Choice
        """
        choice = super(Choice, cls).__new__(cls, value)
        choice.value = value
        choice.label = label
        choice.meta = meta or {}
        return choice

    def __deepcopy__(self, memo):
        """Create a new deep-copied instance of this Choice

        Needs to be implemented because the constructor signature does not match the int's one.
        """
        return Choice(self.value, deepcopy(self.label), deepcopy(self.meta))


class ChoicesMetaclass(type):

    """Prepare a choices class for listing choices, getting them by value and easy access in Django models"""

    def __new__(cls, name, bases, attrs):
        """Prepare choice list and choices_by_value dict and store them as class attributes."""
        choice_list = []
        value_to_choice_dict = {}

        for attribute_name, attribute_value in attrs.items():
            if isinstance(attribute_value, Choice):
                attribute_value.name = attribute_name
                choice_list.append(attribute_value)
                value_to_choice_dict[attribute_value.value] = attribute_value

        attrs['choices'] = sorted(choice_list)
        attrs['choices_by_value'] = value_to_choice_dict

        return super(ChoicesMetaclass, cls).__new__(cls, name, bases, attrs)

    def __iter__(cls):
        """Yield 2-tuples containing choice and its label

        This is a format that Django expects to be provided as the `choices` attribute of a model field.
        """
        for choice in cls.choices:
            yield choice, choice.label


class Choices(six.with_metaclass(ChoicesMetaclass, object)):

    """A base class for defining enumerations

    Example usage:

    >>> class StatusChoices(Choices):
    >>>     ACTIVE = Choice(1, 'Active')
    >>>     INACTIVE = Choice(2, 'Super OK Kraj', {'additional': 1})
    >>>
    >>> StatusChoices.ACTIVE
    1
    >>> StatusChoices.ACTIVE.name
    'ACTIVE'
    >>> StatusChoices.ACTIVE.value
    1
    >>> StatusChoices.ACTIVE.label
    'Active'
    >>> StatusChoices.INACTIVE.meta
    {'additional': 1}
    >>> StatusChoices.choices
    [1, 2]
    >>> StatusChoices.choices[0].name
    'ACTIVE'
    >>> StatusChoices.choices_by_value[2].name
    'INACTIVE'
    >>> list(StatusChoices)
    [(1, 'Active'), (2, 'Super OK Kraj')]
    """

    @classmethod
    def get_choice_by_meta_value(cls, meta_key, meta_value):
        """Get choice by meta value

        :param meta_key: meta dictionary key
        :type meta_key: string
        :param meta_key: meta dictionary value to get
        :type meta_key: string
        :returns: choice
        :rtype: `choices.choices.Choice`

        Example usage:

        >>> from utils.choices.choices import Choice, Choices
        >>>
        >>> class StatusChoices(Choices):
        >>>     ACTIVE = Choice(1, 'Active', {'external_system_name': 'act'})
        >>>     INACTIVE = Choice(2, 'Inactive', {'external_system_name': 'ina'})
        >>>
        >>> found = StatusChoices.get_choice_by_meta_value('external_system_name', 'ina')
        >>> found
        2
        >>> found.name
        'INACTIVE'
        """
        try:
            return next(choice for choice in cls.choices if choice.meta.get(meta_key) == meta_value)
        except StopIteration:
            raise MissingChoiceException('{value} is not an available choice!'.format(value=meta_value))
