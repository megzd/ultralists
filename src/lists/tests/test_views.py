from django.test import TestCase
from django.utils import html
from django.urls import reverse
import lxml.html

from lists.models import List, Item
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")

    def test_displays_input_form(self):
        response = self.client.get("/")
        parsed = lxml.html.fromstring(response.content)

        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), reverse("create_list"))

        inputs = form.cssselect("input")
        self.assertIn("text", [input.get("name") for input in inputs])

class CreateListTest(TestCase):
    def test_saves_post_requests(self):
        self.client.post(reverse("create_list"), data={"text": "new to-do item"})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "new to-do item")

    def test_redirects_to_user_list(self):
        response = self.client.post(reverse("create_list"), data={"text": "new to-do item"})

        my_list = List.objects.get()
        self.assertRedirects(response, my_list.get_absolute_url())

    def test_invalid_input_renders_home_template(self):
        response = self.client.post(reverse("create_list"), data={"text": ""})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/home.html")

    def test_invalid_input_displays_error(self):
        response = self.client.post(reverse("create_list"), data={"text": ""})

        self.assertContains(response, html.escape(EMPTY_ITEM_ERROR))

    def test_invalid_items_are_discarded(self):
        self.client.post(reverse("create_list"), data={"text": ""})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class UserListTest(TestCase):
    def test_uses_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(my_list.get_absolute_url())

        self.assertTemplateUsed(response, "lists/list.html")

    def test_displays_input_form(self):
        my_list = List.objects.create()
        response = self.client.get(my_list.get_absolute_url())
        parsed = lxml.html.fromstring(response.content)

        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), my_list.get_absolute_url())

        inputs = form.cssselect("input")
        self.assertIn("text", [input.get("name") for input in inputs])

    def test_displays_list_items(self):
        first_list = List.objects.create()
        Item.objects.create(text="to-do item 1", list=first_list)
        Item.objects.create(text="to-do item 2", list=first_list)

        second_list = List.objects.create()
        Item.objects.create(text="another item", list=second_list)

        response = self.client.get(first_list.get_absolute_url())
        self.assertContains(response, "to-do item 1")
        self.assertContains(response, "to-do item 2")
        self.assertNotContains(response, "another item")

    def test_saves_post_requests(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            correct_list.get_absolute_url(),
            data={"text": "new to-do item"}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "new to-do item")
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_user_list(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            correct_list.get_absolute_url(),
            data={"text": "new to-do item"}
        )
        self.assertRedirects(response, correct_list.get_absolute_url())

    def test_invalid_input_renders_list_template(self):
        my_list = List.objects.create()
        response = self.client.post(my_list.get_absolute_url(), data={"text": ""})

        parsed = lxml.html.fromstring(response.content)
        [input] = parsed.cssselect("input[name=text]")
        self.assertIn("is-invalid", list(input.classes))

    def test_empty_input_renders_list_template(self):
        my_list = List.objects.create()
        response = self.client.post(my_list.get_absolute_url(), data={"text": ""})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/list.html")

    def test_invalid_input_displays_error(self):
        my_list = List.objects.create()
        response = self.client.post(my_list.get_absolute_url(), data={"text": ""})

        self.assertContains(response, html.escape(EMPTY_ITEM_ERROR))

    def test_invalid_items_are_discarded(self):
        my_list = List.objects.create()
        self.client.post(my_list.get_absolute_url(), data={"text": ""})

        self.assertEqual(Item.objects.count(), 0)

    def test_duplicate_input_renders_list_template(self):
        my_list = List.objects.create()
        Item.objects.create(list=my_list, text="new to-do item") # duplicate item
        response = self.client.post(my_list.get_absolute_url(), data={"text": "new to-do item"})

        self.assertTemplateUsed(response, "lists/list.html")

    def test_duplicate_input_displays_error(self):
        my_list = List.objects.create()
        Item.objects.create(list=my_list, text="new to-do item") # duplicate item
        response = self.client.post(my_list.get_absolute_url(), data={"text": "new to-do item"})

        self.assertContains(response, html.escape(DUPLICATE_ITEM_ERROR))

    def test_duplicate_items_are_discarded(self):
        my_list = List.objects.create()
        Item.objects.create(list=my_list, text="new to-do item") # duplicate item
        self.client.post(my_list.get_absolute_url(), data={"text": "new to-do item"})

        self.assertEqual(Item.objects.all().count(), 1)
