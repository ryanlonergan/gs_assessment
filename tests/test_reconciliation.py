import pandas as pd

from reconciliation import calculate_quantity_change, reconciliation_analysis


def test_reconciliation_logic():
    # Create dummy data for testing
    df_old = pd.DataFrame({'sku': ['A1', 'A2', 'A4', 'A5'], 'quantity': [10, 15, 10, 7]})
    df_new = pd.DataFrame({'sku': ['A1', 'A3', 'A4', 'A5'], 'quantity': [15, 22, 5, 7]})

    # 1. Test reconciliation_analysis()
    merged = reconciliation_analysis(df_old, df_new)
    assert merged.loc[0, 'status'] == 'Retained'
    assert merged.loc[1, 'status'] == 'Removed'
    assert merged.loc[2, 'status'] == 'New'

    # 2. Test calculate_quantity_change()
    processed = calculate_quantity_change(merged, 'quantity_old', 'quantity_new')
    assert processed.loc[0, 'inventory_change'] == 5
    assert processed.loc[3, 'inventory_change'] == -5
    assert processed.loc[4, 'inventory_change'] == 0

    print("All tests passed successfully")


if __name__ == "__main__":
    test_reconciliation_logic()