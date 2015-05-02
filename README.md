# National Homebrewing Competition (NHC) Gold medal data set

All gold-medal winning recipes from NHC in a sql database.

## Why?

To answer those burning questions:

**How many winning IPAs used cascade vs how many used amarillo?**:

    $ sqlite3 nhc.db 'select count(*) from recipes where style="India Pale Ale" and ingredients like "%amarillo%"'
     7

    $ sqlite3 nhc.db 'select count(*) from recipes where style="India Pale Ale" and ingredients like "%cascade%"'
     3

**How many winning recipes in the past decade used SafAle yeast?**

    $ sqlite3 nhc.db 'select count(*) from recipes where ingredients like "%safale%"'
     2

**What are the most common batch sizes at NHC?**

    $ sqlite3 nhc.db 'select vol from recipes' | sort | uniq -c | sort -rn | head -5
     52 5 Gallons (18.93 L)
     25 6 Gallons (22.71 L)
     24 5 Gallons (19 L)
     19 6 Gallons (22.7 L)
     19 5.5 Gallons (20.82 L)