from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_no_empty_list_items(self):
        # user opens website
        self.browser.get(self.live_server_url)
        
        # he accidentally submits an empty to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys(Keys.ENTER)

        # home page updages and an error is displayed
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item"
            )
        )
    
        # he creates a new to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy eggs and milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("1: Buy eggs and milk")

        # he accidentally submits an empty to-do item again
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys(Keys.ENTER)

        # list page updages and an error is displayed
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item"
            )
        )

        # he creates a new to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy cheese and bread")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_list("2: Buy cheese and bread")
