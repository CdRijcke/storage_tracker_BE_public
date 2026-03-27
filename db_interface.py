from storage_tracker.database.db import get_product, update_product


product_oats = get_product("oat_flakes")
update_product(product_oats, 3)

product_peanutbutter = get_product("peanutbutter")
update_product(product_peanutbutter, 1)
