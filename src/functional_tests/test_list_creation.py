from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ListCreationTest(FunctionalTest):
    def test_starting_a_todo_list(self):
        # user opens website
        self.browser.get(self.live_server_url)

        # he sees tab title and a header
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # FIRST ITEM
        # he is invited to enter a to-do item
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # he types into text box and hits enter
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        # page updates and now he sees his new to-do item
        self.wait_for_item_in_list("1: Buy eggs and milk")

        # SECOND ITEM
        # he is invited to enter a to-do item again
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # he types into text box and hits enter
        inputbox.send_keys("Buy cheese and bread")
        inputbox.send_keys(Keys.ENTER)
        # page updates and now he sees both his to-do items
        self.wait_for_item_in_list("2: Buy cheese and bread")
        self.wait_for_item_in_list("1: Buy eggs and milk")

    def test_multiple_users_and_lists(self):
        # user 1 opens website
        self.browser.get(self.live_server_url)
        # he creates a new to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        # he sees his new to-do item
        self.wait_for_item_in_list("1: Buy eggs and milk")

        # his list has a unique URL
        first_user_url = self.browser.current_url
        self.assertRegex(first_user_url, "/lists/.+")

        # user 2 opens website
        self.browser.get(self.live_server_url)
        # he doesn't see user 1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy eggs and milk", page_text)

        # he creates a new to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy cheese and bread")
        inputbox.send_keys(Keys.ENTER)
        # he sees his new to-do item
        self.wait_for_item_in_list("1: Buy cheese and bread")

        # his list has a unique URL
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, "/lists/.+")

        # still no trace of user 1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy eggs and milk", page_text)
        self.assertIn("Buy cheese and bread", page_text)

        # both users have different URLs
        self.assertNotEqual(first_user_url, second_user_url)
