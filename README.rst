======================
Django Elegant Choices
======================

.. image:: https://travis-ci.org/innovationinit/django-elegant-choices.svg?branch=master
    :target: https://travis-ci.org/innovationinit/django-elegant-choices

.. image:: https://coveralls.io/repos/github/innovationinit/django-elegant-choices/badge.svg?branch=master&foolcache=1
    :target: https://coveralls.io/github/innovationinit/django-elegant-choices?branch=master

-------
Purpose
-------

`Django Elegant Choices`_ is an utility for defining enumerations that can be used as choices in `Django`_ models.

--------
Features
--------

- defining symbolic name, database value and label of a choice in a single place
- storing extra metadata for a choice
- retrieving a choice by its symbolic name, database value or metadata entry value
- easy integration with Django by passing a choices class as the choices argument of a model field constructor

--------
Concepts
--------

We use a choices class as a namespace.

Database values of choices are currently integers.

-----
Usage
-----

The following code demonstrates how to use Choices in Django models.

.. code-block:: python

    # app/models.py
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from elegant_choices import Choice, Choices


    class PersonStatusChoices(Choices):
        ACTIVE = Choice(1, _('active'), {'extra_field': 'a'})
        INACTIVE = Choice(2, _('inactive'), {'extra_field': 'i'})


    class Person(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        status = models.PositiveSmallIntegerField(choices=PersonStatusChoices)


    person = Person(first_name='John', last_name='Coder', status=PersonStatusChoices.ACTIVE)
    print(person.status)  # prints 1
    print(person.status.name)  # prints ACTIVE
    print(person.status.label)  # prints active
    print(person.status.meta['extra_field'])  # prints a

    print(PersonStatusChoices.choices)  # prints [1, 2]
    print([choice.name for choice in PersonStatusChoices.choices])  # prints ['ACTIVE', 'INACTIVE']
    print(PersonStatusChoices.get_choice_by_meta_value('extra_field', 'i').name)  # prints INACTIVE
    print(PersonStatusChoices.choices_by_value[2].name)  # prints INACTIVE

-------
License
-------

The Django Elegant Choices package is licensed under the `MIT License`_.

.. _MIT License: https://opensource.org/licenses/MIT
.. _Django: https://www.djangoproject.com
.. _Django Elegant Choices: https://github.com/innovationinit/django-elegant-choices
