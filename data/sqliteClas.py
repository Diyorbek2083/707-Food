import sqlite3

class SQLiteBaza:
    def __init__(self, db_name):
        """YANGI DATABASE YARATISH"""
        self.db_name = db_name
        with sqlite3.connect(db_name) as self.connection:
            self.cursor = self.connection.cursor()

    def create_table(self, table_name, malumotlar):
        """YANGI TABLE YARATISH"""
        malumot_name = ", ".join(f"{tage_name} {type_name}" for tage_name, type_name in malumotlar.items())
        create_table = f"CREATE TABLE {table_name} ({malumot_name});"
        self.cursor.execute(create_table)
        self.connection.commit()
        
    def insert(self, table_name, **kwargs):
        """TABLEGA MALUMOT QOSHISH"""
        malumot = ", ".join(kwargs.keys())
        belgilanuvchi = ", ".join('?' for _ in kwargs)
        values = tuple(kwargs.values())
        insert_table = f"INSERT INTO {table_name} ({malumot}) VALUES ({belgilanuvchi});"
        self.cursor.execute(insert_table, values)
        self.connection.commit()

    def read(self, table_name, yulduz="*",where_name = None):
        """TABLENI ICHIDAGI MALUMOTNI O'QISH"""
        if where_name:
            select_from = f"SELECT {yulduz} FROM {table_name} WHERE {where_name};"
        else:
            select_from = f"SELECT {yulduz} FROM {table_name};"
        self.cursor.execute(select_from)
        chiqan_malumot = self.cursor.fetchall()
        return chiqan_malumot if chiqan_malumot else None
    
    def update(self, table_name, yangi_name, manzil_name):
        """TABLEDAGI MALUMOTLARNI O'ZGARTIRISH"""
        yangi_malumot = f"UPDATE {table_name} SET {yangi_name} WHERE {manzil_name}"
        self.cursor.execute(yangi_malumot)
        self.connection.commit()
    
    def delete(self, table_name, manzil_name):
        """TABLEDAGI MALUMOTLARNI O'CHIRISH QATORI BILAN"""
        delete_table = f"DELETE FROM {table_name} WHERE {manzil_name}"
        self.cursor.execute(delete_table)
        self.connection.commit()

    def yangi_ustun(self, table_name, ustun_name, ustun_tipi):
        """TABLEGA YANGI USTUN QO'SHADI"""
        alter_table = f"ALTER TABLE {table_name} ADD {ustun_name} {ustun_tipi};"
        self.cursor.execute(alter_table)
        self.connection.commit()
    def new_name(self, table_name, new_name):
        """TABLE NOMINI O'ZGARTIRADI"""
        yangi_ism = f"ALTER TABLE {table_name} RENAME TO {new_name};"
        self.cursor.execute(yangi_ism)
        self.connection.commit()

    def drop_table(self, table_name):
        """TABLENI O'CHIRADI"""
        table = f"DROP TABLE {table_name};"
        self.cursor.execute(table)
        self.connection.commit()
    
    def close(self):
        """DATABASENI YOPIB KETADI"""
        self.connection.close()



# data = SQLiteBaza("SQLite/database")

# data.create_table("database", {
#     "tuman_id" : "INTEGER PRIMARY KEY NOT NULL",
#     "tuman_name" : "TEXT NOT NULL",
#     "ism" : "TEXT"
# })

# data.insert("database", tuman_name = "Urganch", ism = "Asadbek")

# print(data.read("database",yulduz="*", where_name="ism = 'Asadbek'"))

# data.update("database",yangi_name='ism = "Shohruh"',manzil_name="tuman_id = 1")

# data.delete("database", 'tuman_id = 1')

# data.alter_table("database", "adres", "TEXT")

# data.new_name("database", "test1")

# data.drop_table("test1")