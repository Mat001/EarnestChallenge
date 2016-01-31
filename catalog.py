__author__ = 'matjaz'
"""
    TESTING PRODUCT CATALOG CALCULATIONS

    Using your language and tools of choice, create a test suite that will verify correct
    pricing for the above catalog and all state tariffs.

    We are interested not only in the test scenarios you plan to execute but also in
    how you design your test suite. If there are opportunities to modify each page's html
    to make it more testable please let us know.
    If you have any questions about success criteria please let us know.

    1. test correct pricing for the above catalog and all state tariffs
    2. test other things: that elements are present when on second page


    PAGE OBJECT DESIGN PATTERN
    --------------------------
    Separates page elements from test logic.
    Usefulness:
    If page changes (different page) we only need to modify the
    page elements class. We don't need to modify much the class
    where tests are held. This way we keep frequently-changing-page-elements
    separate from much-less-changing test-logic. And it's cleaner and more readable.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.common import keys
import time
from pyvirtualdisplay import Display
import unittest
from abc import ABCMeta, abstractmethod


# base class for page objects
class Page():
    def __init__(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver

    # to navigate to catalog page because there is no link on the confirmation page that links to calc page
    def navigate_to_calculation_page(self):
        self.driver.get('https://jungle-socks.herokuapp.com/')
        return CalculationPage(self.driver)


# base class for webdriver
class WebDriver(unittest.TestCase):
    def setUp(self):
        # self._display = Display(visible=0, size=(1024, 768))  # uncomment for headless browser
        # self._display.start()      uncomment for headless browser
        self.driver = webdriver.Firefox()
        self.on_calculation_page = CalculationPage(self.driver)

    def tearDown(self):
        # self._display.stop()  # uncomment for headless browser
        self.driver.quit()


class Data():
    products = 'products'
    name = 'name'
    price = 'price'
    inventory_count = 'inventory_count'
    value = 'value'
    taxes = 'taxes'
    state = 'state'

    d = {
        products: [
            {name: 'zebra', price: 13.00, inventory_count: 23},
            {name: 'lion', price: 20.00, inventory_count: 12},
            {name: 'elephant', price: 35.00, inventory_count: 3},
            {name: 'giraffe', price: 17.00, inventory_count: 15}
        ],
        taxes: [
            {state: 'ca', value: 0.08},
            {state: 'ny', value: 0.06},
            {state: 'mn', value: 0.00}
        ]
    }

    def get_price(self, item_type):
        for item in self.d[self.products]:
            if item[self.name] == item_type:
                return item[self.price]

    def get_inventory_count(self, item_type):
        for item in self.d[self.products]:
            if item[self.name] == item_type:
                return item[self.inventory_count]


    def get_state_tax(self, state_name):
        for tax in self.d[self.taxes]:
            if tax[self.state] == state_name:
                return tax[self.value]
        else:
            return 0.05




# Calculation page - first child class
class CalculationPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # varirables for text fields and dropdown items
    zebra = '1'
    lion = '2'
    elephant = '3'
    giraffe = '4'

    state = 'CA'

    # ============   PAGE ELEMENTS   =================
    # fill form  with data (fillitem fields with quantities and select state)
    def add_quantities(self):
        self.driver.find_element_by_id('line_item_quantity_zebra').send_keys(self.zebra)
        self.driver.find_element_by_id('line_item_quantity_lion').send_keys(self.lion)
        self.driver.find_element_by_id('line_item_quantity_elephant').send_keys(self.elephant)
        self.driver.find_element_by_id('line_item_quantity_giraffe').send_keys(self.giraffe)
        return CalculationPage(self.driver)

    def select_state(self):
        select_state = Select(self.driver.find_element_by_name('state'))    # dropdown could go in its own method?
        select_state.select_by_value(self.state)
        return CalculationPage(self.driver)

    def checkout(self):
        self.driver.find_element_by_name('commit').click()
        if self.driver.find_element_by_tag_name('h1').text == 'Please Confirm Your Order':
            return ConfirmationPage(self.driver)
        elif self.driver.find_element_by_tag_name('h1').text == 'We\'re sorry, but something went wrong.':
            return ErrorPage(self.driver)


# Confirmation page - second child class
class ConfirmationPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # ============   PAGE ELEMENTS   =================
    def zebra_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[2]/td[3]').text

    def lion_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[3]/td[3]').text

    def elephant_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[4]/td[3]').text

    def giraffe_quantity(self):
        return self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[5]/td[3]').text

    # KEEP ADDING PAGE ELEMENTS HERE
    # ...

class ErrorPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def error_message(self):
        return self.driver.find_element_by_tag_name('h1').text


# =====   TESTS, TEST LOGIC, ASSERTIONS, TEST RUNNER
class TestCalculation(WebDriver):

    def test_prices_on_both_pages_match(self):

        self.on_calculation_page\
            .navigate_to_calculation_page()\
            .add_quantities()\
            .select_state()\

        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.zebra_quantity(), self.on_calculation_page.zebra)
        self.assertEqual(on_confirmation_page.lion_quantity(), self.on_calculation_page.lion)
        self.assertEqual(on_confirmation_page.elephant_quantity(), self.on_calculation_page.elephant)
        self.assertEqual(on_confirmation_page.giraffe_quantity(), self.on_calculation_page.giraffe)

    def test_nothing_entered(self):
        self.on_calculation_page.navigate_to_calculation_page()
        on_error_page = self.on_calculation_page.checkout()
        self.assertEqual(on_error_page.error_message() , 'We\'re sorry, but something went wrong.')


if __name__ is "__main__":
    """ Run test suite """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCalculation))
    runner = unittest.TextTestRunner()
    runner.run(suite)














