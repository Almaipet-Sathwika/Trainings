from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="🛍️ E-Commerce Backend")

# ---------------------------
# Database Setup
# ---------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Customer Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        address TEXT
    )
    """)

    # Product Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Models
# ---------------------------
class Customer(BaseModel):
    name: str
    email: str
    address: str | None = None

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float

# ---------------------------
# Customer Routes
# ---------------------------
@app.post("/customers/")
def create_customer(customer: Customer):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)",
                       (customer.name, customer.email, customer.address))
        conn.commit()
        return {"message": "Customer created successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists.")
    finally:
        conn.close()

@app.get("/customers/")
def get_all_customers():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    conn.close()
    return {"customers": data}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return {"customer": customer}
    raise HTTPException(status_code=404, detail="Customer not found.")

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Customer not found.")
    cursor.execute("UPDATE customers SET name = ?, email = ?, address = ? WHERE id = ?",
                   (customer.name, customer.email, customer.address, customer_id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully."}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted."}

# ---------------------------
# Product Routes
# ---------------------------
@app.post("/products/")
def create_product(product: Product):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                   (product.name, product.description, product.price))
    conn.commit()
    conn.close()
    return {"message": "Product created successfully!"}

@app.get("/products/")
def get_all_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return {"products": products}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if product:
        return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found.")

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Product not found.")
    cursor.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
                   (product.name, product.description, product.price, product_id))
    conn.commit()
    conn.close()
    return {"message": "Product updated successfully."}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"message": "Product deleted."}




#---------------to run -----------
# uvicorn main:app --reload
