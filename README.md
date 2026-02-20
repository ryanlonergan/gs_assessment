Assumptions
- Snapshot_1 is cleaner than Snapshot_2 and should be used as the greater source of truth between the two snapshots.
- The snapshot columns represent the same data, but the columns were named differently between exports.
- SKU's that don't follow the same format ('SKU-###') are from unclean data entry and do not represent new items.
- Duplicated SKU's are from data entry/item transfer errors and the quantities can be logically combined.
- Item names should not change between snapshots, but data quality or manual entry can introduce errors.
- Item quantities can not be negative or fractional and can be converted to integers once data quality issues are found.