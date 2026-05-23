from django.test import TestCase
from django.utils import html
import lxml.html

from lists.models import List, Item

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")

    def test_displays_input_form(self):
        response = self.client.get("/")
        parsed = lxml.html.fromstring(response.content)

        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), "/lists/create")

        inputs = form.cssselect("input")
        self.assertIn("item_text", [input.get("name") for input in inputs])

class CreateListTest(TestCase):
    def test_saves_post_requests(self):
        self.client.post("/lists/create", data={"item_text": "new to-do item"})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "new to-do item")

    def test_redirects_to_user_list(self):
        response = self.client.post("/lists/create", data={"item_text": "new to-do item"})

        my_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{my_list.id}/")

    def test_handles_validation_errors(self):
        response = self.client.post("/lists/create", data={"item_text": ""})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lists/home.html")

        expected_error = html.escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_are_discarded(self):
        self.client.post("/lists/create", data={"item_text": ""})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class UserListTest(TestCase):
    def test_uses_list_template(self):
        my_list = List.objects.create()

        response = self.client.get(f"/lists/{my_list.id}/")
        self.assertTemplateUsed(response, "lists/list.html")

    def test_displays_input_form(self):
        my_list = List.objects.create()

        response = self.client.get(f"/lists/{my_list.id}/")
        parsed = lxml.html.fromstring(response.content)

        [form] = parsed.cssselect("form[method=POST]")
        self.assertEqual(form.get("action"), f"/lists/{my_list.id}/")

        inputs = form.cssselect("input")
        self.assertIn("item_text", [input.get("name") for input in inputs])

    def test_displays_list_items(self):
        first_list = List.objects.create()
        Item.objects.create(text="to-do item 1", list=first_list)
        Item.objects.create(text="to-do item 2", list=first_list)

        second_list = List.objects.create()
        Item.objects.create(text="another item", list=second_list)

        response = self.client.get(f"/lists/{first_list.id}/")
        self.assertContains(response, "to-do item 1")
        self.assertContains(response, "to-do item 2")
        self.assertNotContains(response, "another item")

    def test_saves_post_requests(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"item_text": "new to-do item"}
        )
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "new to-do item")
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_user_list(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"item_text": "new to-do item"}
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
