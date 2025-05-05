import logging

# Setup logging
logging.basicConfig(
    filename='shopping_list_app.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

shopping_list = []
TAX_RATE = 0.07  # fixed tax rate (7%)

def home_screen():
    while True:
        print("\n--- Home Screen ---")
        print("1. Add Item")
        print("2. View Shopping List")
        print("3. Checkout")
        print("4. Settings")
        print("5. Exit App")
        choice = input("Select an option: ").strip()

        if choice == '1':
            add_item_screen()
        elif choice == '2':
            view_list_screen()
        elif choice == '3':
            checkout_screen()
        elif choice == '4':
            settings_screen()
        elif choice == '5':
            print("Exiting the app. Goodbye!")
            logging.info("User exited the app.")
            break
        else:
            print("Invalid input. Please try again.")

def add_item_screen():
    print("\n--- Add Item Screen ---")
    name = input("Enter item name: ").strip()
    try:
        quantity = int(input("Enter quantity: ").strip())
        price = float(input("Enter price per item: $").strip())
    except ValueError:
        print("Invalid input. Quantity must be an integer and price a number.")
        return

    if name:
        shopping_list.append({'name': name, 'quantity': quantity, 'price': price})
        print(f"Added: {name} (x{quantity}) at ${price:.2f} each")
        logging.info(f"Added item: {name} x{quantity} @ ${price:.2f}")
    else:
        print("Item name cannot be empty.")

def view_list_screen():
    while True:
        print("\n--- View Shopping List ---")
        if not shopping_list:
            print("Your shopping list is empty.")
            return

        for idx, item in enumerate(shopping_list, 1):
            total = item['price'] * item['quantity']
            print(f"{idx}. {item['name']} (x{item['quantity']}) - ${total:.2f}")

        print("\nOptions: [e] Edit | [d] Delete | [b] Back to Home")
        action = input("Select an option: ").strip().lower()

        if action == 'b':
            break
        elif action in ('e', 'd'):
            index = input("Enter item number to modify: ").strip()
            try:
                idx = int(index) - 1
                if action == 'e':
                    edit_item_screen(idx)
                elif action == 'd':
                    deleted = shopping_list.pop(idx)
                    print(f"Deleted: {deleted['name']}")
                    logging.info(f"Deleted item: {deleted['name']}")
            except (ValueError, IndexError):
                print("Invalid item number.")
        else:
            print("Invalid option.")

def edit_item_screen(index):
    item = shopping_list[index]
    print(f"\n--- Edit Item Screen ---")
    print(f"Editing: {item['name']} (x{item['quantity']}) at ${item['price']:.2f}")
    new_name = input("Enter new name (leave blank to keep current): ").strip()
    try:
        new_qty = input("Enter new quantity (leave blank to keep current): ").strip()
        new_qty = int(new_qty) if new_qty else item['quantity']
        new_price = input("Enter new price (leave blank to keep current): ").strip()
        new_price = float(new_price) if new_price else item['price']
    except ValueError:
        print("Invalid input. Quantity must be an integer and price a number.")
        return

    item['name'] = new_name if new_name else item['name']
    item['quantity'] = new_qty
    item['price'] = new_price

    shopping_list[index] = item
    print("Item updated.")
    logging.info(f"Updated item: {item['name']} x{item['quantity']} @ ${item['price']:.2f}")

def settings_screen():
    print("\n--- Settings Screen ---")
    print("1. Clear Shopping List")
    print("2. Back to Home")
    choice = input("Select an option: ").strip()
    if choice == '1':
        confirm = input("Are you sure you want to clear the list? (y/n): ").strip().lower()
        if confirm == 'y':
            shopping_list.clear()
            print("Shopping list cleared.")
            logging.info("Shopping list cleared by user.")
    elif choice == '2':
        return
    else:
        print("Invalid option.")

def checkout_screen():
    if not shopping_list:
        print("Shopping list is empty.")
        return

    subtotal = sum(item['price'] * item['quantity'] for item in shopping_list)
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    print(f"\nSubtotal: ${subtotal:.2f}")
    print(f"Tax (7%): ${tax:.2f}")
    print(f"Total with tax: ${total:.2f}")

    logging.info(f"Checkout - Subtotal: ${subtotal:.2f}, Tax: ${tax:.2f}, Total: ${total:.2f}")

def main():
    print("Welcome to the Shopping List App (Fixed Tax Version)!")
    home_screen()

if __name__ == "__main__":
    main()
