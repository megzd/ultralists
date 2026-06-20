from django.test import TestCase

from lists.forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from lists.models import Item, List

class ItemFormTest(TestCase):
    def test_form_has_placeholder_and_css_classes(self):
        form = ItemForm()
        rendered = form.as_p()

        self.assertIn('placeholder="Enter a to-do item"', rendered)
        self.assertIn('class="form-control form-control-lg"', rendered)

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={"text": ""})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        my_list = List.objects.create()
        form = ItemForm(data={"text": "new to-do item"})
        new_item = form.save(for_list=my_list)

        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, "new to-do item")
        self.assertEqual(new_item.list, my_list)

    def test_invalid_form_has_is_invalid_css_class(self):
        form = ItemForm(data={"text": ""})

        self.assertFalse(form.is_valid())
        field = form.fields["text"]
        self.assertEqual(field.widget.attrs["class"], "form-control form-control-lg is-invalid")


class ExistingListItemFormTest(TestCase):
    def test_form_has_placeholder_and_css_classes(self):
        my_list = List.objects.create()
        form = ExistingListItemForm(for_list=my_list)
        rendered = form.as_p()

        self.assertIn('placeholder="Enter a to-do item"', rendered)
        self.assertIn('class="form-control form-control-lg"', rendered)

    def test_form_validation_for_blank_items(self):
        my_list = List.objects.create()
        form = ExistingListItemForm(for_list=my_list, data={"text": ""})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        my_list = List.objects.create()
        Item.objects.create(list=my_list, text="new to-do item")
        form = ExistingListItemForm(for_list=my_list, data={"text": "new to-do item"})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [DUPLICATE_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        my_list = List.objects.create()
        form = ExistingListItemForm(for_list=my_list, data={"text": "new to-do item"})

        self.assertTrue(form.is_valid())
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.get())

