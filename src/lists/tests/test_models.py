from django.test import TestCase

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
