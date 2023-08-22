from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_coffee_maker = CoffeeMaker()
my_money_machine = MoneyMachine()
meni = Menu()

on = True
while on:
    options = meni.get_items()
    choice = input(f"What would you like to order: {options} ")
    if choice == "off":
        on = False
    elif choice == "report":
        my_money_machine.report()
        my_coffee_maker.report()
    else:
        drink = meni.find_drink(choice)
        if my_coffee_maker.is_resource_sufficient(drink) and my_money_machine.make_payment(drink.cost):
            my_coffee_maker.make_coffee(drink)
        elif my_coffee_maker.is_resource_sufficient(drink) == False:
            on = False
