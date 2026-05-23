from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from lists.models import List, Item

class ModelsTest(TestCase):
    def test_saves_and_retrieves_items(self):
        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.text = "to-do item 1"
        first_item.list = my_list
        first_item.save()

        second_item = Item()
        second_item.text = "to-do item 2"
        second_item.list = my_list
        second_item.save()

        # there should only be one object with get()
        saved_list = List.objects.get()
        self.assertEqual(saved_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "to-do item 1")
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "to-do item 2")
        self.assertEqual(second_saved_item.list, my_list)

    def test_rejects_new_null_items(self):
        my_list = List()
        my_list.save()

        # database-level validation
        # by default in TextField(), database doesn't accept None value (NOT NULL constraint)
        new_item = Item(list=my_list, text=None)

        # testing that incorrect behaivor raises an error
        # the testing would continue after an error due to with statement
        # but assertRaises() itself would fail if no error is raised
        with self.assertRaises(IntegrityError):
            new_item.save()

    def test_rejects_new_empty_items(self):
        my_list = List()
        my_list.save()

        new_item = Item(list=my_list, text="")

        # model-level validation
        # by default in TextField(), django doesn't accept empty string (blank=False attribute)
        with self.assertRaises(ValidationError):
            # django models don’t run full validation on save
            new_item.full_clean()
