def quantity_update(db, name, param):
    cursor = db.cursor()
    cursor.execute("""UPDATE product SET quantity = quantity + ?
                   WHERE name = ?""", [param, name])
    cursor.execute("""UPDATE product SET updates = updates + 1
                   WHERE name = ?""", [name])
    db.commit()

def price_abs(db, name, param):
    cursor = db.cursor()
    cursor.execute("""UPDATE product SET price = price + ?
                   WHERE name = ?""", [param, name])
    cursor.execute("""UPDATE product SET updates = updates + 1
                   WHERE name = ?""", [name])
    db.commit()

def price_percent(db, name, param):
    cursor = db.cursor()
    cursor.execute("""UPDATE product SET price = price * (1 + ?)
                   WHERE name = ?""", [param, name])
    cursor.execute("""UPDATE product SET updates = updates + 1
                   WHERE name = ?""", [name])
    db.commit()

def remove_product(db, name, param):
    cursor = db.cursor()
    cursor.execute("""DELETE FROM product 
                   WHERE name = ?""", [name])
    db.commit()

def update_available(db, name, param):
    param = 'True' if param else 'False'
    cursor = db.cursor()
    cursor.execute("""UPDATE product SET isAvailable = ?
                   WHERE name = ?""", [param, name])
    cursor.execute("""UPDATE product SET updates = updates + 1
                   WHERE name = ?""", [name])
    db.commit()
