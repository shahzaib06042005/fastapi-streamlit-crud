from fastapi import FastAPI, HTTPException
from models import Item
from database import get_connection, init_db

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI CRUD! Visit route/items to see data."}

# Initialize DB when API starts
init_db()

# --- CREATE ---
@app.post("/items/")
def create_item(item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price, description) VALUES (?, ?, ?)",
                   (item.name, item.price, item.description))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"message": "Item created successfully", "item_id": item_id}

# --- READ ALL ---
@app.get("/items/")
def get_all_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return [dict(row) for row in items]

# --- READ ONE ---
@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)

# --- UPDATE ---
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=?, price=?, description=? WHERE id=?",
                   (item.name, item.price, item.description, item_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated successfully"}

# --- DELETE ---
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
