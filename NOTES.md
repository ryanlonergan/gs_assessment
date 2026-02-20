### Approach

I began the assessment focusing on EDA to identify and resolve data quality issues  as they were identified. Once I had a clean data foundation to work with, I developed the reconciliation logic and performed manual validation to cross-reference my outputs with the original reports. My workflow involved prototyping the logic in a Python notebook for flexibility, then refactoring that code into a clean, consolidated Python script. Finally, I implemented tests for the reconciliation logic to ensure it handled data reliably and performed as expected under different conditions.


### Assumptions

Given the timeframe and available data context, this analysis relies on the following assumptions:

- Snapshot_1 is cleaner than Snapshot_2 and should be used as the greater source of truth between the two snapshots.
- The snapshot columns represent the same data, but the columns were named differently between exports.
- SKU's that don't follow the same format ('SKU-###') are from unclean data entry and do not represent new items.
- Duplicated SKU's are from data entry/item transfer errors and the quantities can be logically combined.
- Item names should not change between snapshots, but data quality or manual entry can introduce errors.
- Item quantities can not be negative or fractional and can be converted to integers once data quality issues are handled.


### Data Issues

Most of the data issues I ran into seem to stem from manual entry. It seems strict constraints on columns like 'sku' or 'last_counted,' are not enforced, creating messy data that requires extra normalization. I also noticed that column names shifted between snapshots which should not normally happen. These issues are fixable, but the ETL pipeline probably needs to be investigated to prevent further errors and manual cleaning work later.

One specific catch was a 'sku' that showed up twice in the second snapshot. They shared the same 'sku' code but had different names indicating a possible manual entry for a warehouse transfer. I merged the records to keep the analysis accurate, but using a central product table as the 'source of truth' should be investigated further  avoid this kind of duplication.

Here is the full list of data issues I identified:

    column names change between snapshots
        name to product_name
        quantity to qty
        location to warehouse
        last_counted to updated_at
    sku
        format (missing dash)
        duplicates
    name
        whitespace
        names matches between skus
    quantity
        decimals
        negative values (handled through duplicated sku merge)
    location
        (none found)
    last_counted
        date format
