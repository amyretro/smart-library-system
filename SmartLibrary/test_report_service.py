from services.report_service import (
    get_sales_report,
    get_purchases_report,
    get_inventory_report,
    get_profit_report
)

def test_report_service():
    print("\n--- Testing Sales Report ---")
    sales = get_sales_report()
    print(sales)
    assert isinstance(sales, dict)
    assert "total_sales" in sales
    assert "total_quantity_sold" in sales
    assert "total_revenue" in sales
    print("Sales report test passed.")

    print("\n--- Testing Purchases Report ---")
    purchases = get_purchases_report()
    print(purchases)
    assert isinstance(purchases, dict)
    assert "total_purchases" in purchases
    assert "total_quantity_purchased" in purchases
    assert "total_cost" in purchases
    print("Purchases report test passed.")

    print("\n--- Testing Inventory Report ---")
    inventory = get_inventory_report()
    print(inventory)
    assert isinstance(inventory, list)

    if inventory:
        assert isinstance(inventory[0], dict)
        assert "book_id" in inventory[0]
        assert "title" in inventory[0]
        assert "total_quantity" in inventory[0]
        assert "available_quantity" in inventory[0]
        assert "borrowed_quantity" in inventory[0]

    print("Inventory report test passed.")

    print("\n--- Testing Profit Report ---")
    profit = get_profit_report()
    print(profit)
    assert isinstance(profit, dict)
    assert "total_revenue" in profit
    assert "cost_of_goods_sold" in profit
    assert "gross_profit" in profit
    print("Profit report test passed.")

    print("\nPASS: All report service tests succeeded.")

if __name__ == "__main__":
    test_report_service()