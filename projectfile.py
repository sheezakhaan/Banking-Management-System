import mysql.connector

db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="")

class Bank:
        cursor = db.cursor()
        cursor.execute("CREATE database IF NOT EXISTS bank_db")
        cursor.execute("USE bank_db")

        cursor.execute('''CREATE TABLE IF NOT EXISTS branch(
                   branch_id INT NOT NULL AUTO_INCREMENT,
                   branch_name TEXT NOT NULL,
                   phone_no VARCHAR(50) NOT NULL,
                   address VARCHAR(50), 
                   PRIMARY KEY(branch_id)
                   )''')
      
        cursor.execute('''INSERT IGNORE INTO branch (branch_id,branch_name,phone_no,address) 
                   VALUES
                   (1, 'ABC', '12345', 'ABC Road'),
                   (2, 'XYZ', '54321', 'XYZ Road'),
                   (3, 'PQR', '13579', 'PQR Road'),
                   (4, 'ASD', '02468', 'ASD Road') 
                 ''')
            
        db.commit()

       

        cursor.execute('''CREATE TABLE IF NOT EXISTS customer(
                   customer_id INT NOT NULL AUTO_INCREMENT,
                   name TEXT NOT NULL,
                   phone_no VARCHAR(50) NOT NULL,
                   nic VARCHAR(15) NOT NULL,
                   address VARCHAR(60),
                   branch_id INT NOT NULL,
                   c_password VARCHAR(50) NOT NULL,
                   PRIMARY KEY(customer_id),
                   FOREIGN KEY(branch_id) REFERENCES branch(branch_id)
                   ON DELETE CASCADE
                   )''')
        


        cursor.execute('''CREATE TABLE IF NOT EXISTS employee(
                   employee_id INT NOT NULL AUTO_INCREMENT,
                   name TEXT NOT NULL,
                   phone_no VARCHAR(50) NOT NULL,
                   nic VARCHAR(15) NOT NULL,
                   address VARCHAR(100),
                   branch_id INT NOT NULL,
                   PRIMARY KEY(employee_id),
                   FOREIGN KEY(branch_id) REFERENCES branch(branch_id)
                   ON DELETE CASCADE 
                   )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(
               account_id INT NOT NULL AUTO_INCREMENT,
               password VARCHAR(50) NOT NULL,
               account_balance FLOAT,
               account_type TEXT,
               customer_id INT NOT NULL,    
               PRIMARY KEY(account_id),
               FOREIGN KEY(customer_id) REFERENCES customer(customer_id)   
               ON DELETE CASCADE        
               )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS transaction(
               transaction_id INT NOT NULL AUTO_INCREMENT,
               transaction_type VARCHAR(50),         
               transaction_amount FLOAT(12),
               account_id INT NOT NULL,
               transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (transaction_id),
               FOREIGN KEY (account_id) REFERENCES accounts(account_id)
               )''')


        
        


        
        def create_account(self,name,phone_no,nic,address,c_password,branch_id):

        
                
                query = f"INSERT INTO customer (name, phone_no, nic, address, c_password, branch_id) VALUES ('{name}', '{phone_no}', '{nic}', '{address}', '{c_password}','{branch_id}')"
                self.cursor.execute(query)     
                db.commit()
                print("Customer Account created successfully")
                query = f"SELECT customer_id FROM customer WHERE nic = '{nic}'"
                self.cursor.execute(query)     
                result = self.cursor.fetchone()[0]     
                
                print(f"Your customer ID is: {result} ")

           
                account_details = str(input("Do you want to Open Bank Account Now or Later?\n Yes/No: "))
                
                if account_details == "YES" or account_details == "yes" or account_details == "Yes":
                        
                        password = input("Create Password: ")
                        account_balance = float(input("Deposit the First Account Balance: "))                                
                        account_type = str(input("Enter Account Type (Saving/Current): "))
                        customer_id = int(input("Enter your customer ID: "))     
                        
                        query = f"INSERT INTO accounts (password, account_balance, account_type, customer_id) VALUES ('{password}', '{account_balance}', '{account_type}', '{customer_id}')"
                        self.cursor.execute(query)     
                        db.commit()
                        print("Customer Bank Account created Successfully")  
                        query = f"SELECT * FROM accounts a INNER JOIN customer c ON a.customer_id = c.customer_id WHERE c.customer_id = '{customer_id}'"
                        self.cursor.execute(query)     
                        account = self.cursor.fetchone()
                        query = f"INSERT INTO transaction (transaction_type,transaction_amount,account_id) VALUES ('Deposit','{account_balance}','{account[0]}')"
                        self.cursor.execute(query)
                        db.commit()  
                        query = f"SELECT account_id FROM accounts WHERE customer_id = '{result}'"
                        self.cursor.execute(query)     
                        result1 = self.cursor.fetchone()[0]   
                        print(f"Your account ID is: {result1} ")  
                                       
                        
                              
                else:
                        print("Thanks For Visit!")

        
        def create_bank_account(self,password,account_balance,account_type,customer_id):
              
                                query = f"INSERT INTO accounts (password, account_balance, account_type,customer_id) VALUES ('{password}', '{account_balance}', '{account_type}', '{customer_id}')"
                                self.cursor.execute(query)     
                                db.commit()
                                print("Customer Bank Account created successfully")

        def deposit_amount(self,account,amount):

                result = account[2] + amount
                query = f"UPDATE accounts SET account_balance = '{result}' WHERE account_id = '{account[0]}'"
                self.cursor.execute(query)
                db.commit()
                query = f'''SELECT name FROM customer 
                            INNER JOIN accounts 
                            ON customer.customer_id = accounts.customer_id 
                            WHERE account_id = '{account[0]}';'''
                self.cursor.execute(query)
                name_welcome = self.cursor.fetchone()[0] 
                
                print(f'Hello {name_welcome}, Hope you doing well!')
                print()
                print(f"{amount} is Deposited in your Account")
                query = f"SELECT account_balance FROM accounts WHERE account_id = '{account[0]}'"
                self.cursor.execute(query)
                account_balance  = self.cursor.fetchone()[0] 
                print(f"your current balance is {account_balance}")
                query = f"INSERT INTO transaction (transaction_type,transaction_amount,account_id) VALUES ('Deposit','{amount}','{account[0]}')"
                self.cursor.execute(query)
                db.commit()

        def withdraw_amount(self,account,amount):
               
                if amount <= account[2]:
                        result = account[2] - amount
                        query = f"UPDATE accounts SET account_balance = '{result}' WHERE account_id = '{account[0]}'"
                        self.cursor.execute(query)
                        db.commit()
                        query = f'''SELECT name FROM customer 
                            INNER JOIN accounts 
                            ON customer.customer_id = accounts.customer_id 
                            WHERE account_id = '{account[0]}';'''
                        self.cursor.execute(query)
                        name_welcome = self.cursor.fetchone()[0] 
                        
                
                        print(f'Hello {name_welcome}, Hope you doing well!')
                        print()
                        print(f"{amount} is Deducted from your Account")
                        print(f"your current balance is {result}")     
                        query = f"INSERT INTO transaction (transaction_type,transaction_amount,account_id) VALUES ('Withdraw','{amount}','{account[0]}')"
                        self.cursor.execute(query)
                        db.commit()


                else:
                        print("Insufficient balance")
       
            
               
        def check_balance(self,account_no):   
                print(f"Your Balance is: Rs.{account_no[2]}")
                
        def update_account(self, db_table_index,customer_id):
                if db_table_index == 1:
                        info = input("Enter a new name to update: ")
                        query = f"UPDATE customer SET name = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit()
                elif db_table_index == 2:
                        info = input("Enter a new Phone no to update: ")
                        query = f"UPDATE customer SET phone_no = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit() 
                elif db_table_index == 4:
                        info = input("Enter a address to update: ")
                        query = f"UPDATE customer SET address = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit() 
                elif db_table_index == 6:
                        info = input("Enter a new customer password to update: ")
                        query = f"UPDATE customer SET c_password = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit() 
                elif db_table_index == 7:
                        info = input("Enter a account password to update: ")
                        query = f"UPDATE accounts SET password = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit()  
                elif db_table_index == 3:
                        info = input("Enter a account type to update: ")
                        query = f"UPDATE accounts SET account_type = '{info}' WHERE customer_id = '{customer_id}'"
                        self.cursor.execute(query)
                        db.commit()  
                elif db_table_index == 0:
                        info = input("Enter a branch id to update: ")
                        query = f'''UPDATE customer 
                                    INNER JOIN branch 
                                    ON branch.branch_id = customer.branch_id 
                                    SET customer.branch_id = '{info}'
                                    WHERE customer.customer_id = '{customer_id}' '''
                        self.cursor.execute(query)
                        db.commit()  
                
                
                print("Your Account is Updated Succefully")

        def display_acc_details(self,customer_account):
                query = f'''SELECT account_id, name, phone_no, account_balance, address, account_type
                            FROM customer
                            INNER JOIN accounts
                            ON customer.customer_id = accounts.customer_id
                            WHERE customer.customer_id = '{customer_account[0]}' '''
                self.cursor.execute(query)
                details = self.cursor.fetchone()
                 
                        
                
                print(f"""
                                ____________________________________________________________________________________________________________________
                                
                                                        
                                        Account No: {details[0]} | Name: {details[1]} | Phone No: {details[2]} | Account Balance: {details[3]}  
                                                                Address: {details[4]} | Account Type: {details[5]}
                                
                                ____________________________________________________________________________________________________________________
                      """)
       
        def create_employee_account(self,name,phone_no,nic,address,branch_id):
                query = f"INSERT INTO employee (name, phone_no, nic, address, branch_id) VALUES ('{name}', '{phone_no}', '{nic}', '{address}', '{branch_id}')"
                self.cursor.execute(query)     
                db.commit()
                print("Employee Account created successfully")
        
        def display_employees(self):
                query = f'''SELECT count(employee_id) as no_emps FROM employee'''
                self.cursor.execute(query)
                a = self.cursor.fetchone()[0]
                query1 = f'''SELECT * FROM employee e INNER JOIN branch b ON e.branch_id = b.branch_id'''
                self.cursor.execute(query1)
                b = self.cursor.fetchall()
                for i in range(a):
                        print(f'''Employee: {i+1}
                                Employee ID: {b[i][0]}
                                Employee Name: {b[i][1]}
                                Phone no: {b[i][2]}
                                NIC: {b[i][3]}
                                address: {b[i][4]}
                                branch name: {b[i][7]}''')
                        
        def update_employee_account(self, db_table_index, employee_id):
                if db_table_index == 1:
                        info = input("Enter a new name to update: ")
                        query = f"UPDATE employee SET name = '{info}' WHERE employee_id = '{employee_id}'"
                        self.cursor.execute(query)
                        db.commit()
                elif db_table_index == 2:
                        info = input("Enter a new Phone no to update: ")
                        query = f"UPDATE employee SET phone_no = '{info}' WHERE employee_id = '{employee_id}'"
                        self.cursor.execute(query)
                        db.commit() 
                elif db_table_index == 4:
                        info = input("Enter a address to update: ")
                        query = f"UPDATE employee SET address = '{info}' WHERE employee_id = '{employee_id}'"
                        self.cursor.execute(query)
                        db.commit() 
                elif db_table_index == 5:
                        info = input("Enter a branch id to update: ")
                        query = f"UPDATE employee SET branch_id = '{info}' WHERE employee_id = '{employee_id}'"
                        self.cursor.execute(query)
                        db.commit() 
       
        def checking_for_id(self, id, table):
                if table == "employee":
                        query = f"SELECT * FROM employee WHERE employee_id = '{id}'"
                        self.cursor.execute(query)
                        result = self.cursor.fetchone()
                        if result is not None: 
                                return "valid"
                        else:
                                return "not valid"
                elif table == "customer":
                        query = f"SELECT * FROM customer WHERE customer_id = '{id}'"
                        self.cursor.execute(query)
                        result = self.cursor.fetchone()
                        if result is not None: 
                                return "valid"
                        else:
                                return "not valid"
                elif table == "accounts":
                        query = f"SELECT * FROM accounts WHERE account_id = '{id}'"
                        self.cursor.execute(query)
                        result = self.cursor.fetchone()
                        if result is not None: 
                                return "valid"
                        else:
                                return "not valid"
                elif table == "transaction":
                        query = f"SELECT * FROM transaction WHERE account_id = '{id}'"
                        self.cursor.execute(query)
                        result = self.cursor.fetchall()
                        if result is not None: 
                                return "valid"
                        else:
                                return "not valid"
                        
        def transactions(self,account_no):
                query = f"select count(transaction_id) FROM transaction WHERE transaction.account_id = '{account_no[0][3]}' "
                self.cursor.execute(query)
               
                a = self.cursor.fetchone()[0]
                
                query1 = f'''SELECT *
                        FROM transaction
                        INNER JOIN accounts
                        ON transaction.account_id = accounts.account_id
                        WHERE transaction.account_id = '{account_no[0][3]}' '''
               
                self.cursor.execute(query1)
                details = self.cursor.fetchall()
               
                for i in range(a):
                        print(f'''Transaction id = {details[i][0]}
                                Transaction_type = {details[i][1]}
                                Transaction_amount = {details[i][2]}
                                Account ID = {details[i][3]} 
                                Transaction Time = {details[i][4]} ''')

        
        def display_transactions(self):
                query = f'''SELECT count(transaction_id) as no_trans FROM transaction'''
                self.cursor.execute(query)
                a = self.cursor.fetchone()[0]
                
                query1 = f'''SELECT * FROM transaction t INNER JOIN accounts a ON t.account_id = a.account_id'''
                self.cursor.execute(query1)
                b = self.cursor.fetchall()
                for i in range(a):
                        print(f'''Transaction no: {i+1}
                                Transaction ID: {b[i][0]}
                                transaction Type: {b[i][1]}
                                Transaction Amount: {b[i][2]}
                                Account ID: {b[i][3]}
                                Transaction Time: {b[i][4]} ''')


        def delete_customer_account(self,customer_account):         
                
                queryAcc = f"DELETE FROM accounts WHERE customer_id = '{customer_account[0]}' "
                self.cursor.execute(queryAcc)
                queryCus = f"DELETE FROM customer WHERE customer_id = '{customer_account[0]}' "
                self.cursor.execute(queryCus)
                db.commit()
                print("Account Deleted successfully")            


        def delete_bank_account(self,account_no):         
                query = f"DELETE FROM accounts WHERE account_id = '{account_no[0]}'"
                self.cursor.execute(query)
                db.commit()
                print("Account Deleted successfully")

        def delete_employee(self,account_no):         
                query = f"DELETE FROM employee WHERE account_id = '{account_no[0]}'"
                self.cursor.execute(query)
                db.commit()
                print("Employee Account Deleted successfully")

        #----------------------------------------------
       
        def get_cust_account(self, customer_id):
                query = f"SELECT * FROM customer WHERE customer_id = '{customer_id}' "
                self.cursor.execute(query)
                result = self.cursor.fetchone() 
                return result  
        
        def get_account(self, account_no):
                query = f"SELECT * FROM accounts WHERE account_id = '{account_no}'"
                self.cursor.execute(query)
                result = self.cursor.fetchone() 
                return result
        
        def get_emp_account(self,account_no):
                query = f"SELECT * FROM employee WHERE employee_id = '{account_no}'"
                self.cursor.execute(query)
                result = self.cursor.fetchone() 
                return result
        
        def get_transaction_id(self, account_no):
                query = f"SELECT * FROM transaction WHERE account_id = '{account_no}'"
                self.cursor.execute(query)
                result = self.cursor.fetchall() 
                return result
        

        


def Menu():
        print( 
               """
                
                
                                                        *******************************************************
                                                        Menu: 
                                                                => Press '1' to Create Customer Account
                                                                => Press '2' to Create Bank Account
                                                                => Press '3' to Deposit 
                                                                => Press '4' to Withdraw
                                                                => Press '5' to Update account 
                                                                => Press '6' to Display Account Details
                                                                => Press '7' to Check Balance
                                                                => Press '8' to Delete Customer Account
                                                                => Press '9' to Delete Bank Account
                                                                => Press '10' to Create Employee Account
                                                                => Press '11' to Display Employees
                                                                => Press '12' to Update Employee Account
                                                                => Press '13' to Display Transactions
                                                                => Press '14' to Display Transaction of a customer
                                                                => Press '15' to Exit Account
                                                
                                                        ********************************************************
        
        """)

cus = Bank()

while True:
        
        Menu()
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
                name = input("Enter your Full name: ") 
                phone_no = int(input("Enter your Phone no: e.g:(03123456779): "))
                nic = int(input("Enter your NIC: e.g:(42111058551): "))
                address = input("Enter your current home adress: ")
                c_password = input("Create customer account password: ")
                branch_id = int(input("Enter Branch_id: "))
                cus.create_account(name,phone_no,nic,address,c_password,branch_id)


        elif choice == 2:            
                customer_id = int(input("Enter your customer ID: "))                                
                account_checking = cus.checking_for_id(customer_id,"customer")
                if account_checking == "valid":
                
                        cust_password = input("Enter your customer Account Password: ")
                        c_account = cus.get_cust_account(customer_id)
                        if cust_password == c_account[6]:
                                password = input("Create Bank Account Password: ")
                                account_balance = float(input("Deposit the First Account Balance: "))                                
                                account_type = str(input("Enter Account Type (Saving/Current): "))                                
                                cus.create_bank_account(password,account_balance,account_type,customer_id)
                        else:
                                print(f"Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
                
                
                
        elif choice == 3:
                account_no = int(input("Enter account number: "))
                account_checking = cus.checking_for_id(account_no,"accounts")
                if account_checking == "valid":
                
                        account = cus.get_account(account_no)
                        password = input("Enter Password to Deposit: ")
                        if password == account[1]:
                                amount = float(input("Enter amount to deposit: "))
                                cus.deposit_amount(account,amount)
                        else:
                                print(f"Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
                        
        
        
        elif choice == 4:
                
                account_no = int(input("Enter account number: "))
                account_checking = cus.checking_for_id(account_no,"accounts")
                if account_checking == "valid":
                
                        account = cus.get_account(account_no)
                        password = input("Enter Password: ")
                        if password == account[1]:
                                amount = float(input("Enter amount to withdraw: "))
                                cus.withdraw_amount(account,amount)
                        else:
                                print("Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
             
                
        elif choice == 5:
                account_no = int(input("Enter Your Account Number: "))
                account_checking = cus.checking_for_id(account_no,"customer")
                if account_checking == "valid":
                
                        account = cus.get_cust_account(account_no)
                        password = input("Enter Password: ")
                        if password == account[6]:
                        
                                print('''What do you want to Update:
                                => Name                      => to Enter "Name"
                                => Phone No                  => to Enter "Phone No"
                                => Address                   => to Enter "Address"
                                => Customer Account Password => to Enter "Customer Password"
                                => Bank Account Password     => to Enter "Account Password"
                                => Account Balance           => to Enter "Account Type or balance or account"
                                => Account Type              => to Enter "Account Type"
                                => Branch ID                 => to Enter "Branch ID "
                                ''')
                        print()
                        update = input("Enter what do you want to update write by comma seperated like (Name, phone no, address): ")

                        updatingList = update.replace(" ","").lower().split(",")
                        for i in range(len(updatingList)):
                                if updatingList[i] == "name":
                                        cus.update_account(1,account[0])
                                elif updatingList[i] == "phoneno":
                                        cus.update_account(2,account[0])
                                elif updatingList[i] == "address":
                                        cus.update_account(4,account[0])
                                if updatingList[i] == "password":
                                                password1 = input("Enter which password do you want to update(customer password or account password): ").lower()
                                                if updatingList[i] == "customerpassword":
                                                        cus.update_account(6,account[0])
                                                elif updatingList[i] == "accountpassword":
                                                        cus.update_account(7,account[0])
                                elif updatingList[i] == "customerpassword":
                                                cus.update_account(6,account[0])
                                elif updatingList[i] == "accountpassword":
                                                cus.update_account(7,account[0])
                                elif updatingList[i] == "accountbalance" or updatingList[i] == "balance" or updatingList[i] == "amount":
                                                info = input("Enter whether yu want to deposit or withdraw: ")
                                                if info == "deposit" or info == "Deposit":
                                                        account_no = int(input("Enter account number: "))
                                                        account = cus.get_account(account_no)
                                                        password = input("Enter Password: ")
                                                        if password == account[1]:
                                                                amount = float(input("Enter amount to withdraw: "))
                                                                cus.deposit_amount(account,amount)
                                                        else:
                                                                print("Please Enter a Correct Password")
                                                                
                                                elif info == "withdraw" or info == "Withdraw":
                                                        account_no = int(input("Enter account number: "))
                                                        account = cus.get_account(account_no)
                                                        password = input("Enter Password: ")
                                                        if password == account[1]:
                                                                amount = float(input("Enter amount to withdraw: "))
                                                                cus.withdraw_amount(account,amount)
                                                        else:
                                                                print("Please Enter a Correct Password")
                                elif updatingList[i] == "accounttype":
                                        cus.update_account(3,account[0]) 
                                elif updatingList[i] == "branchid":
                                        cus.update_account(0,account[0]) 
                        else:
                                print("Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
        
        
        elif choice == 6:
                customer_id = int(input("Enter Your Customer ID Number: "))
                account_checking = cus.checking_for_id(customer_id,"customer")
                if account_checking == "valid":
                
                        customer = cus.get_cust_account(customer_id)
                        password = input("Enter Password: ")
                        if password == customer[6]:        
                                cus.display_acc_details(customer)   
                        else:
                                print("Please Enter a Correct Password")
        
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
        

        elif choice == 7:
                account_no = int(input("Enter Your Account Number: "))
                account_checking = cus.checking_for_id(account_no,"accounts")
                if account_checking == "valid":
                
                        account = cus.get_account(account_no)
                        password = input("Enter Password: ")
                        if password == account[1]:
                                cus.check_balance(account)
                        else:
                                print("Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
        
        elif choice == 8:
                customer_id = int(input("Enter Your Customer ID: "))
                account_checking = cus.checking_for_id(account_no,"customer")
                if account_checking == "valid":
                
                        account = cus.get_cust_account(customer_id)
                        password = input("Enter Password: ")
                        if password == account[6]:
                                cus.delete_customer_account(account)
                        else:
                                print("Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
        
        elif choice == 9:
                account_no = int(input("Enter Your Account Number: "))
                account_checking = cus.checking_for_id(account_no,"accounts")
                if account_checking == "valid":
                        account = cus.get_account(account_no)
                        password = input("Enter Password: ")
                        if password == account[1]:
                                cus.delete_bank_account(account)
                        else:
                                print("Please Enter a Correct Password")
                
                elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
        
        
        elif choice == 10:
                name = input("Enter your Full name: ") 
                phone_no = int(input("Enter your Phone no: e.g:(03123456779): "))
                nic = int(input("Enter your NIC: e.g:(42111058551): "))
                address = input("Enter your current home adress: ")
                branch_id = int(input("Enter Branch_id: "))
                cus.create_employee_account(name,phone_no,nic,address,branch_id)
        
        elif choice == 11:
              cus.display_employees()  

        elif choice == 12:
              account_no = int(input("Enter Your Account Number: "))
              account_checking = cus.checking_for_id(account_no,"employee")
              if account_checking == "valid":
                account = cus.get_emp_account(account_no)
                
                
                print('''What do you want to Update:
                                => Name                => to Enter "Name"
                                => Phone No            => to Enter "Phone No"
                                => Address             => to Enter "Address"
                                => Branch ID           => to Enter "Branch ID "
                                ''')
                print()
                
                update = input("Enter what do you want to update type by comma seperated like (Name, phone no, address): ")

                updatingList = update.replace(" ","").lower().split(",")
                for i in range(len(updatingList)):
                                if updatingList[i] == "name":
                                        cus.update_employee_account(1,account[0])
                                elif updatingList[i] == "phoneno":
                                        cus.update_employee_account(2,account[0])
                                elif updatingList[i] == "address":
                                        cus.update_employee_account(4,account[0])
                                elif updatingList[i] == "branchid":
                                        cus.update_employee_account(5,account[0])
              
              elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
       
        elif choice == 13:
             cus.display_transactions()

        elif choice == 14:
              account_no = int(input("Enter Your Account Number: "))
              account_checking = cus.checking_for_id(account_no,"accounts")
              if account_checking == "valid":
                        account1 = cus.get_transaction_id(account_no)
                        account = cus.get_account(account_no)
                        
                        password = input("Enter Password to show your transactions: ")
                        if password == account[1]:
                                cus.transactions(account1)
              
              elif account_checking == "not valid":
                      print("The Entered value is not valid or present") 
       

        elif choice == 15:
                break
        

