class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            print(f"Ошибка: недостаточно товара '{self.name}' на складе.")
        else:
            self.stock += quantity


class Order:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity):
        if product.stock < quantity:
            print(f"Ошибка: недостаточно товара '{product.name}' на складе.")
        else:
            if product in self.products:
                self.products[product] += quantity
            else:
                self.products[product] = quantity
            product.update_stock(-quantity)

    def calculate_total(self):
        total = 0
        for product, quantity in self.products.items():
            total += product.price * quantity
        return total


class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def list_products(self):
        for product in self.products:
            print(f"{product.name}: {product.price} руб, на складе {product.stock} шт.")

    def create_order(self):
        return Order()


# Пример использования:
if __name__ == "__main__":
    store = Store()
    p1 = Product("Ноутбук", 75000, 10)
    p2 = Product("Мышь", 1500, 25)
    store.add_product(p1)
    store.add_product(p2)

    store.list_products()

    order = store.create_order()
    order.add_product(p1, 2)
    order.add_product(p2, 3)

    print(f"Общая стоимость заказа: {order.calculate_total()} руб.")
    store.list_products()
