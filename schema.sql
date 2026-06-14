
-- Collection Centers Table
CREATE TABLE CollectionCenter (
    center_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_name TEXT NOT NULL,
    location TEXT NOT NULL
);

-- Waste Collection Table
CREATE TABLE WasteCollection (
    collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_id INTEGER NOT NULL,
    waste_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    collection_date TEXT NOT NULL,
    FOREIGN KEY (center_id) REFERENCES CollectionCenter(center_id)
);

-- Recycling Plants Table
CREATE TABLE RecyclingPlant (
    plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity_per_day INTEGER NOT NULL
);

-- Recycling Records Table
CREATE TABLE RecyclingRecord (
    recycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id INTEGER NOT NULL,
    plant_id INTEGER NOT NULL,
    recycled_quantity INTEGER NOT NULL,
    recycling_date TEXT NOT NULL,
    FOREIGN KEY (collection_id) REFERENCES WasteCollection(collection_id),
    FOREIGN KEY (plant_id) REFERENCES RecyclingPlant(plant_id)
);

