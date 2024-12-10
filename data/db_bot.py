from data.sqliteClas import SQLiteBaza

baza = SQLiteBaza("imtihon.db")

# baza.create_table("admins",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     "tg_id":"INTEGER",
#     "name":"TEXT",
#     "number":"TEXT"
# })
# baza.create_table("categoriya",{
#     'id':"INTEGER PRIMARY KEY NOT NULL",
#     "name":"TEXT",
#     "rasmi":"TEXT"
# })
# baza.create_table("product",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     "name":"TEXT",
#     "narxi":"TEXT",
#     "rasm":"TEXT",
#     "c_id":'TEXT'
# })
# baza.create_table("users",{
#     "id":'INTEGER PRIMARY KEY NOT NULL',
#     "tg_id":"INTEGER",
#     "user":"TEXT"
# })
# baza.create_table("malumotlar",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     'tel':"TEXT",
#     "tg":"TEXT",
#     "insta":"TEXT",
#     "kanal":"TEXT"
# })
# baza.create_table("coment",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     "tg_id":"INTEGER",
#     "user":"TEXT",
#     "coment":"TEXT"
# })
# baza.create_table("savat",{
#     "id":"INTEGER PRIMARY KEY NOT NULL",
#     "tg_id":"INTEGER",
#     "user":"TEXT",
#     "name":"TEXT",
#     "narxi":"INTEGER",
#     "soni":"INTEGER"
# })


admins = baza.read("admins","*")
users = baza.read("users","*")

def AdminsId():
    id = []
    for i in baza.read(f"admins","*"):
        id.append(i[1])
    return id

def UsersId():
    id = []
    for i in baza.read(f"users","*"):
        id.append(i[1])
    return id

# print(type(UserId()))
