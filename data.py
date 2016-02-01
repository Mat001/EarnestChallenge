# class to deal with catalog data - not sure if it's really needed
# I only used it to calculate tax
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