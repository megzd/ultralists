from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from lists.models import List, Item

class ModelsTest(TestCase):
    def test_saves_and_retrieves_items(self):
        my_list = List.objects.create()
        Item.objects.create(list=my_list, text="to-do item 1")
        Item.objects.create(list=my_list, text="to-do item 2")
        # returns the only object present
        # raises DoesNotExist or MultipleObjectsReturned otherwise
        saved_list = List.objects.get()
        self.assertEqual(saved_list, my_list)
        # returns all objects present
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "to-do item 1")
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "to-do item 2")
        self.assertEqual(second_saved_item.list, my_list)

    def test_rejects_new_null_items(self):
        my_list = List.objects.create()
        # database-level validation
        # by default, database doesn't accept None value in TextField() (NOT NULL constraint)
        new_item = Item(list=my_list, text=None)
        # testing that incorrect behaivor raises an error
        # the tests will continue after an error due to with statement
        with self.assertRaises(IntegrityError):
            new_item.save()

    def test_rejects_new_empty_items(self):
        my_list = List.objects.create()
        # model-level validation
        # by default, django doesn't accept empty string in TextField() (blank=False attribute)
        new_item = Item(list=my_list, text="")
        with self.assertRaises(ValidationError):
            # django models don’t run full validation on just save()
            new_item.full_clean()

    def test_rejects_new_duplicate_items(self):
        my_list = List.objects.create()
        first_item = Item(list=my_list, text="new to-do item")
        first_item.save()
        with self.assertRaises(ValidationError):
            second_item = Item(list=my_list, text="new to-do item")
            second_item.full_clean()

    def test_saves_same_item_in_different_lists(self):
        first_list = List.objects.create()
        second_list = List.objects.create()
        first_item = Item(list=first_list, text="new to-do item")
        first_item.save()
        second_item = Item(list=second_list, text="new to-do item")
        second_item.full_clean() # should not raise

    def test_item_string_representation(self):
        new_item = Item(text="new to-do item")
        self.assertEqual(str(new_item), "new to-do item")

    def test_get_absolute_url_for_lists(self):
        my_list = List.objects.create()
        self.assertEqual(my_list.get_absolute_url(), f"/lists/{my_list.id}/")

    def test_item_order_in_lists(self):
        my_list = List.objects.create()
        first_item = Item.objects.create(list=my_list, text="3")
        second_item = Item.objects.create(list=my_list, text="1")
        third_item = Item.objects.create(list=my_list, text="2")
        self.assertEqual(list(my_list.item_set.all()), [first_item, second_item, third_item])
