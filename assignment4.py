'''  DO:  more $HOME/.my.cnf to see your MySQL username and  password
#  CHANGE:  MYUSERNAME and MYMYSQLPASSWORD in the test section of
#  this program to your username and mysql password
#  RUN: Python3 python_db_connector.py '''

import mysql.connector
from tabulate import tabulate


# database access functions #



def open_database(hostname, user_name, mysql_pw, database_name):
    global conn
    conn = mysql.connector.connect(host=hostname,
                                   user=user_name,
                                   password=mysql_pw,
                                   database=database_name
                                   )
    global cursor
    cursor = conn.cursor()
    if conn:
        print("connected to database",database_name)
    else:
        print("can not connect to database",database_name)


def printFormat(result):
    header = []
    for cd in cursor.description:  # get headers
        header.append(cd[0])
    print('')
    print('Query Result:')
    print('')
    print(tabulate(result, headers=header))  # print results in table format

# select and display query


def executeSelect(query):
    
    try:
        cursor.execute(query)
        printFormat(cursor.fetchall())
    
    except Exception as e:
        print(e)

def insert(table, values):
    
    try:
        query = "INSERT into " + table + " values (" + values + ")" + ';'
        cursor.execute(query)
        conn.commit()
        
    except Exception as e:
        print(e)
        


def executeUpdate(query):  # use this function for delete and update
    
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print("Error: " + e)


def close_db():  # use this function to close db
    cursor.close()
    conn.close()

def create_table(sql):
    cursor.execute(sql)
    conn.commit()
    
def drop_table(table):
    cursor.execute('drop table if exists ' +  table)
    conn.commit()

##### Test #######
mysql_username = 'krasguer'  # please change to your username
mysql_password = 'EiThahy4'  # please change to your MySQL password
mysql_database = 'krasguer'
open_database('localhost', mysql_username, mysql_password,
              mysql_database)  # open database



# menu functiuons #


# Inventory check. Find all suppliers, tea names, inventory on hand
def inventory_check():
    print("inventory check")
    query = "select ITEM.NAME AS Item, SUPPLIER.NAME as SUPPLIER ,ITEM.QUANTITY from ITEM,SUPPLIER "
    query += "WHERE ITEM.SUPPLIER_ID = SUPPLIER.ID"
    executeSelect(query)


# Add a new supplier with item(s) that they provide.
# INSERT INTO SUPPLIER VALUES (ID, 'NAME','PHONE', 'EMAIL');
def add_supplier():
    print("add supplier")

    # get inputs
    
    id = input("Enter ID: ")
    name = input("Enter name: ")
    while name=="":
        name = input("Enter name: ")
        
    phone = input("Enter phone: ")
    while phone=="":
        phone = input("Enter phone: ")
    
    email = input("Enter email: ")
    while email=="":
        email = input("Enter email: ")
        
    # makevalues    
    values = id + ",'" + name + "','" + phone + "','" + email + "'";
    
    # insert into data base
    insert("SUPPLIER", values)
    
    
    # show supplier
    executeSelect("select * from SUPPLIER where ID = " + id)
    

# Close day. Calculate all the tips (15% of the TOTAL),
# update the totals (TOTAL - GRATUITY)
# then print out all the employees and their total earnings for the day.
def close_day():
    print("close day")

    # Close day. Calculate all the tips (15% of the TOTAL),
    # update the totals (TOTAL - GRATUITY
    sql = "UPDATE SALES"
    sql += " SET"
    sql += " GRATUITY = (ROUND((TOTAL*0.15),2)),"
    sql += " UPDATED_AT = CURDATE(), "
    sql += " TOTAL = TOTAL - ROUND((TOTAL*0.15),2);"
    
    executeUpdate(sql)
    print("Sales")
    executeSelect("select * from SALES")
    
    #update quantity
    print("Item before")
    executeSelect("select * from ITEM")
        
    sql = "UPDATE ITEM,SALE_ITEMS"
    sql += " SET ITEM.QUANTITY = ITEM.QUANTITY - SALE_ITEMS.QUANTITY"
    sql += " WHERE ITEM.ID = SALE_ITEMS.ITEM_ID;"
    
    executeUpdate(sql)
    
    print("Item after")
    executeSelect("select * from ITEM")
     
     
    # show sales and counts
    sql = "SELECT CONCAT('$  ', FORMAT(SUM(TOTAL - GRATUITY), 2))  AS 'Total Sales For Today',"
    sql += "COUNT(*) AS 'NUMBER OF SALES' "
    sql += " FROM SALES "
    sql += " WHERE UPDATED_AT = CURDATE()";
    
    executeSelect(sql);
    
    # then print out all the employees and their total earnings for the day.
    print("Employee")
    executeSelect("select EMPLOYEE.NAME,SALES.TOTAL, SALES.GRATUITY from EMPLOYEE,SALES WHERE EMPLOYEE.ID = SALES.EMPLOYEE_ID")
        
    
# Update Item
# CREATE TABLE ITEM(
#    ID int NOT NULL,
#    NAME char(50) NOT NULL,
#    SUPPLIER_ID int NOT NULL,
#    QUANTITY int NOT NULL,
#    UNIT_PRICE float NOT NULL,
#    PRIMARY key (ID),
#    CHECK (QUANTITY <= 0)
#    );
 
def update_item():
    
    print("update item")

    
    # get updated value
    
    print()
    
    # get name
    name = input("Enter ITEM name: ")
    while name=="":
        name = input("Enter ITEM name: ")
        
    # show item before
    print("ITEM before update")
    executeSelect("select * from ITEM where NAME = '" + name + "'")  
        
    
    # get quantity
    quantity = int(input("Enter quantity: "))
    while quantity < 0:
        quantity = int(input("Enter quantity: "))
        
    # update data base    
    sql = "UPDATE ITEM"
    sql += " SET"
    sql += " QUANTITY  = " + str(quantity)  
    sql += " WHERE Name = '" + name + "'";
    
    executeUpdate(sql)
    
    # show item after
    print("ITEM after update")
    executeSelect("select * from ITEM where NAME = '" + name + "'")  
    
# print menu
def menu():
    
    print("\nSelection Menu:")
    print("1.  Inventory check")
    print("2.  Add a new supplier") 
    print("3.  Close day")
    print("4.  Update Item")
    print("5.  Quit")
    choice = input("Enter selection: ")
    return choice


# main function #


def main():

    # menu loop
    while True:
        
        try:
            
            # get menu selection
            choice = menu()
                
            # process menu selection
            if choice == "1":
                
                inventory_check()
                    
            elif choice == "2":
                
                add_supplier()
                
            elif choice == "3":
                
                close_day()
                
            elif choice == "4":
                
                update_item()
                
            elif choice == "5":
                
                break
        
        except Exception as e:

            print(e)
        
    close_db()  # close database

# run main
main()


