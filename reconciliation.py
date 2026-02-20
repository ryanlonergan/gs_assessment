import pandas as pd


def reconciliation_analysis(snapshot_old, snapshot_new):
    """
    Merges two snapshots and adds a 'status' column to the new snapshot dataframe.

    Performs a full outer join to combine the data from the two input snapshots. It then
    creates a 'status' column using the indicator parameter from the merge and assigns values
    based on the status_map dictionary.

    :param snapshot_old: DataFrame containing the older snapshot data
    :param snapshot_new: DataFrame containing the newer snapshot data
    :return: DataFrame containing the merged snapshot data including a new 'status' column
    """

    # Merge snapshots on 'sku' while retaining both old and new values
    merged = pd.merge(snapshot_old, snapshot_new, on='sku', how='outer', indicator='status', suffixes=('_old', '_new'))

    # Add a status based on the type of merge to differentiate SKU retention
    status_map = {
        'left_only': 'Removed',
        'right_only': 'New',
        'both': 'Retained'
    }

    merged['status'] = merged['status'].map(status_map)

    return merged


def calculate_quantity_change(df, old_quantity='quantity_old', new_quantity='quantity_new'):
    """
    Calculates the change in quantity between two quantity columns in a df.

    Makes a copy of the df to prevent slice errors and subtracts the newer quantity from
    the older quantity.

    :param df: DataFrame containing the quantity levels
    :param old_quantity: Column name for the older snapshot quantity
    :param new_quantity: Column name for the newer snapshot quantity
    :return: A new calculated column that records the difference between the two snapshot
     quantities
    """

    df = df.copy()

    df['inventory_change'] = df[new_quantity] - df[old_quantity]

    return df


## Import snapshot data

snapshot_1 = pd.read_csv('data/snapshot_1.csv')
snapshot_2 = pd.read_csv('data/snapshot_2.csv')

# rename snapshot_2's columns to match snapshot_1's assuming they have the same column data in the same column order
snapshot_2.columns = snapshot_1.columns


## Cleaning

# cleans the sku's to have uppercase letters for the 'SKU' part of their item code
snapshot_2['sku'] = snapshot_2['sku'].str.upper()
# adds a dash between the first capture group ('SKU') and second capture group (###)
snapshot_2['sku'] = snapshot_2['sku'].str.replace(r'(SKU)(\d+)', r'\1-\2', regex=True)

# find duplicated sku's
df_duplicates = snapshot_2[snapshot_2.duplicated(subset='sku', keep=False)]

# groups and merges duplicated sku's
agg_rules = {
    'sku': 'first', # takes first value that appears
    'name': 'last', # changed to last for matching names between snapshots - unsure what official name is
    'quantity': 'sum',
    'location': 'first',
    'last_counted': 'first'
}

snapshot_2 = snapshot_2.groupby('sku', as_index=False).agg(agg_rules)

# Remove whitespaces in names
snapshot_1['name'] = snapshot_1['name'].str.strip()
snapshot_2['name'] = snapshot_2['name'].str.strip()

# Change data type of snapshot_2's 'quantity' column to match snapshot_1's
snapshot_2['quantity'] = snapshot_2['quantity'].astype(snapshot_1['quantity'].dtype)

# Normalize date format for snapshot_2's 'last_counted' column
snapshot_2['last_counted'] = pd.to_datetime(snapshot_2['last_counted'], format='mixed')
snapshot_2['last_counted'] = snapshot_2['last_counted'].dt.strftime('%Y-%m-%d')


## Reconciliation Work

# Identify new, removed and retained items and assign them a status
reconciliation_df = reconciliation_analysis(snapshot_1, snapshot_2)

# Create new df's that separate items's based on status
# dropna removes empty columns for slices
new_df = reconciliation_df[reconciliation_df['status'] == 'New'].dropna(axis=1, how='all').copy()
removed_df = reconciliation_df[reconciliation_df['status'] == 'Removed'].dropna(axis=1, how='all').copy()
retained_df = reconciliation_df[reconciliation_df['status'] == 'Retained'].copy()

# Find quantity changes for retained items
retained_df = calculate_quantity_change(retained_df)


## Clean up output df's

# Remove Unneeded Columns
new_df.drop(columns=['status'], inplace=True)
removed_df.drop(columns=['status'], inplace=True)
retained_df.drop(columns=['status', 'name_new'], inplace=True)

# Rename column suffixes that are no longer needed
new_df.rename(columns={
    'name_new': 'name',
    'quantity_new': 'quantity',
    'location_new': 'location',
    'last_counted_new': 'last_counted'
}, inplace=True)

removed_df.rename(columns={
    'name_old': 'name',
    'quantity_old': 'quantity',
    'location_old': 'location',
    'last_counted_old': 'last_counted'
}, inplace=True)

retained_df.rename(columns={
    'name_old': 'name',
}, inplace=True)

# Change quantity related columns to integers
new_df['quantity'] = new_df['quantity'].astype('int64')
removed_df['quantity'] = removed_df['quantity'].astype('int64')
retained_df['quantity_old'] = retained_df['quantity_old'].astype('int64')
retained_df['quantity_new'] = retained_df['quantity_new'].astype('int64')
retained_df['inventory_change'] = retained_df['inventory_change'].astype('int64')

# Reindex retained_df for readability
retained_df= retained_df.reindex(columns=[
    'sku',
    'name',
    'location_old',
    'location_new',
    'last_counted_old',
    'last_counted_new',
    'quantity_old',
    'quantity_new',
    'inventory_change'])


## Reconciliation Reports Output

# Retrieve timestamp date for latest snapshot
latest_snapshot_date = retained_df['last_counted_new'][1]

# Output reconciliation reports to csv files with timestamps included
new_df.to_csv(f'output/new_items_{latest_snapshot_date}.csv', index=False)
removed_df.to_csv(f'output/removed_items_{latest_snapshot_date}.csv', index=False)
retained_df.to_csv(f'output/retained_items_{latest_snapshot_date}.csv', index=False)
