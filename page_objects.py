from selenium.webdriver.support.ui import Select
from data import Data


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


# Calculation page - first child class
class CalculationPage(Page):
    # variables for text fields and dropdown items
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # ============   PAGE ELEMENTS   =================
    # fill form  with data (fillitem fields with quantities and select state)
    def add_quantities(self, **kwargs):
        self.driver.find_element_by_id('line_item_quantity_zebra').send_keys(kwargs['ZEBRA'])
        self.driver.find_element_by_id('line_item_quantity_lion').send_keys(kwargs['LION'])
        self.driver.find_element_by_id('line_item_quantity_elephant').send_keys(kwargs['ELEPHANT'])
        self.driver.find_element_by_id('line_item_quantity_giraffe').send_keys(kwargs['GIRAFFE'])
        return CalculationPage(self.driver)

    def select_state(self, STATE):
        select_state = Select(self.driver.find_element_by_name('state'))  # dropdown could go in its own method?
        select_state.select_by_value(STATE)
        return CalculationPage(self.driver)

    def checkout(self):
        self.driver.find_element_by_name('commit').click()
        if self.driver.find_element_by_tag_name('h1').text == 'Please Confirm Your Order':
            return ConfirmationPage(self.driver)
        elif self.driver.find_element_by_tag_name('h1').text == 'We\'re sorry, but something went wrong.':
            return ErrorPage(self.driver)

    def tax_rate(self, st):
        return Data().get_state_tax(
            st.lower())  # see if this is not empty string!!!! Should populate when select_state method is called.

    # get prices, displayed on the calculation page
    def get_price_zebra_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[2]/td[2]').text)

    def get_price_lion_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[3]/td[2]').text)

    def get_price_elephant_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[4]/td[2]').text)

    def get_price_giraffe_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[5]/td[2]').text)

    # get inventory values, displayed on calculation page
    def get_stock_zebra_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[2]/td[3]').text)

    def get_stock_lion_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[3]/td[3]').text)

    def get_stock_elephant_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[4]/td[3]').text)

    def get_stock_giraffe_calc_page(self):
        return float(self.driver.find_element_by_xpath('html/body/form/table[1]/tbody/tr[5]/td[3]').text)


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

    def page_title(self):
        return self.driver.find_element_by_tag_name('h1').text


# error page - third child class
class ErrorPage(Page):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def error_message(self):
        return self.driver.find_element_by_tag_name('h1').text