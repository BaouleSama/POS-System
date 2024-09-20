#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print("Welecome to POS System")
class Security:
    
    def __init__(self):
        
        self.is_logged = True
        self.dataUser = {}
        self.count =0
        
    def login(self):
        while(self.is_logged):
            
            self.userid = input("Please enter userid ")
            self.password = input("Please enter password ")
            
            file_object = open("signup.txt","r")
            for file in file_object:
                    line = file.strip().split(",")
                    self.dataUser[line[0]]=line[1]

            if(self.count==2):
                        print("Your account has been locke out. Please contact your system admin")
                        
            elif( (self.userid in self.dataUser) and (self.password == self.dataUser[self.userid]) ):
                        print("Welcome back " + self.userid)
                        break
            else:
                print("wrong user or password")
                self.count +=1

class Item:
    def __init__(self, UPC, 
                 Description,
                 Item_Max_Qty,
                 Order_Threshold,
                 replenishment_order_qty,
                 Item_on_hand,
                 Unit_price,
                 Order_placed):
        
        self.upc = UPC
        self.description = Description
        self.iItem_max_qty = Item_Max_Qty
        self.order_threshold = Order_Threshold
        self.replenishment_order_qty = replenishment_order_qty
        self.item_on_hand = Item_on_hand
        self.unit_price = Unit_price
        self.order_placed = Order_placed
    
       
class Inventory:
    
    def __init__(self):
        self.database={}
        
        
    def readData(self):
        file = open("RetailStoreItemData.txt","r")
        for files in file:
            line = files.strip().split(",")
            self.item = Item(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
    
            self.database[line[0]] = self.item
        file.close()
        
        
    def updateUnitOnHand(self,upc,numberOfItems):
        self.update=float(self.database[upc].item_on_hand) + float(numberOfItems)
        if(self.update<0):
            self.update=0
        self.database[upc].item_on_hand = self.update
        
    def writeDataToFile(self):
        with open("RetailStoreItemData-1.txt.txt", "w") as file:
            for upc, item in self.database.items():
                line = f"{upc},{item.description},{item.iItem_max_qty},{item.order_threshold},{item.replenishment_order_qty},{item.item_on_hand},{item.unit_price},{item.order_placed}\n"
                file.write(line)
        
    def inventory(self):
        for i in self.database:
            print(i,self.database[i].description, 
                  self.database[i].iItem_max_qty,
                  self.database[i].order_threshold,
                  self.database[i].replenishment_order_qty,
                  self.database[i].item_on_hand,self.database[i].unit_price,
                  self.database[i].order_placed)

class Start():
    
    def __init__(self):
        self.is_running = True
        self.myInventory = Inventory()
        self.myInventory.readData()
        self.sale = NewSale()
        self.security = Security()
        self.login()
        
    def login(self):
        self.security.login()
        if self.security.is_logged:
            self.menu()
            
    def menu(self):
        while(self.is_running== True):
            
            option = int(input('''Please select an option)
                    1: "New Sale",
                    2: "Return Item/s",
                    3: "Backroom Operations",
                    4: "Report",
                    9: "Exit Application"\n'''))
            
            
            if (option == 1):
                print("New Sale")
                self.sale.make_sale()
                
            elif (option == 2):
                print("Return Item/s")
                self.sale.returnItem()
                
            elif (option == 3):
                print("Backroom Operations")
                self.myInventory.inventory()
                
            elif (option == 4):
                print("Report")
                self.sale.report()
                
            elif (option == 9):
                print("Bye ")
                break
                
class NewSale():
    
    def __init__(self):
       
        self.receipt =[]
        self.receipt_number = 1509474
        self.order = set()
        
    def make_sale(self):
        
        self.sale = True
        self.myInventory = Inventory()
        self.myInventory.readData()
        
        self.store_inventory = self.myInventory.database
        
        while(self.sale == True):
#           ask customer for UPC
            self.upc = input("Please enter a UPC ")
            
#           look for upc is in the inventory
            if(self.upc in self.store_inventory):
#                   Show the item ask for
                    print("You enter " + self.store_inventory[self.upc].description )
                 
#                   Ask for Item Quantity
                    self.quantity = int(input("Please enter Quantity "))
                    result = self.quantity * float(self.myInventory.database[self.upc].unit_price)
                    
#                   Update the quantity on hand
                    self.myInventory.updateUnitOnHand(self.upc, -self.quantity)
                    print("Item on hand : " + str(self.myInventory.database[self.upc].item_on_hand))
                    self.myInventory.writeDataToFile()
#                     self.myInventory.findItem(self.upc)

                    self.order.add(self.upc)
                    print("The price is " + str(result))

                    option = int(input('''Please select an option)
                        1: "Sell another Item",
                        2: "Return Item/s",
                        9: "Complete Sale "\n'''))
                    

                    if(option ==2):
                        self.returnItem()
                    elif(option == 9):
                
                        # check if there is no duplicate receipt number                         
                        if(self.receipt_number in self.receipt):
                            self.receipt_number *= 2
                            self.receipt.append(str(self.receipt_number))
                        else:
#                           if no recipt number duplicate, add the receipt to the collection 
                            self.receipt.append({str(self.receipt_number) : self.order})
                      
#                       Give the receipt number 
                        print("Your receipt number is " + str(self.receipt_number))
                        self.receipt_number +=1
                        self.sale = False
                                         
            else:
                    print("NO UPC FOUND")
                    
    
    def report(self):
        print("Today sales include :")
        
        for receipts in self.receipt:
            for r_number in receipts:
                convert_order_in_list = list(receipts[r_number])
                total_sale = 0
                for list_order in convert_order_in_list:
                    print(self.myInventory.database[list_order].description)
                    total_sale += round(float(self.myInventory.database[list_order].unit_price),2)
                
            print("return amount: " +"$" +str(total_sale))
        
    def returnItem(self):
        
#       Ask for the receipt number
        self.myReceipt = input("Enter Receipt Number")
        
#       look for the receipt provided by customer 
        for receipts in self.receipt:
        
#           When receipt found, ask for all item to be return or just one
            if(self.myReceipt in  receipts):
                r_option = int(input("1 = Return Single item, 2 = Return All Item"))

                if(r_option == 1):
#                   ask for item upc and quanity of item to be return and give the refund 
                    self.myUPC = input("Enter the UPC to be Returned ")
                    self.quantity_wanted = input("Please enter quantity ")
                    self.quantity_refunded = round(float(self.quantity_wanted) * float(self.myInventory.database[self.myUPC].item_on_hand),2)
                    print("Return amount " +  str(self.quantity_refunded))
                
                    # Update the database after the return
                    self.myInventory.updateUnitOnHand(self.myUPC, round(float(self.quantity_wanted),2))
                    self.myInventory.writeDataToFile()
                
                elif(r_option ==2):
                    make_sure = input("Are you sure you want to return all items? Y=yes, N=No")
                    if(make_sure == "Y"):
                        quantity_to_return =0
                        
#                       convert the set of upc in list to be itrable 
                        convert_order_in_list = list(receipts[self.myReceipt])
                        total_refunded = 0
        
#                       loop through every upc and and print the the item, then calculate total refund 
                        for list_order in convert_order_in_list:
                                quantity_to_return = self.myInventory.database[list_order].item_on_hand
                                total_refunded += round(float(self.myInventory.database[list_order].unit_price),2)
                                print("You entered " + self.myInventory.database[list_order].description)        
                        print("return amount: " +"$" +str(total_refunded))
                        
                        # Update the database after the return
                        self.myInventory.updateUnitOnHand(list_order, round(float(quantity_to_return),2))
                        self.myInventory.writeDataToFile()
                    
                        receipts[self.myReceipt].clear()
                        

            else:
                print("No receeipt found")

s = Start()


# In[ ]:




