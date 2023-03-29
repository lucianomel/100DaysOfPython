from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

is_on = True
coffee_maker = CoffeeMaker()
menu = Menu()
money_machine = MoneyMachine()
while is_on:
    coffee_input = input(f"What would you like? ({menu.get_items()})")
    if coffee_input =="off":
        is_on=False
    elif coffee_input == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        menu_item = menu.find_drink(coffee_input)
        if coffee_maker.is_resource_sufficient(menu_item):
            if money_machine.make_payment(menu_item.cost):
                # Sufficient money, coins accepted
                coffee_maker.make_coffee(menu_item)
            #else:
                # Insuficient money, money refunded
        #else:
         #   print_insufficient_resource(coffee_maker,menu_item)

