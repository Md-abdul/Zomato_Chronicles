import json

# Load menu data from data.json file (if it exists)
try:
    with open('data.json', 'r') as file:
        menu = json.load(file)
except FileNotFoundError:
    menu = []

# Define orders
orders = []

# Function to add a new dish to the menu
def add_dish(menu, dish):
    menu.append(dish)
    print(f"{dish['dishname']} has been added to the menu.")
    save_menu(menu)

# Function to remove a dish from the menu
def remove_dish(menu, dish_id):
    dish_found = False
    for dish in menu:
        if dish['id'] == dish_id:
            menu.remove(dish)
            dish_found = True
            print(f"Dish with ID {dish_id} has been removed from the menu.")
            save_menu(menu)
            break

    if not dish_found:
        print(f"Dish with ID {dish_id} not found in the menu.")

# Function to update dish availability
def update_availability(menu, dish_id, availability):
    dish_found = False
    for dish in menu:
        if dish['id'] == dish_id:
            dish['availability'] = availability
            print(f"Availability of dish with ID {dish_id} has been updated.")
            save_menu(menu)
            dish_found = True
            break

    if not dish_found:
        print(f"Dish with ID {dish_id} not found in the menu. Availability not updated.")

# Function to take orders from customers
def take_order(menu, customer_name, dish_ids):
    order = {'customer_name': customer_name, 'dishes': [], 'status': 'received'}
    
    for dish_id in dish_ids:
        dish_found = False
        for dish in menu:
            if dish['id'] == dish_id and dish['availability']:
                order['dishes'].append(dish['dishname'])
                dish_found = True
                break
        
        if not dish_found:
            print(f'Dish with ID {dish_id} is not available or does not exist.')

    if order['dishes']:
        orders.append(order)
        print(f"Order for {customer_name} has been received and added to the queue.")

# Function to update the status of an order
def update_order_status(order_id, new_status):
    order_found = False
    for order in orders:
        if order.get('order_id') == order_id:
            order['status'] = new_status
            print(f"Order {order_id} status has been updated to {new_status}.")
            order_found = True
            break

    if not order_found:
        print(f"Order with ID {order_id} not found.")

# Function to save menu data to data.json file
def save_menu(menu):
    with open('data.json', 'w') as file:
        json.dump(menu, file, indent=4)

# Main program loop
while True:
    print("\nWelcome to Zomato Chronicles!")
    print("1. Add a new dish to the menu")
    print("2. Remove a dish from the menu")
    print("3. Update dish availability")
    print("4. Take a new order")
    print("5. Update order status")
    print("6. Review all orders")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        dish_id = int(input("Enter dish ID: "))
        dishname = input("Enter dish name: ")
        price = float(input("Enter dish price: "))
        availability = input("Is the dish available (yes/no)? ").lower() == 'yes'
        new_dish = {'id': dish_id, 'dishname': dishname, 'price': price, 'availability': availability}
        add_dish(menu, new_dish)

    elif choice == '2':
        dish_id = int(input("Enter dish ID to remove: "))
        remove_dish(menu, dish_id)

    elif choice == '3':
        dish_id = int(input("Enter dish ID to update availability: "))
        availability = input("Is the dish available (yes/no)? ").lower() == 'yes'
        update_availability(menu, dish_id, availability)

    elif choice == '4':
        customer_name = input("Enter customer's name: ")
        dish_ids_input = input("Enter dish IDs (space-separated): ")
        dish_ids = [int(x) for x in dish_ids_input.split()]

        # Check if all entered IDs are valid and available
        all_ids_valid = True
        for dish_id in dish_ids:
            dish_found = False
            for dish in menu:
                if dish['id'] == dish_id and dish['availability']:
                    dish_found = True
                    break
            if not dish_found:
                print(f'Dish with ID {dish_id} is not available or does not exist.')
                all_ids_valid = False
                break

        if all_ids_valid:
            take_order(menu, customer_name, dish_ids)

    elif choice == '5':
        order_id = int(input("Enter order ID to update status: "))
        new_status = input("Enter new status: ")
        update_order_status(order_id, new_status)

    elif choice == '6':
        print("\nAll Orders:")
        for i, order in enumerate(orders):
            print(f"Order {i + 1}:")
            print(f"Customer: {order['customer_name']}")
            print(f"Dishes: {', '.join(order['dishes'])}")
            print(f"Status: {order['status']}\n")

    elif choice == '7':
        print("Exiting Zomato Chronicles. Have a great day!")
        save_menu(menu)  # Save menu data before exiting
        break

    else:
        print("Invalid choice. Please select a valid option.")
