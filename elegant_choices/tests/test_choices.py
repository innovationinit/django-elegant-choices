# -*- coding: utf-8 -*-

from unittest2 import TestCase

from elegant_choices import Choice, Choices, MissingChoiceException


class SimpleChoices(Choices):
    FIRST = Choice(1, 'First')
    SECOND = Choice(2, 'Second')
    THIRD = Choice(3, 'Third')


class MetadataChoices(Choices):
    FIRST = Choice(1, 'First', {'alternative_value': 'a'})
    SECOND = Choice(2, 'Second', {'alternative_value': 'b'})
    THIRD = Choice(3, 'Third', {'alternative_value': 'c'})


class ChoicesTestCase(TestCase):
    def test_retrieving_choices_by_identifier(self):
        self.assertEqual(SimpleChoices.FIRST, 1)
        self.assertEqual(SimpleChoices.SECOND, 2)
        self.assertEqual(SimpleChoices.THIRD, 3)

    def test_choice_attributes(self):
        self.assertEqual(SimpleChoices.FIRST.name, 'FIRST')
        self.assertEqual(SimpleChoices.FIRST.value, 1)
        self.assertEqual(SimpleChoices.FIRST.label, 'First')
        self.assertEqual(SimpleChoices.FIRST.meta, {})

        self.assertEqual(MetadataChoices.FIRST.name, 'FIRST')
        self.assertEqual(MetadataChoices.FIRST.value, 1)
        self.assertEqual(MetadataChoices.FIRST.label, 'First')
        self.assertEqual(MetadataChoices.FIRST.meta, {'alternative_value': 'a'})

    def test_choices_attribute(self):
        self.assertEqual(SimpleChoices.choices, [1, 2, 3])
        self.assertEqual(SimpleChoices.choices[0].name, 'FIRST')

    def test_getting_choice_by_meta_value(self):
        with self.assertRaises(MissingChoiceException):
            SimpleChoices.get_choice_by_meta_value('alternative_value', 'a')

        with self.assertRaises(MissingChoiceException):
            MetadataChoices.get_choice_by_meta_value('alternative_value', 'd')

    def test_iteration(self):
        as_list = list(SimpleChoices)
        self.assertListEqual(as_list, [(1, 'First'), (2, 'Second'), (3, 'Third')])
