#CLI layer
import argparse
from src.inventory import add_ingredient, list_inventory, remove_ingredient, update_ingredient, load_inventory, set_threshold, check_threshold

def main():
    args = parser.parse_args()

    if args.command == "add":
        add_ingredient(args.name, args.qty, args.unit)
        print(f"{args.qty} {args.unit} of {args.name} added to inventory.")
    elif args.command == "list":
        inv = list_inventory()
        for name, info in inv.items():
            print(f"{name}: {info['quantity']} {info['unit']}")
    elif args.command == "remove":
        success = remove_ingredient(args.name)
        if success:
            print(f"{args.name} removed.")
        else:
            print(f"No ingredient named {args.name}.")
    elif args.command == "update":
        check = update_ingredient(args.name, qty=args.qty, unit=args.unit)
        if check:
            print("Updated ingredients.")
        else:
            print(f"Failed to update {args.name!r}")
    elif args.command == "check":
        alerts = check_threshold()
        if alerts:
            print("Low stock:")
            for n, p in alerts.items():
                print(f"  {n}: {p['quantity']} {p['unit']} (<{p['threshold']})")
        else:
            print("All stock levels are OK.")
    elif args.command == "set-threshold":
        check = set_threshold(args.name, args.threshold)
        if check:
            print("Threshold set.")
        else:
            print("Ingredient not found.")



parser = argparse.ArgumentParser(prog="kitchen-app")
subparsers = parser.add_subparsers(dest="command", required=True)

#add parser
add_p = subparsers.add_parser("add", help="Add or overwrite an ingedient")
add_p.add_argument("name", help="Ingredient name")
add_p.add_argument("qty", type=float, help="Total quantity")
add_p.add_argument("unit", help="Unit of measure")

#list parser
list_p = subparsers.add_parser("list", help="List all ingredients or specific one")
list_p.add_argument("name", nargs="?", help="(Optional) Name of the ingredient to list")

#remove parser
remove_p = subparsers.add_parser("remove", help="Remove an ingredient")
remove_p.add_argument("name", help ="Remove a specific ingredient from the table")

#update parser
upd_p = subparsers.add_parser("update", help="Change quantity and/or unit of an ingredient")
upd_p.add_argument("name")
upd_p.add_argument("qty", nargs="?", type=float, help="New quantity (omit to leave unchanged)", default=None)
upd_p.add_argument("unit", nargs="?", help="New unit (omit to leave unchanged)", default=None
)

#check parser
chk_p = subparsers.add_parser("check", help="Show ingredients below their low-stock threshold")

#set threshold parser
th_p = subparsers.add_parser(
    "set-threshold", help="Assign a low-stock threshold for an ingredient")
th_p.add_argument(
    "name", help="Name of the ingredient to set a threshold for")
th_p.add_argument(
    "threshold", type=float, help="Threshold quantity (below this triggers a low-stock alert)")

if __name__== "__main__":
    main()