"""
server.py
automated teller machine (ATM).
The server-side software maintains a bank account and a user accesses the account via client software.
For this program, you can assume that a single account will be accessed by a single user.
There are two sides to this program: a server and a client.
The server maintains the balance and does all updates (withdrawals and deposits)
and also responds to queries on the amount of money in the account.
The user issues commands via the client to check the available balance,
withdraw money from the account, and deposit money into the account.
The server should initialize the balance in the bank account to $100. 
Optional overdraft is provided
"""

# program constants
PORT = 2000
BUFFER_SIZE = 4096
ACCOUNT = "1000"
PIN = "1234"
OVERDRAFT = 0


import socket


# starting balance
balance = 100


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', PORT))
serv.listen(5)

# connection loop
while True:
    
    # initialize
    login = False
    PIN = False
    
    # wait for clients
    print("server waiting for clients")
    conn, addr = serv.accept()

    # process client
    while True:
        
        # get request from client
        request= conn.recv(BUFFER_SIZE).decode()
        if not request: break
        print ("received from_client: ", request)
        
        # process command
        cmd = request.split()
        
        # log in to account
        if(cmd[0] == "Account:"):
            if cmd[1] != "1000":
                conn.send("Wrong Account Number".encode())
            else:
                login = True
                conn.send("OK".encode())
                
        # validate pin
        elif(cmd[0] == "PIN:"):
            if cmd[1] != "1234":
                conn.send("Wrong PIN Number".encode())
            else:
                PIN = True
                conn.send("OK".encode())
                
        # deposit amount
        elif(cmd[0] == "Deposit:"):
            
            try:
                amount = float(cmd[1])
                
                # validate amount
                if(amount <= 0):
                    conn.send("No negative numbers please".encode())
                    
                # deposit amount
                else:
                    balance += amount
                    conn.send("OK".encode())
            except:
                conn.send("Amount entered is not a number".encode())
                
        # with draw funds
        elif(cmd[0] == "Withdraw:"):
            try:
                amount = float(cmd[1])
                
                 # validate amount
                if(amount <= 0):
                    conn.send("No negative numbers please".encode())
                else:
                
                    # withdawl amount
                    if(amount > balance+OVERDRAFT):
                        conn.send("Insufficient funds".encode())
                    else:
                        balance -= amount
                        conn.send("OK".encode())
            except:
                conn.send("Amount entered is not a number".encode())
            
        # check balance
        elif(cmd[0] == "Balance:"):
            conn.send(("Your Balance is: " + "$%.2f" % (balance)).encode())
            
        # logout
        elif(cmd[0] == "Logout:"):
            conn.send(("Thankyou for banking with us").encode()) 
            break;
        
        # unknown command
        else:
            conn.send(("Unknown Command Received").encode()) 
        
    # close client connection
    conn.close()
    print ('client disconnected')
    
