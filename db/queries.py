CREATE_DATABASE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_products VARCHAR(255),
    category VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    article VARCHAR(255),
    photo TEXT
    )
"""


INSERT_PRODUCTS = """
    INSERT INTO products (name_products, category, size, price, article, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""
