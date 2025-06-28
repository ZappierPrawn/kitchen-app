# All logic

#imports
import sqlite3

DB_PATH = "data/inventory.db"

#load inventory from stored SQLite table, return as dict
def load_inventory(db_path = None):
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name, quantity, unit FROM inventory")
    rows = cur.fetchall()

    conn.close()

    #build a dict

    inventory = {
        name: {"quantity": qty, "unit": unit}
        for name, qty, unit in rows
    }
    return inventory

#save inventory to the SQLite table
def save_inventory(data: dict, db_path=None):
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory")  # nuke old rows
    for name, props in data.items():
        cur.execute(
            "INSERT INTO inventory(name, quantity, unit) VALUES (?, ?, ?)",
            (name, props["quantity"], props["unit"])
        )
    conn.commit()
    conn.close()


#add ingredient to table and save
def add_ingredient(name: str, qty:float, unit: str, db_path = None):
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""INSERT OR REPLACE INTO inventory(name, quantity, unit) VALUES (?, ?, ?)""", (name, qty, unit))

    conn.commit()
    conn.close()

#remove ingredients entered
def remove_ingredient(name: str, db_path=None):
    db_path = db_path or DB_PATH
    conn    = sqlite3.connect(db_path)
    cur     = conn.cursor()

    cur.execute("DELETE FROM inventory WHERE name = ?", (name,))

    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


#update ingredient counts
def update_ingredient(name: str, qty: float = None, unit = None, db_path = None):
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    fields, params = [], []
    if qty is not None:
        fields.append("quantity = ?")
        params.append(qty)
    if unit is not None:
        fields.append("unit = ?")
        params.append(unit)

    if not fields:
        conn.close()
        return False  # nothing to update

    params.append(name)  # WHERE name = ?
    sql = f"UPDATE inventory SET {', '.join(fields)} WHERE name = ?"
    cur.execute(sql, params)
    updated = cur.rowcount > 0

    conn.commit()
    conn.close()
    return updated


#list everything in the table
def list_inventory(db_path = None):
    inventory = load_inventory(db_path)
    print(inventory)
    return load_inventory(db_path)

#set low amount
def set_threshold(name: str, threshold: float, db_path=None):
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE inventory SET threshold = ? WHERE name = ?",
        (threshold, name)
    )
    updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    return updated


#check for low amounts
def check_threshold(db_path=None):
    db = db_path or DB_PATH
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT name, quantity, unit, threshold
        FROM inventory
        WHERE threshold IS NOT NULL
          AND quantity < threshold
        """
    )
    rows = cur.fetchall()
    conn.close()

    return {
        name: {"quantity": qty, "unit": unit, "threshold": th}
        for name, qty, unit, th in rows
    }
