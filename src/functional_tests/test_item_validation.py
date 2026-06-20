from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_no_empty_list_items(self):
        # user opens website
        self.browser.get(self.live_server_url)

        # he accidentally submits an empty to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        # home page updages and an error is displayed
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # he creates a new to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy eggs and milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("1: Buy eggs and milk")

        # he accidentally submits an empty to-do item again
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        # list page updages and an error is displayed
        self.wait_for_item_in_list("1: Buy eggs and milk")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid")
        )

        # he creates a new to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy cheese and bread")
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid")
        )
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("2: Buy cheese and bread")

    def test_cannot_add_duplicate_items(self):
        # user opens website
        self.browser.get(self.live_server_url)

        # he creates a new to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("1: Buy eggs and milk")

        # he accidentally submits a duplicate to-do item
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)

        # list page updages and an error is displayed
        self.wait_for_item_in_list("1: Buy eggs and milk")
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You've already got this in your list"
            )
        )
