"""
client.py

Banking using an automated teller machine (ATM).
The server-side software maintains a bank account and a user accesses
the account via client software.

The user issues commands via the client to check the available balance,
withdraw money from the account, and deposit money into the account. 

The user must be able to do the following activities from the client software: 
Deposit money into the account on the server. 
Withdraw money from the account on the server. 
Check the balance of the amount in the account on the server

"""
#Zachary Holland 010579240

# progtam constants
PORT = 2000
BUFFER_SIZE = 4096

import socket

# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', PORT))

#client logins
print("Welcome to ATM machine")
account_number = input("Enter Account number(1000): ")
client.send(("Account: " + account_number).encode())
response = client.recv(BUFFER_SIZE).decode()
print(response)

if(response == "OK"):

    # cllent enters pin
    pin_number = input("Enter Pin number(1234): ")
    client.send(("PIN: " + pin_number).encode())
    response = client.recv(BUFFER_SIZE).decode()
    if(response == "OK"):

        # loop for commands
        while(True):

            # print menu
            print("1 Make Deposit")
            print("2 Withdraw Money")
            print("3 Check Balance")
            print("0 Logout")

            # get user choice
            choice = input("Enter your selection: ")

            # process selection

            # make deposit
            if choice == "1":
                amount = input("Enter amount to deposit: ")

                # send amount to server
                client.send(("Deposit: " + str(amount)).encode())

                # wait for response from server
                response = client.recv(BUFFER_SIZE).decode()
                print(response)
                
            # make withdraw
            elif choice == "2":
                amount = input("Enter amount to withdraw: ")

                # send amount to server
                client.send(("Withdraw: " + str(amount)).encode())

                # wait for response from server
                response = client.recv(BUFFER_SIZE).decode()
                print(response)
                
            # get balance
            elif choice == "3":
            
                # send request to server
                client.send(("Balance: ").encode())

                # wait for response from server
                response = client.recv(BUFFER_SIZE).decode()
                print(response)

            # get logout
            elif choice == "0":
            
                # send request to server
                client.send(("Logout: ").encode())

                # wait for response from server
                response = client.recv(BUFFER_SIZE).decode()
                print(response)
                break
                
            # bad choice
            else:
                print("Wromg choice selected")

# client closes connection
client.close()

    
