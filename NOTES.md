### Assumptions
- Snapshot_1 is cleaner than Snapshot_2 and should be used as the greater source of truth between the two snapshots.
- The snapshot columns represent the same data, but the columns were named differently between exports.
- SKU's that don't follow the same format ('SKU-###') are from unclean data entry and do not represent new items.
- Duplicated SKU's are from data entry/item transfer errors and the quantities can be logically combined.
- Item names should not change between snapshots, but data quality or manual entry can introduce errors.
- Item quantities can not be negative or fractional and can be converted to integers once data quality issues are handled.

### Data Issues

The majority of the data issues I found most likely stem from manual data entry. 

A comprehensive list of data issues I found include:

    column names change between files
        name to product_name
        quantity to qty
        location to warehouse
        last_counted to updated_at
    sku
        format (missing dash)
        capital letters
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