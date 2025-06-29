import sqlite3 as sq        
from db import DATABASE     # make sure DB name is defined in db.py! 

# insert object into DB from JSON obj, replace attributes as needed
def insertPlant(data):
    """
    Inserts the given object into the DB based on attribute + value. Assumes 
    that JSON object keys are of the same name as the attributes in the table.

    :param data:    JSON object with appropriate DB object attributes
                    (note: does not need ID # if int is primary key in DB)
    """
    # assign values based on object keys to the respective variables
    genus = data["genus"]
    species = data["species"]
    statusID = data["statusID"]
    qty = data["qty"]
    wishlist = data["wishlist"]
    
    # process any values that aren't already handled by the front end...
    if wishlist == 1:
        qty = 0
        statusID = None  # no status for wishlist

    # now insert values into the DB based on previously defined columns
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()

        # make sure that the values inserted use :placeholder format
        c.execute("""INSERT INTO plants (genus, species, statusID, qty, wishlist)
                    VALUES (:genus, :species, :statusID, :qty, :wishlist)""",

                    {'genus': genus, 'species': species, 'statusID' : statusID, 
                     'qty': qty, 'wishlist' : wishlist})

# return all litems in table, replace table names as needed
def getPlants():
    """Fetch all rows from the table and return them as a list of dicts"""
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("""
            SELECT 
                plants.plantID, 
                plants.genus, 
                plants.species, 
                plants.qty, 
                plants.wishlist, 
                statuses.status
            FROM plants
            LEFT JOIN statuses ON plants.statusID = statuses.statusID
        """)
        rows = c.fetchall()
        return [dict(row) for row in rows]  


# return all owned plants (non-wishlist)
def getOwnedPlants():
    """Fetches all rows from the table and return them as a list of dicts"""
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("""
            SELECT 
                plants.plantID, 
                plants.genus, 
                plants.species, 
                plants.qty, 
                plants.wishlist, 
                statuses.status
            FROM plants
            LEFT JOIN statuses ON plants.statusID = statuses.statusID
            WHERE qty > 0
        """)
        rows = c.fetchall()
        return [dict(row) for row in rows]


# return all wishlist plants
def getWishlistPlants():
    """Fetches all rows from the table and return them as a list of dicts"""
    with sq.connect(DATABASE) as conn:
        conn.row_factory = sq.Row
        c = conn.execute("""
            SELECT 
                plants.plantID, 
                plants.genus, 
                plants.species, 
                plants.qty, 
                plants.wishlist, 
                statuses.status
            FROM plants
            LEFT JOIN statuses ON plants.statusID = statuses.statusID
            WHERE wishlist = 1
        """)
        rows = c.fetchall()
        return [dict(row) for row in rows]


# return a plant by ID (no front end use yet...)
def getByID(id):
    """Fetches a specific plant by ID and returns it as a dict

    :SQL: 'SELECT * FROM plants WHERE plantID = :id' """
    with sq.connect(DATABASE) as conn:
        # create parser for row and fetch instance of a plant
        conn.row_factory = sq.Row
        c = conn.execute(
            'SELECT * FROM plants WHERE plantID = :id', {'id': id})
        plant = c.fetchone()
        return dict(plant) if plant else None


# TODO: get plants by genus
# TODO: get plants by status

# delete a plant by ID
def deletePlant(id):
    """Deletes a specific row by ID

    :SQL: 'SELECT * FROM plants WHERE plantID = :id' """
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM plants WHERE plantID = :id", {'id' : id})
        conn.commit()
    
    print(f"deleted row with id {id} in table (in DB)")


# update a plant (note: this requires you to pass the plant to front end 
# initially to pre-fill these fields & ensure the user sees OG values)
def updatePlant(data):
    """ Updates a DB item on any variables changed in the front end. Assumes 
    that the given JSON object has all of the needed keys.

    :param:     JSON object with appropriate DB object attributes
    """

    id = data["plantID"]
    genus = data["genus"]
    species = data["species"]
    statusID = data["statusID"]
    qty = data["qty"]
    wishlist = data["wishlist"]
    
    # if set to wishlist, reset qty + status
    if wishlist == 1:
        qty = 0
        statusID = None

    # Update all variables as needed
    with sq.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""UPDATE plants SET 
                  genus = :genus, 
                  species = :species, 
                  statusID = :statusID, 
                  qty = :qty, 
                  wishlist = :wishlist
                  WHERE plantID = :plantID
                  """, {
                      'genus': genus, 
                      'species': species, 
                      'statusID' : statusID, 
                      'qty': qty, 
                      'wishlist' : wishlist,
                      'plantID' : id})
        conn.commit()

# TODO: make fields update-able in-table? May require a function to fetch the
# the attributes individually 


