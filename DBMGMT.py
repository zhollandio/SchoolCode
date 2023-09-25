"""
database file management program

"""
import os
import os.path


class DB:
    
    def __init__(self):
        """
        input parameter(s): none
        returns: nothing
        purpose: inits instance variables, e.g., sets numSortedRecords and numOverflowRecords
        to 0, data and overflow file handles to NULL, etc.
        """
        self.numSortedRecords = 0
        self.numOverflowRecords = 0
        self.datafile = None
        self.configfile = None
        self.overflowfile = None
        self.recordLength = 128
        self.opened = False
        
    def create(self, filename):
        
        """
        input parameter(s): none
        returns: nothing
        purpose: reads csv file, creates data, overflow and config files
        
        """
        
        # open csv file
        if not os.path.isfile(filename):
            print(str(filename)+" not found")
            return False
        else:
            csvfile = open(filename, 'r')
            
            index = filename.find('.csv')
            
            # make database name and files
            if index > 0:
                databasename = filename[:index]
                # open triplet files
                datafile = open(databasename+".data","w")
                     
                # write data
                numSortedRecords = 0
                numOverflowRecords = 0
                
                # read all records
                for line in csvfile:
                    line=line.strip()
                    #print(line)
                    fmtstr = "%-"+ str(self.recordLength-2) + "s\n"
                    datafile.write(fmtstr % line)
                    numSortedRecords+=1
                datafile.close();
                                        
                # write config file: num records
                configfile = open(databasename+".config","w")
                configfile.write(str(numSortedRecords)+"\n")
                configfile.write(str(numOverflowRecords)+"\n")
                configfile.close()          
                
                # write empty overflow file
                if os.path.exists(databasename+".overflow"):
                    os.remove(databasename+".overflow")
                overflowfile = open(databasename+".overflow","w")
                overflowfile.close()
                return True
                
            else:
                print("not a csv file")
                return False
        
    def open(self,databasename):
        """
        input parameter(s): name of file to open
        returns: Boolean (true if successful, false if not)
        purpose: opens the config file to set numSortedRecords, numOverflowRecords;
        opens the data and overflow files in read/write mode,
        updates values in any other instance variables
        """
        
        # check if data base opened
        if self.opened:
            print("data base all ready opened")
            return False
        
        self.opened = False
        
        try:
        
            # set numSortedRecords, numOverflowRecords;
            # read config file: num records
            self.configfile = open(databasename+".config","r")
            self.numSortedRecords = int(self.configfile.readline())
            self.numOverflowRecords = int(self.configfile.readline())
            self.configfile.close()
            
            # open data file
            self.datafile = open(databasename+".data","r+")
            
            # oprn overflow file
            self.overflowfile = open(databasename+".overflow","r+")
            
            self.databasename=databasename
            
            self.opened = True # databasse opened
            
        # report error
        except Exception as e:
            print("Exception error: ",e)
        
        return self.opened
        
        
        
        
    def close(self):
        """
        input parameter(s): none
        returns: nothing
        purpose: resets instance variables, e.g., sets numSortedRecords,numOverflowRecords
        to 0, file handles to NULL, etc.
        """
        
        # check if data base opened
        if not self.opened:
            print("data base not opened")
            return 
        
        # close all opened files
        self.datafile.close()
        self.overflowfile.close()
        self.opened = False
        self.numSortedRecords = 0
        self.numOverflowRecords = 0
        print("data base closed")
        
                
    def isOpen(self):
        """
        input parameter(s): none
        returns: Boolean (true if database is open, false if not)
        purpose: allow main program to check the status of the DB
        """
        return self.opened
        
        
    def readRecord(self,recordNum,record):
        """
        input parameter(s): recordNum, record: id, state, city, name
        returns: Boolean (true if successful, false otherwise)
        purpose: if db open, and valid recordNum, it seeks to the beginning of recordNum
        in the indicated file and reads the record, filling the parameters from the data.
        """
        returnflag = False
    
        # check recordnum
        if recordNum >=0 and recordNum < self.numSortedRecords:
            self.datafile.seek(0,0) # seek to beginning
            index = recordNum*self.recordLength
            self.datafile.seek(index)
            line= self.datafile.readline().rstrip('\n')
            #print("line",line)
            returnflag = True
            id, state, city, name = line.split(',')
            record['id'] =id
            record['state']=state
            record['city']=city
            record['name']=name

        return returnflag
        
        
    def writeRecord(self,record):
        """
        input parameter(s): fileptr, id, state, city, name
        returns: Boolean (true if file is open, false otherwise)
        purpose: Using formatted writes, writes a fixed length record at the
        current location of the fileptr.
        By opening a file and calling writeRecord successively, 
        records are written sequentially. Used to create a db. 
        could omit fileptr parameter and just always do this on the sorted file)
        """
        
        # check if data base opened
        if self.opened:
            line = record['id'] + "," + record['city'] + "," + record['state'] + "," + record['name'] 
            fmtstr = "%-"+ str(self.recordLength-2) + "s\n"
            self.datafile.write(fmtstr % line)
            return True
        else:
            return False
        
    def overwriteRecord(self,index,file,record):
        """
        input parameter(s): fileptr, recordNum, id, state, city, name
        returns: Boolean (true if file is open and recordNum is valid for that file, false otherwise)
        purpose: if valid recordNum, using formatted writes, writes a fixed length record.
        It seeks to the beginning of recordNum in the indicated file and overwrites the record. The indicated file may be the sorted file or the overflow file. Used to update a record in either the sorted or overflow file.
        """
        line = record['id'] + "," + record['city'] + "," + record['state'] + "," + record['name'] 
        fmtstr = "%-"+ str(self.recordLength-2) + "s\n"
        
        # data file
        if file=='datafile':
            self.datafile.seek(0,0) # seek to beginning
            self.datafile.seek(int(index))
            self.datafile.write(fmtstr % line)
            self.datafile.seek(int(index))
            #x = self.datafile.readline()
            #print(x)
            return True
        
        # overflow file
        if file=='overflowfile':
            self.datafile.seek(0,0) # seek to beginning
            self.overflowfile.seek(int(index))
            self.overflow.write(fmtstr % line)
            return True
           
        
    def appendRecord(self,record):
        """
        input parameter(s): id, state, city, name
        returns: Boolean (true if db is open, false otherwise)
        purpose: Using formatted writes, writes a fixed length record at the end of the file.
        Used to add a record to the overflow file.
        """
        
        # check if data base opened
        if self.opened:
            line = record['id'] + "," + record['city'] + "," + record['state'] + "," + record['name'] 
            fmtstr = "%-"+ str(self.recordLength-2) + "s\n"
            self.overflowfile.seek(0, 2) # seek to end
            self.overflowfile.write(fmtstr % line)
            self.numOverflowRecords+=1
            # update config file
            self.configfile = open(self.databasename+".config","w")
            self.configfile.write(str(self.numSortedRecords)+"\n")
            self.configfile.write(str(self.numOverflowRecords)+"\n")
            self.configfile.close()    
            
            return True
        else:
            return False
        
    def binarySearch(self,id,record={'id':None,'state':None,'city':None,'name':None}):
        """
        input parameter(s): id, state, city, name
        returns: the recordNum of the record for the id (if found), -1 if not found
        purpose: if db open, it uses seeks to perform binary search on the sorted file
        to locate the id. It fills in the parameters with the data (if found),
        otherwise it sets them to default values.
        """

        low = 0
        high = self.numSortedRecords - 1
        found = -1
        cur_record = {'id':None,'state':None,'city':None,'name':None}

        while high >= low:

            middle = (low+high)//2
            self.readRecord(middle,cur_record)
            #print(cur_record)
            mid_id = cur_record["id"]
            
            # id found
            if int(mid_id) == int(id):
                found = middle*self.recordLength
                record['id'] = cur_record['id']
                record['state'] = cur_record['state']
                record['city'] = cur_record['city']
                record['name'] = cur_record['name']
                return found
            elif int(mid_id) > int(id):
                high = middle - 1
            elif int(mid_id) < int(id):
                low = middle + 1
        return found
    
    def findRecord(self,record_number,record={'id':None,'state':None,'city':None,'name':None}):
        """
        input parameter(s): recordNum, fileId, id, state, city, name
        returns: Boolean (true if db is open, false otherwise)
        purpose: if db open, it calls binary search to search the sorted file by id.
        If the record is not found in that file, it searches the overflow file sequentially.
        It fills the parameters from the data (if found), otherwise it sets them to default values.
        It also fills in the recordNum and an id that indicates in which file the record was found.
        """
        
        # check data file
        index = self.binarySearch(record_number, record)
        
        if index != -1:
            return (index,'datafile')
        
        # check over flow file
        self.overflowfile.seek(0,0)
        
        for index in range(self.numOverflowRecords):
            self.overflowfile.seek(index*self.recordLength)
            line= self.overflowfile.readline().rstrip('\n')
            id, state, city, name = line.split(',')
            if int(id) == int(record_number):
                record['id'] = id
                record['state'] = state
                record['city'] = city
                record['name'] = name
                return (index*self.recordLength,'overflow')
            
        # no record found
        return (-1,'')
            
    
        
    def addRecord(self,id,state,city,name):
        """
        input parameter(s): id, state, city, name
        returns: Boolean, true if db open, false otherwise
        purpose: if db is open, it appending a new fixed length record to the
        end of the overflowfile.
        """
        
        # check if data base opened
        if self.opened:
            record = {'id':id,'state':state,'city':city,'name':name}
            self.appendRecord(record)
            return True
        else:
            
            return False
            
        
    def updateRecord(self,index,file,record):
        """
        input parameter(s): id, state, city, name
        returns: Boolean, true if record is updated, false otherwise
        purpose: if db is open, it uses findRecord to locate the record.
        It then uses overwriteRecord to update it.
        """
        
        # check if data base opened
        if self.opened:
            self.overwriteRecord(index,file,record)
            return True
        else:
            return False
            
        
    def deleteRecord(self,id):
        """
        input parameter(s): id
        returns: Boolean, true if record is deleted, false otherwise
        purpose: if db is open, it uses findRecord to locate the record.
        It then uses overwriteRecord to update it to default (empty) values.
        Keep the id the same though, otherwise binarySearch will break
        """
      
        record = {'id':id,'state':'','city':'','name':''}
        
        # check if data base opened and is digit
        if id.isdigit() and self.opened:
            index, file = self.findRecord(id,record)
            print("index",index,"file found in ",file)
            
            # delete data
            record = {'id':id,'state':'','city':'','name':''}
            line = record['id'] + "," + record['city'] + "," + record['state'] + "," + record['name'] 
            fmtstr = "%-"+ str(self.recordLength-2) + "s\n"
            
            # delete from data file
            if file=='datafile':
                self.overflowfile.seek(0,0)
                self.datafile.seek(index)
                self.datafile.write(fmtstr % line)
                return True
            
            # delete from overflow
            if file=='overflow':
                self.overflowfile.seek(0,0)
                self.overflowfile.seek(index)
                self.overflowfile.write(fmtstr % line)
                return True
           
            return False
                
        else:
            return False
        


"""
main
"""

def menu():
    
    """
    input parameter(s): none
    returns: menu selection
    purpose: returns user menu selection
    """
    
    # print menu
    print("1) Create new database")
    print("2) Open database")
    print("3) Close database")
    print("4) Display record")
    print("5) Update record")
    print("6) Create report")
    print("7) Add record")
    print("8) Delete record")
    print("9) Quit")
    
    # get menu selection
    choice = input("Enter menu selection: ")
    return choice


def main():
    
    # db
    db = DB()
    
    # read menu choice
    choice = menu()
    
    # loop till exit
    while(choice!="9"):
        
        # process selection
                    
        # Create new database
        if choice == "1":
                    
            # ask for data base file name
            filename = "collages-lf.csv"
            filename = input("Enter data base CSV file name: ")
           
            if not db.create(filename):
                print("cannot create data base files")
            else:
                print("data base created")
            
        # Open database
        elif choice == "2":
            
            # chebk if a data base is opened
            if db.isOpen():
                print("a data base is allready opened, close current data base")
                
            else:
                # ask for data base name
                dbname = "collages-lf"
                dbname=input("Enter data base name: ")
                if not db.open(dbname):
                    print("cannot open data base")
                else:
                    print("data base opened")
        
        # Close database
        elif choice == "3":
            db.close()
        # Display record
        elif choice == "4":
            
            if not db.isOpen():
                print("data base not opened")
                
            # data base opened
            else:
                
                record = {}
                record_number = input("enter record number: ")
                if record_number.isdigit():
                    index, file = db.findRecord(record_number,record)
                    if index == -1:
                        print("record not found")
                    else:
                        print("index",index,"file found in ",file)
                        print("id:",record['id'])
                        print("city:",record['city'])
                        print("state:",record['state'])
                        print("name:",record['name'])
                else:
                    print("bad record number entered")
                    
        # Update record
        elif choice == "5":
            
            # check if data base opened
            if not db.isOpen():
                print("data base not opened")
            else:
                record = {}
                record_number = input("enter record number: ")
                
                # find record
                if record_number.isdigit():
                    index, file = db.findRecord(record_number,record)
                    print("index",index,"file found in ",file)
                    print("id:",record['id'])
                    print("city:",record['city'])
                    if(input("change city (y/n)? ").lower() == 'y'):
                        record['city'] = input("Enter new city: ")
                    if(input("change state (y/n)? ").lower() == 'y'):
                        record['state'] = input("Enter new state: ")
                    if(input("change name (y/n)? ").lower() == 'y'):
                        record['name'] = input("Enter new name: ")
                    db.updateRecord(index,file,record)
                else:
                    print("bad record number entered")
        # Create report
        elif choice == "6":
            
            # check if data base opened
            if not db.isOpen():
                print("data base not opened")
                
            else:
                print("report")
                
                record = {}
                
                # read first 10 records
                for i in range(10):
                    
                    db.readRecord(i,record)
                    print("id:",record['id'])
                    print("city:",record['city'])
                    print("state:",record['state'])
                    print("name:",record['name'])
                    print()
            
        # Add record
        elif choice == "7":
            
            # check if data base opened
            if not db.isOpen():
                print("data base not opened")
            else:
                # get data
                id = input("Enter id: ")
                city = input("Enter city: ")
                state = input("Enter state: ")
                name = input("Enter name: ")
                
                # add record
                if(db.addRecord(id,city,state,name)):
                    print("record added")
                else:
                    print("record not added")
        
        # Delete record
        elif choice == "8":
            
            # check if data base opened
            if not db.isOpen():
                print("data base not opened")
                
            else:
                id = input("Enter record id:")
                
                if id.isdigit():
                    if db.deleteRecord(id):
                        print("record deleted")
                    else:
                        print("record not deleted")
                else:
                    print("bad record number entered")
                
     
        # read next menu choice
        choice = menu()
        
    # Quit
    if db.isOpen():
        db.close()
    print("goodbye")
        
main() # run main

   
    
    
    
    

        
        
