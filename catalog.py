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
import logging


ZEBRA = 1
LION = 2
ELEPHANT = 3
GIRAFFE = 4
STATE = 'NY'

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

    # this method removes duplication
    # It's used in most test methods so it's been put here and referenced as one line "navigate()"
    def go_to_calculation_page_and_fill_it_out(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities() \
            .select_state()

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
                return float(tax[self.value])
        else:
            return float(0.05)


# Calculation page - first child class
class CalculationPage(Page):
    # variables for text fields and dropdown items
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # ============   PAGE ELEMENTS   =================
    # fill form  with data (fillitem fields with quantities and select state)
    def add_quantities(self):
        self.driver.find_element_by_id('line_item_quantity_zebra').send_keys(ZEBRA)
        self.driver.find_element_by_id('line_item_quantity_lion').send_keys(LION)
        self.driver.find_element_by_id('line_item_quantity_elephant').send_keys(ELEPHANT)
        self.driver.find_element_by_id('line_item_quantity_giraffe').send_keys(GIRAFFE)
        return CalculationPage(self.driver)

    def select_state(self):
        select_state = Select(self.driver.find_element_by_name('state'))    # dropdown could go in its own method?
        select_state.select_by_value(STATE)
        return CalculationPage(self.driver)

    def checkout(self):
        self.driver.find_element_by_name('commit').click()
        if self.driver.find_element_by_tag_name('h1').text == 'Please Confirm Your Order':
            return ConfirmationPage(self.driver)
        elif self.driver.find_element_by_tag_name('h1').text == 'We\'re sorry, but something went wrong.':
            return ErrorPage(self.driver)

    def tax_rate(self):
        return Data().get_state_tax(STATE.lower())

    def get_price_zebra_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[2]/td[2]').text)

    def get_price_lion_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[3]/td[2]').text)

    def get_price_elephant_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[4]/td[2]').text)

    def get_price_giraffe_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[5]/td[2]').text)




# Confirmation page - second child class
class ConfirmationPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # ============   PAGE ELEMENTS   =================
    # QUANTITY
    def quantity_zebra(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[2]/td[3]').text)

    def quantity_lion(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[3]/td[3]').text)

    def quantity_elephant(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[4]/td[3]').text)

    def quantity_giraffe(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[5]/td[3]').text)

    # PRICE
    def price_zebra(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[2]/td[2]').text)

    def price_lion(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[3]/td[2]').text)

    def price_elephant(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[4]/td[2]').text)

    def price_giraffe(self):
        return float(self.driver.find_element_by_xpath('html/body/table[2]/tbody/tr[5]/td[2]').text)

    # SUBTOTAL
    def subtotal(self):
        subtotal = self.driver.find_element_by_id('subtotal').text
        if subtotal.startswith('$'):
            return float(subtotal[1:])
        else:
            return float(subtotal)

    def taxes(self):
        taxes = self.driver.find_element_by_id('taxes').text
        if taxes.startswith('$'):
            return float(taxes[1:])
        else:
            return float(taxes)

    def total(self):
        total = self.driver.find_element_by_id('total').text
        if total.startswith('$'):
            return float(total[1:])
        else:
            return float(total)


class ErrorPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def error_message(self):
        return self.driver.find_element_by_tag_name('h1').text



# =====   TESTS, TEST LOGIC, ASSERTIONS, TEST RUNNER
class TestCalculation(WebDriver):

    # ==========   TESTS FOR CALCULATIONS   ===========
    def test_subtotal(self):
        self.go_to_calculation_page_and_fill_it_out()

        on_confirmation_page = self.on_calculation_page.checkout()

        subtotal_zebra = on_confirmation_page.price_zebra() * on_confirmation_page.quantity_zebra()
        subtotal_lion = on_confirmation_page.price_lion() * on_confirmation_page.quantity_lion()
        subtotal_elephant = on_confirmation_page.price_elephant() * on_confirmation_page.quantity_elephant()
        subtotal_giraffe = on_confirmation_page.price_giraffe() * on_confirmation_page.quantity_giraffe()

        subtotal_expected = subtotal_zebra + subtotal_lion + subtotal_elephant + subtotal_giraffe
        subtotal_displayed = on_confirmation_page.subtotal()
        self.assertEqual(subtotal_expected, subtotal_displayed)


    def test_tax(self):
        self.go_to_calculation_page_and_fill_it_out()

        on_confirmation_page = self.on_calculation_page.checkout()

        # expected taxes
        taxes_expected = on_confirmation_page.subtotal() * self.on_calculation_page.tax_rate()
        taxes_expected = round(taxes_expected, 4)   # round decimal number to 4 digits
        # displayed taxes
        taxes_displayed = on_confirmation_page.taxes()
        self.assertEqual(taxes_expected, taxes_displayed)


    def test_total(self):
        self.go_to_calculation_page_and_fill_it_out()

        on_confirmation_page = self.on_calculation_page.checkout()

        total_expected = on_confirmation_page.subtotal() + on_confirmation_page.taxes()
        total_displayed = on_confirmation_page.total()
        self.assertEqual(total_displayed, total_expected)


class TestFormat(WebDriver):
    # ==========   TESTS RELATED TO THE FORMAT AND OF ENTERED VALUES   ===========
    def test_item_where_entered_characters_should_no_be_calculated(self):
        pass

    def test_item_whereentered_special_chars_should_not_be_calculated(self):
        pass

    def test_mix_of_entered_specialchars_chars_numbers_should_calculate_only_numbers(self):
        pass

    def test_entered_exremely_large_numbers_should_be_limited(self):
        pass

    def test_all_entered_are_characters_should_calculate_total_zero(self):
        pass

    def test_entered_decimal_number_should_have_decimal_part_truncated(self):
        pass

    def test_negative_numbers_ignored_in_calculation(self):
        pass


class TestInventoryLimit(WebDriver):
    # ==========   TESTS RELATED INVENTORY LIMIT   ===========
    def test_quantities_higher_than_stock_not_allowed(self):
        pass


class TestDataDriven(WebDriver):
    # ==========   TESTS RELATED TO COMBINATIONS OF POPULATED AND EMPTY FIELDS AND STATE SELECTIONS   ===========
    pass


class TestDisplay(WebDriver):
    # ==========   TESTS RELATED TO CORRECTLY DISPLAYING VALUES   ===========
    def test_entered_quantities_display_on_confirmation_page(self):
        self.go_to_calculation_page_and_fill_it_out()
        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.quantity_zebra(), ZEBRA)
        self.assertEqual(on_confirmation_page.quantity_lion(), LION)
        self.assertEqual(on_confirmation_page.quantity_elephant(), ELEPHANT)
        self.assertEqual(on_confirmation_page.quantity_giraffe(), GIRAFFE)

    def test_displayed_prices_on_both_pages_match(self):
        self.go_to_calculation_page_and_fill_it_out()
        on_confirmation_page = self.on_calculation_page.checkout()

        self.assertEqual(on_confirmation_page.price_zebra(), self.on_calculation_page.get_price_zebra_calc_page())
        self.assertEqual(on_confirmation_page.price_lion(), self.on_calculation_page.get_price_lion_calc_page())
        self.assertEqual(on_confirmation_page.price_elephant(), self.on_calculation_page.get_price_elephant_calc_page())
        self.assertEqual(on_confirmation_page.price_giraffe(), self.on_calculation_page.get_price_giraffe_calc_page())


class TestEdgeCases(WebDriver):
    # ========   TESTING EDGE CASES   =============
    def test_nothing_entered_should_take_to_error_page(self):
        self.on_calculation_page.navigate_to_calculation_page()
        on_error_page = self.on_calculation_page.checkout()
        self.assertEqual(on_error_page.error_message(), 'We\'re sorry, but something went wrong.')

    def test_quantites_all_selected_but_no_state_should_take_to_error_page(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .add_quantities()
        # no state selected !

        # should redirect to error page
        on_error_page = self.on_calculation_page.checkout()
        self.assertEqual(on_error_page.error_message(), 'We\'re sorry, but something went wrong.')

    def test_state_selected_but_no_quantities_should_total_zero(self):
        self.on_calculation_page \
            .navigate_to_calculation_page() \
            .select_state()

        # should ive total as zero
        on_confirmation_page = self.on_calculation_page.checkout()

        total_expected = on_confirmation_page.subtotal() + on_confirmation_page.taxes()
        total_displayed = on_confirmation_page.total()
        self.assertEqual(total_displayed, total_expected)
        self.assertEqual(total_displayed, 0.00)



if __name__ is "__main__":
    """ Run test suites """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCalculation))
    suite.addTest(unittest.makeSuite(TestDisplay))
    suite.addTest(unittest.makeSuite(TestDataDriven))
    suite.addTest(unittest.makeSuite(TestEdgeCases))
    suite.addTest(unittest.makeSuite(TestFormat))
    suite.addTest(unittest.makeSuite(TestInventoryLimit))
    runner = unittest.TextTestRunner()
    runner.run(suite)














