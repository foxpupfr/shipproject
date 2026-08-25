# Please read the commends carefully to understand the program 

#imports 
try: # Tries to import all the modules needed 
    import mysql.connector as s #will be used for everything around
    from datetime import datetime #will be mainly used for logging
    import time #will be used to program menu driven interface timings and all
    module_error_flag=False  # if no error occurs this flag will be set to false
except Exception as err:
    module_error=str(err)  # if error occurs the error will be converted into string
    module_error_flag=True  # Then the flag will be set to true 
                            # all of this is done to ensure every error is logged and thus helps in maintaince
#imports over



# function blocks for easy management

# function block for first run of program (fully hardcoded block)
 #most values here are hardcoded as to show examples and as such 
def first_run():
    log("#### program shipproject.py was started ####",escape_sequences="\n\n\n\n\n")
    def run_querie(*command):   #for error checking and handling also logs into the log.txt if the table exits 
        try: #here we check for existence of database with fact if error arises or not 
            cur1.execute(command[0])
            con1.commit()
            log("Table "+command[1]+" was not found so it was created")
            return True
        except s.errors.ProgrammingError: #here the error is used for propper logging of actions 
            log("Table "+command[1]+" already exits moving on...")
            return False

    #con0 was oppened to intiated the check for existence of database and create it if required
    con0 = s.connect(host="localhost", user="theblackfox", password="theblackfox90")
    cur0 = con0.cursor()
    if con0.is_connected() == True:
        log("connection 0 was connected")
    try:
        cur0.execute("create database shipproject")
        print("\n\nDatabase shipproject and connected tables were not found creating them please wait...")
        database_flag=0    
        log("Database shipproject was not found so it was created using connection0")
        time.sleep(1.5)  # some timing for looks 
    except s.errors.DatabaseError: # this means database was already present so it moved on 
        database_flag=1
        log("Database shipproject already exits moving on...") 
    con0.close()        #con0 was closed here 
    log("connection 0 was closed")
    global con1      #con1 is being opened here for all other interactions in this program with mysql
    con1 = s.connect(host="localhost",user="theblackfox",password="theblackfox90",database="shipproject",)
    if con1.is_connected() == True:  
        log("connection 1 was connected")
    global cur1   # cur1 is being made into global scope for future use 
    cur1 = con1.cursor()

#login and register tables and pre-inserts some values

    #creates register_table
    run_querie("create table register_list(user_id int primary key,email_address varchar(100) not null unique,password varchar(225) not null, first_name varchar(50) not null,last_name varchar(50) not null,age int not null,phonenumber bigint unique not null,adhar_id bigint unique not null,nationality varchar(50) not null,tc char(1) not null )","register_list")
         
    #creates staff_register_table
    if run_querie("create table staff_register_list(staff_id int primary key,email_address varchar(100) not null unique,password varchar(225) not null, first_name varchar(50) not null,last_name varchar(50) not null,age int not null,phonenumber bigint unique not null,adhar_id bigint unique not null,nationality varchar(50) not null,tc char(1) not null ,is_admin char(1),is_owner char(1))","staff_register_list"):
        #adds admin to staff tables so admin can add the other staffs 
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(1,'ownerforshipproject@gmail.com','owner','owner for','shipproject',18,9090190901,0010,'India','y','y','y')")
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin)values(2,'adminforshipproject@gmail.com','admin','admin for','shipproject',18,9090190991,00100,'India','y','y')")
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc)values(3,'staffforshipproject@gmail.com','staff','staff for','shipproject',18,9090190999,001000,'India','y')")
        con1.commit()
        log("all basic staff entries were added to staff register list")

        # The below values are commended just for the pupose of examples and showcase this is not a security letdown
        # Also the below values are generic examples in cases of staffs and admins 
        # Admins and staff can be removed or added but owner will be hardcoded 

        # owner's staff id : 1 
        # owner's password : owner
        # admin's staff id : 2
        # admin's password : admin
        # staff's staff id : 3
        # staff's password : staff

    #creates login checklist table
    run_querie("create table login_checklist(user_id int primary key,email_adress varchar(100) not null unique,phonenumber bigint not null,password varchar(225) not null)","login_checklist")

    #creates staff checklist table 
    if run_querie("create table staff_checklist(staff_id int primary key,email_adress varchar(100) not null unique,phonenumber bigint not null,password varchar(225) not null,is_admin char(1),is_owner char(1))","staff_checklist"):
        #adds admin to staff tables so admin can add the other staffs
        cur1.execute("insert into staff_checklist(staff_id,email_adress,phonenumber,password,is_admin,is_owner)values(1,'ownerforshipproject@gmail.com',9090190991,'owner','y','y')")
        cur1.execute("insert into staff_checklist(staff_id,email_adress,phonenumber,password,is_admin)values(2,'adminforshipproject@gmail.com',9090190901,'admin','y')")
        cur1.execute("insert into staff_checklist(staff_id,email_adress,phonenumber,password)values(3,'staffforshipproject@gmail.com',9090190999,'staff')")
        con1.commit()
        log("all basic staff entries were added to staff login checklist")
        
    #creates ship history
    run_querie("create table ship_history(ship_name varchar(50),user_id int, seat_no int, allocation varchar(50), ticket_id int,food varchar(50))","ship_history")

    #creates ticket history
    run_querie("create table ticket_history(ship_name varchar(50),user_id int, ticket_id int,ticket_validity varchar(50))","ticket_history")

    #creates foodlist
    run_querie("create table foodlist(user_id int(11),ticket_id int(11),food_coupon_id int(11),food_item_name varchar(200))","foodlist")

    #creates table for ships and pre-inserts some values

    tables_to_create_list=["mv_kavaratti","pre_mv_kavaratti","mv_arabian_sea","pre_mv_arabian_sea","mv_lakshadweep_sea","pre_mv_lakshadweep_sea","mv_amindivi","pre_mv_amindivi","hsc_parali","pre_hsc_parali"]
    # the list has names of ship through which it will itrate to form the ship tables

    for table_name_index in range(0,len(tables_to_create_list)):
        table_to_create=tables_to_create_list[table_name_index]
        if run_querie("create table "+table_to_create+"(ship_name varchar(50), user_id int, seat_no int, allocation varchar(50), ticket_id int,ticket_validity varchar(50),food varchar(50))",table_to_create):
            for seat_no in range(1,51):
                seat_no_str=str(seat_no)
                cur1.execute("insert into "+table_to_create+"(ship_name,seat_no,allocation,ticket_validity,food)values('"+table_to_create+"','"+seat_no_str+"','disallocated','Not booked','not booked')")
                con1.commit()
            log("all basic values were inserted into "+table_to_create)

    if database_flag==0: #this is database flag from con0 side which shows the confirmation (check con0 for reference)
        print("\nDone !")
        time.sleep(1) # some timing for looks 
        print("\n"*100) #prints 100 newlines in intention to clear terminal
#block end


# fuction block for user regiasteration (part 1)
def user_registeration1():
    email_address = input("\n\t\t\b\bPlease enter you email : ") # Takes in all the basic user values for registeration
    print("\n\t\t\b\b### please remember your password ###\n".upper()) 
    password = input("\t\t\b\bPlease enter a secure password : ")
    password0 = input("\t\t\b\bPlease reconfirm your password : ")
    flag = 0
    if password != password0: # Checks if both entered passwords are not same, condition is True it makes the flag = 1 
        flag = 1               # flag = 1 here indicates passwords didn't match
        print("\n\n\t\tBoth passwords are not the same !!!\n")
        log("user didn't type matching passwords")
        print("\t\tredirecting you to menu again !")
    else:                      # If the passwords were same, above condition was deemed False it makes flag = 0
        flag = 0               # flag = 0 here means passwords did match
    return flag,password,email_address   
# Here it returns the above entered info and also the flag to the place function was called from 
# block end

# fuction block for user registeration (part 2)
# This block is only entred if the passwords in first block matched 
# That is because it depends on the flag varible in user_registeration2() refer to the fucntion for more info
def user_registeration2(password,email_address):
    cur1.execute("select max(user_id) from register_list")  #selects the biggest user od or the last registered user id from table 
    c = cur1.fetchall() # just stores the alst regisered user id 
    if c[0][0]==None:
        user_id = 0 # if no user id was found meaning the database was just created it sets default to 0
    else:
        user_id = c[0][0] + 1
    first_name = input("\t\t\b\bPlease enter your first name : ")
    last_name = input("\t\t\b\bPlease enter your last name : ")
    age = input("\t\t\b\bPlease enter your age : ")
    phonenumber = input("\t\t\b\bPlease enter your phone number  : ")
    adhar_id = input("\t\t\b\bPlease enter your adhar id : ")
    nationality = input("\t\t\b\bPlease enter your nationality : ")
    tc = input("\t\t\b\bDo you comply with T&C (y or n) : ")

    values_1 = (user_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc)
    values_2 = (user_id,email_address,phonenumber,password)

    try:
        cur1.execute("insert into register_list(user_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values_1)
        cur1.execute("insert into login_checklist(user_id,email_adress,phonenumber,password)values(%s,%s,%s,%s)",values_2)
        print("\n\tsuccesfully registered !\n")
        print("\n\tyour user id is :",user_id)
        print("\tplease remember your user_id and password")
        log("a user was registered !")
    except s.errors.DataError:
        print("\n\n\t#### Error : Please enter appropriate values above ####".upper())
        log("user entered inappropriate value")
    except s.errors.IntegrityError:
        print("\n\n\t#### Error : Please enter your own email, phonenumber, adhar ID and check for its correctness ####")
        log("user entred wrong email,phonenumber etc")
    con1.commit()
# block end


# fuction block for staff registeration1
def staff_registeration1():
    email_address = input("\n\t\t\b\bPlease enter you email : ")
    print("\n\t\t\b\b### please remember your password ###\n".upper())
    password0 = input("\t\t\b\bPlease enter a secure password : ")
    password1 = input("\t\t\b\bPlease reconfirm your password : ")
    flag = 0
    if password0!=password1:
        flag = 1
        print("\n\n\t\tBoth passwords are not the same !!!\n")
        log("user didn't type matching passwords")
        print("\t\tredirecting you to menu again !")
    else:
        flag = 0
    return flag,password0,email_address
# block end

# fuction block for staff registeration2
def staff_registeration2(password,email_address,privilage_level,staff_type):
    staff_id=0
    cur1.execute("select max(staff_id) from staff_register_list")
    tempvar1=cur1.fetchall()
    staff_id=str(tempvar1[0][0])
    if staff_id=="None":
        staff_id="0"
    else:
        staff_id=str(int(staff_id)+1)
    first_name = input("\t\t\b\bPlease enter your first name : ")
    last_name = input("\t\t\b\bPlease enter your last name : ")
    age = input("\t\t\b\bPlease enter your age : ")
    phonenumber = input("\t\t\b\bPlease enter your phone number  : ")
    adhar_id = input("\t\t\b\bPlease enter your adhar id : ")
    nationality = input("\t\t\b\bPlease enter your nationality : ")
    tc = input("\t\t\b\bDo you comply with T&C (y or n) : ")
    if privilage_level==3 and staff_type=="staff":
        is_admin="n"
        is_owner="n"
    elif privilage_level==4 and staff_type=="staff":
        is_admin="n"
        is_owner="n"
    elif privilage_level==4 and staff_type=="admin":
        is_admin="y"
        is_owner="n"
    values=(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)
    try:
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values)
        values=(staff_id,email_address,phonenumber,password,is_admin,is_owner)
        cur1.execute("insert into staff_checklist(staff_id,email_adress,phonenumber,password,is_admin,is_owner)values(%s,%s,%s,%s,%s,%s)",values)
        print("\n\tsuccesfully registered !\n")
        print("\n\tyour staff id is :",staff_id)
        print("\tplease remember your staff_id and password")
        log("a staff was registered !")
#    except s.errors.DataError:
#        print("\n\n\t#### Error : Please enter appropriate values above ####".upper())
#        log("user entered inappropriate value")
    except s.errors.IntegrityError:
        print("\n\n\t#### Error : Please enter your own email, phonenumber, adhar ID and check for its correctness ####")
        log("user entred wrong email,phonenumber etc")
    con1.commit()
# block end

#function block for login 
def staff_login():
        log("staff choosed login option")
        staff_id0=input("\n\t\t\b\bPlease enter you user id :")
        try:
            cur1.execute("select password from staff_checklist where staff_id = '%s'"%staff_id0)
            passwd=cur1.fetchall()
            cur1.execute("select password from staff_checklist where staff_id = '%s'"%staff_id0)
            passwd=cur1.fetchall()
            password1=passwd[0][0]
            for i in staff_id0:
                if i not in ("1234567890"):
                    print("\n\t\t\b\b### Enter proper user id ###\n")
                    password2=None
                    break
                else:
                    password2=input("\t\t\b\bPlease enter your pasasword :")
            if password1==password2:
                cur1.execute("select is_admin from staff_checklist where staff_id = '%s'"%staff_id0)
                is_admin=cur1.fetchall()
                if is_admin[0][0]=="y":
                    cur1.execute("select is_owner from staff_checklist where staff_id = '%s'"%staff_id0)
                    is_owner=cur1.fetchall()
                    if is_owner[0][0]=="y":
                        log("owner succesfully logged in")
                        print("\n\t\t\b\blogin succesfull")
                        return 4,staff_id0
                    else:
                        log("admin succesfully loged in")
                        print("\n\t\t\b\blogin succesfull")
                        return 3,staff_id0
                else:
                    log("staff succesfully loged in")
                    print("\n\t\t\b\blogin succesfull")
                    return 2,staff_id0
            else:
                log("login failed")
                if password2==None:
                    pass
                else:
                    print("\n\t\t\b\b### Either staff iad or password is wrong ###\n")
                return 0
        except IndexError:
            return 0
            print("\n\t\t\b\b### Either user id or password is wrong ###\n")
#end block


#function block for login 
def login():
        log("user choosed user login option from login menu") 
        user_id0=input("\n\t\t\b\bPlease enter you user id :") #picks up user id 
        try:
            cur1.execute("select password from login_checklist where user_id = '%s'"%user_id0)
            passwd=cur1.fetchall() # fetchs password for comparing
            password1=passwd[0][0] # extracts password for comparing form [(passwd,),]
            for i in user_id0:
               if i not in ("1234567890"):
                    print("\n\t\t\b\b### Enter proper user id ###\n") #checks user if if its valid
                    log("login failed user id",user_id0,"was inappropriate")
                    return 0 #return fucntion if its not valid
               else: 
                    password2=input("\t\t\b\bPlease enter your password :")
            if password1==password2:
                log("user succesfully loged in with user id",user_id0)
                print("\n\tlogin succesfull")
                return 1,str(user_id0)
            else:
                log("login failed user with user id",user_id0,"used wrong password")
                print("\n\t\t\b\b### Either user id or password is wrong ###\n")
                return 0
        except IndexError:
            print("\n\t\t\b\b### Either user id or password is wrong ###\n")
            return 0
#end block

#fucntion block for staff removal
def remove_staff(privilage_level,staff_type):
    tempvar=int(input("\n\t\tplease enter staff id of staff you want to delete : "))
    staff_id=(tempvar,)
    choice_confirmation=input("\n\t\tAre you sure you want to continue : ")
    if choice_confirmation!="y":
        return
    if privilage_level==4 and staff_type=="admin":
        cur1.execute("select is_owner from staff_checklist where staff_id=%s",staff_id)      
        authority_check=cur1.fetchall()
        if authority_check[0][0]=="y":
            print("\n\t\tyou dont have permission to remove yourself")
            return
        cur1.execute("select is_admin from staff_checklist where staff_id=%s",staff_id)
        authority_check=cur1.fetchall()
        if authority_check[0][0]=="y" and staff_type=="staff":
            print("\n\t\tThis part of menu is meant to remove admins\nplease use staff removal part of menu")
            return
        if authority_check[0][0]=="n" and staff_type=="admin":
            print("\n\t\tThis part of menu is meant to remove normal staffs\nplease use admin removal part of menu")
            return
        cur1.execute("delete from staff_checklist where staff_id=%s",staff_id)
        cur1.execute("delete from staff_register_list where staff_id=%s",staff_id)
        con1.commit()
    else:
        cur1.execute("select is_owner from staff_checklist where staff_id=%s",staff_id)
        authority_check=cur1.fetchall()
        if authority_check[0][0]=="y":
            print("\n\t\tyou dont have permission to remove owner")
            return
        cur1.execute("select is_owner from staff_checklist where staff_id=%s",staff_id)
        authority_check=cur1.fetchall()
        if authority_check[0][0]=="y":
            print("\n\t\tyou dont have permission to remove another admin")
            return
        try:
            cur1.execute("delete from staff_checklist where staff_id=%s",staff_id)
            cur1.execute("delete from staff_register_list where staff_id=%s",staff_id)
            con1.commit()
        except ZeroDivisionError:
            print("\n\t\tunkwon error in staff removal")
#block end 

#function block for booking ticket
def book_ticket(option_given,user_id,booking_type="booking"):    
    payment_check=input("\n\t\t\b\bHave you have completed your payment at counter (y/n) : ")
    def ship_filter_and_book(ship_name,user_id):
        cur1.execute("select min(seat_no) from "+ship_name+" where allocation='disallocated'")
        tempvar1=cur1.fetchall()
        seat_no=str(tempvar1[0][0])
        cur1.execute("select max(ticket_id) from ticket_history")
        tempvar2=cur1.fetchall()
        ticket_id=tempvar2[0][0]
        if seat_no=="None" and booking_type=="prebooking":
            print("\n\t\t\b\bSorry to dissapoint you but all prebooking seats are booked too !\n\t\t\b\bPlease book tickets another day !")
        if seat_no=="None":
            print("\n\t\t\b\bSorry to dissapoint you but all seats are booked !\n\t\t\b\bPlease use the pre-booking area for travelling another day !")
        else:
            if ticket_id==None:
                cur1.execute("insert into ticket_history(ship_name,user_id,ticket_id,ticket_validity)values('"+ship_name+"',"+user_id+",1,'valid')")
                cur1.execute("update "+ship_name+" set user_id="+user_id+",ticket_id=1,ticket_validity='valid',allocation='allocated' where seat_no="+seat_no)
                con1.commit()
            else:
                ticket_id=str(ticket_id+1)
                cur1.execute("insert into ticket_history(ship_name,user_id,ticket_id,ticket_validity)values('"+ship_name+"',"+user_id+","+ticket_id+",'valid')")
                cur1.execute("update "+ship_name+" set user_id="+user_id+",ticket_id="+ticket_id+",ticket_validity='valid',allocation='allocated' where seat_no="+seat_no)
                con1.commit()

    #for prebooking
    if payment_check in ["y","Y"] and booking_type=="prebooking":
        if option_given==1:
            ship_filter_and_book("pre_mv_kavaratti",user_id)
            return True
        if option_given==2:
            ship_filter_and_book("pre_mv_arabian_sea",user_id)
            return True
        if option_given==3:
            ship_filter_and_book("pre_mv_lakshadweep_sea",user_id)
            return True
        if option_given==4:
            ship_filter_and_book("pre_mv_amindivi",user_id)
            return True
        if option_given==5:
            ship_filter_and_book("pre_hsc_parali",user_id)
            return True

    #for normal booking 
    elif payment_check in ["y","Y"] and booking_type=="booking":
        if option_given==1:
            ship_filter_and_book("mv_kavaratti",user_id)
            return True
        if option_given==2:
            ship_filter_and_book("mv_arabian_sea",user_id)
            return True
        if option_given==3:
            ship_filter_and_book("mv_lakshadweep_sea",user_id)
            return True
        if option_given==4:
            ship_filter_and_book("mv_amindivi",user_id)
            return True
        if option_given==5:
            ship_filter_and_book("hsc_parali",user_id)
            return True

    elif payment_check in ["n","N"]:
        print("\n\t\t\b\bPlease pay ticket fees at the counter")
    else:
        print("\n\t\t\b\b### please enter appropriate values ###".upper())
#block end

#fucntion block for seeing info regarding diffrent matters
def see_info(info_type):
    def select_ship(ship_type="normal"):
        if ship_type=="pre":
            print("\n\t\t1.Pre-MV Kavaratti")
            print("\t\t2.Pre-MV Arabian sea")
            print("\t\t3.Pre-MV Lakshadweep sea")
            print("\t\t4.Pre-MV Amindivi")
            print("\t\t5.Pre-HSC Parali")
            print("\t\t6.Exit")
            opt=int(input("\n\t\tPlease choose from any of the option given above (1, 2, 3, 4, 5, 6) : "))
            if opt==1:
                return "pre_mv_kavaratti"
            if opt==2:
                return "pre_mv_arabian_sea"
            if opt==3:
                return "pre_mv_lakshadweep_sea"
            if opt==4:
                return "pre_mv_amindivi"
            if opt==5:
                return "pre_hsc_parali"
            if opt==6:
                return
        if ship_type=="normal":
            print("\n\t\t1.MV Kavaratti")
            print("\t\t2.MV Arabian sea")
            print("\t\t3.MV Lakshadweep sea")
            print("\t\t4.MV Amindivi")
            print("\t\t5.HSC Parali")
            opt=int(input("\n\t\tPlease choose from any of the option given above (1, 2, 3, 4, 5, 6) : "))
            if opt==1:
                return "mv_kavaratti"
            if opt==2:
                return "mv_arabian_sea"
            if opt==3:
                return "mv_lakshadweep_sea"
            if opt==4:
                return "mv_amindivi"
            if opt==5:
                return "hsc_parali"
            if opt==6:
                return

    if info_type=="ship info-current":
        ship_name=select_ship()
        cur1.execute("select * from "+ship_name)
        info=cur1.fetchall()
        tableconv(info,table_name=ship_name,escape_sequences="\n\n\t\t")
    if info_type=="ship info-prebooking":
        ship_name=select_ship(ship_type="pre")
        cur1.execute("select * from "+ship_name)
        info=cur1.fetchall()
        tableconv(info,table_name=ship_name,escape_sequences="\n\n\t\t")
    if info_type=="ship history":
        cur1.execute("select * from ship_history")
        info=cur1.fetchall()
        if info!=[]:
            tableconv(info,table_name="ship_history",escape_sequences="\n\n\t\t")
        else:
            print("\t\t\b\btable empty !")
    if info_type=="ticket history":
        cur1.execute("select * from ticket_history")
        info=cur1.fetchall()
        if info!=[]:
            tableconv(info,table_name="ticket_history",escape_sequences="\n\n\t\t")
        else:
            print("\t\t\b\btable empty !")
#end of block


#function block for deactivating and updating tickets
def update_ticket(update_type="deactivate"):
    ticket_id=int(input("\n\t\tPlease enter ticket id you want to "+update_type+" : "))
    ticket_id=(ticket_id,)
    cur1.execute("select ship_name from ticket_history where ticket_id=%s",ticket_id)
    ship_name=cur1.fetchall()
    ship_name=ship_name[0][0]

    if update_type=="deactivate":
        cur1.execute("select * from ticket_history where ticket_id=%s",ticket_id)
        ticket_info1=cur1.fetchall()
        cur1.execute("select * from "+ship_name+" where ticket_id=%s",ticket_id)
        ticket_info2=cur1.fetchall()
        print("\n")
        tableconv(ticket_info1,table_name="ticket_history",escape_sequences="\t\t")
        print("\n")
        tableconv(ticket_info2,table_name=ship_name,escape_sequences="\t\t")
        confirmation=input("\n\t\tThe ticket would be registered deactivated on both these tables, do you want to continue (y/n) : ")
        if confirmation in ["y","Y"]:
            cur1.execute("update ticket_history set ticket_validity='deactivated' where ticket_id=%s",ticket_id)
            cur1.execute("update "+ship_name+" set ticket_validity='deactivated',allocation='disallocated',food='not booked' where ticket_id=%s",ticket_id)
            con1.commit()
            print("\n\t\tchanges were made !")
        else:
            print("\n\t\tproccess cancelled !")
            return

    if update_type=="refund":
        cur1.execute("select * from ticket_history where ticket_id=%s",ticket_id)
        ticket_info1=cur1.fetchall()
        cur1.execute("select * from "+ship_name+" where ticket_id=%s",ticket_id)
        ticket_info2=cur1.fetchall()
        print("\n")
        tableconv(ticket_info1,table_name="ticket_history",escape_sequences="\t\t")
        print("\n")
        tableconv(ticket_info2,table_name=ship_name,escape_sequences="\t\t")
        confirmation=input("\n\t\tThe ticket would be registered refunded on both these tables, do you want to continue (y/n) : ")
        if confirmation in ["y","Y"]:
            cur1.execute("update ticket_history set ticket_validity='refunded' where ticket_id=%s",ticket_id)
            cur1.execute("update "+ship_name+" set ticket_validity='refunded',allocation='disallocated',food='not booked' where ticket_id=%s",ticket_id)
            con1.commit()
            print("\n\t\tchanges were made !")
        else:
            print("\n\t\tproccess cancelled !")
            return
#block end

#fucntion block for seeing tickets booked by specific user who logged in 
def see_tickets_for_user(user_id):
    print("\n\t\t\b\b1.active tickets")
    print("\t\t\b\b2.refunded tickets")
    print("\t\t\b\b3.inactive tickets")
    print("\t\t\b\b4.exit")
    opt=int(input("\n\t\t\b\bPlease choose from above options 1, 2, 3, 4 : "))
    if opt==1:
        ship_namelist_to_scan=["mv_kavaratti","pre_mv_kavaratti","mv_arabian_sea","pre_mv_arabian_sea","mv_lakshadweep_sea","pre_mv_lakshadweep_sea","mv_amindivi","pre_mv_amindivi","hsc_parali","pre_hsc_parali"]

        final_list_of_active_tickets=[]

        for ship_name_index in range(0,len(ship_namelist_to_scan)):
            ship_name=ship_namelist_to_scan[ship_name_index]
            cur1.execute("select * from "+ship_name+" where user_id="+user_id+" and ticket_validity='valid'")
            tempvar=cur1.fetchall()
            for index in range(0,len(tempvar)):
                final_list_of_active_tickets.append(tempvar[index])
        tableconv(final_list_of_active_tickets,table_name="mv_kavaratti",escape_sequences="\t\t\b\b")
    if opt==2:
        cur1.execute("select * from ticket_history where user_id="+user_id+" and ticket_validity='refunded'")
        refunded_tickets=cur1.fetchall()
        tableconv(refunded_tickets,table_name="ticket_history",escape_sequences="\t\t\b\b")
    if opt==3:
        cur1.execute("select * from ticket_history where user_id="+user_id+" and ticket_validity='deactivated'")
        deactivated_tickets=cur1.fetchall()
        tableconv(deactivated_tickets,table_name="ticket_history",escape_sequences="\t\t\b\b")
    if opt==4:
        print("\n\t\t\b\bexiting...")
        return
    else:
        print("\n\t\t\b\bcancelled !")
        return
#block end

#function block for booking food 
def book_food(user_id):

    ticket_id=int(input("\n\t\t\b\bPlease enter you ticket id which you wnat to book food for : "))

    food_list=["Rotti and Beef chops","Dosa and Curries","Lemon rice","Biriyani","Idli and Curries","Meals","Al-faham","Fried rice and Chilli gopi or Chilli chicken","Chole batture","Aloo paratha","Butter garlic naan and palak paneer","Chicken noodles","Mushroom soup","Vada pav","Omelette","Fish fry","Samosa and Chuttney","Popcorn","Burger (type choosable at food stall)","Pizza (type choosable at food stall)","Mango lassi","Soda items (can be selected from food stall)","Tea/Coffe (can be selectd from food stall)","Fresh lime","Water"]

    tableconv(food_list,escape_sequences="\n\t\t\b\b",list_only=True,numbered=True,full_lined=True)
   
    food_selection=int(input("\n\t\t\b\bPlease enter the number of food item you want to book (1-25) :"))
    food_selection-=1
    payment_check=input("\n\t\t\b\bDid you complete the payment at the counter (y/n :) ")
    food_item_name=food_list[food_selection]

    if payment_check in ["Y","y"]:
        cur1.execute("select max(food_coupon_id) from foodlist")
        food_coupon_id=cur1.fetchall()
        food_coupon_id=food_coupon_id[0][0]
        if food_coupon_id==None:
            food_coupon_id=0
        else:
            food_coupon_id+=1
        values=(user_id,ticket_id,food_coupon_id,food_item_name)
        cur1.execute("insert into foodlist(user_id,ticket_id,food_coupon_id,food_item_name)values(%s,%s,%s,%s)",values)
        con1.commit()
        print("\n\t\t\b\b"+food_item_name,"was succesfully booked !")
    else:
        print("\n\t\t\b\bPlease complete the payment at counter !")
#block end

#function block for checking of emails and passwords as such since i dont wanna repeat it nor huge pain reading stuff 
def valid_data_catching(typelist,usecase):

    #a list containing values to return get passed or so called a typelist by me 
    for type in typelist:       #we itrate through the typelist to featch all the values neccesary
        
        if type == "email_address":
            
            def email_local_part_validation():      #validation of the local part 
                special_chars = "._-+"      #speical chars which are allowed in email address
                if len(local_part) > 64:    #local part checking starts
                    tableconv("part before \"@\" must be less than or equal to 64 charecters",warning_box = True)
                    pass
                elif len(local_part) < 1:
                    tableconv("Part before \"@\" must be less than or equal to 1 charecter",warning_box= True)
                    pass
                if local_part[0].isalnum() == False or local_part[len(local_part) - 1].isalnum() == False:
                    tableconv("Part before \"@\" must start and end with alpha-numeric charecters",warning_box = True)
                error_flag0 = 0
                error_flag1 = 0
                for i in range(len(local_part)):
                    if i == len(local_part) - 1:
                        pass
                    elif local_part[i] in special_chars and local_part[i + 1] in special_chars and error_flag0 == 0:
                        tableconv("\".\" ,\"_\" ,\"-\" ,\"+\" cannot be used consiqutively",warning_box = True)
                        error_flag0 = 1
                    if local_part[i] not in special_chars and local_part[i].isalnum() == False and error_flag1 == 0:
                        tableconv("Charecters other than \".\" ,\"_\" ,\"-\" ,\"+\" cannot be used in email",warning_box = True)
                        error_flag1 = 1

            def email_domain_validation():  #validation of domain
                special_chars = ".-"
                if domain.count(".") < 1:
                    tableconv("A domain must contain at least one \".\"",warning_box = True)
                if len(domain) < 4 or if len(domain) > 255:
                    tableconv("A domain should be between 4 and 255 charecters long",error_box = True)
                if domain[0].isalnum() == False or domain[len(domain) - 1].isalnum() == False:
                    tableconv("A domain cannot start or end with special charecters",warning_box = True)
                error_flag0 = 0
                error_flag1 = 0
                for i in range(len(domain)):
                    if i == len(domain) - 1:
                        pass
                    elif domain[i] + domain[i + 1] in ["..",".-","-."] and error_flag0 == 0:
                        tableconv("A domain cannot have \".\", \"-\" used consiqutivel",warning_box = True)
                        error_flag0 = 1
                    if domain[i] not in special_chars and domain[i].isalnum() == False and error_flag1 == 0:
                        tableconv("A domain cannot have special charecters other than \".\", \"-\"",warning_box = True)
                        error_flag1 = 1
                    label_list = domain..split(".")
                    for label in range(len(label_list)):
                        if label == len(label_list) - 1:
                            if len(label_list[label]) < 2 or len(label_list[label]) > 63:
                                tableconv("The final label in a domain should be between 2 and 63 charcters long",warning_box = True)
                            if label_list[label].isalnum() == False:
                                tableconv("The final label in a domain should only contain alphabets",warning_box = True)
                        elif len(label_list[label]) < 1 or len(label_list[label]) > 63:
                            tableconv("The labels should between 1 and 64 charecters long",warning_box = True)

            for s in range(3):
                email = input("Please enter a valid email address : ")
                error_flag = 0

                if len(email) > 320:        #global checking for errors
                    tableconv("An email cannot have more than 320 charecters",warning_box = True)
                    error_flag = 1
                if " " in email:
                    tableconv("An email cannot contain whitespaces", warning_box = True)
                    error_flag = 1
                if email.count("@") != 1:
                    tableconv("An email must contain one \"@\" symbol, not more not less",warning_box = True)
                    error_flag = 1 

                if error_flag == 0:      #splitting of local part and domain for seprate validy chekcing
                    local_part,domain = email.split("@")    #splitting only happens if its free from global errors
                    
                    if local_part == "" or domain == "":        #if any of parts are missing
                        tableconv("There should be a part before and after the \"@\" symbol",warning_box =True)
                    else:   #if parts are not missing it enters else block
                        if email_local_part_validation() == None or email_domain_validation() == None:
                            return None
                        else:
                            return email_local_part_validation() + "@" + email_domain_validation()
                        
               
                

        elif type == "password":
            pass
        elif type == "name":
            pass 
        elif type == "phonenumber":
            pass
        elif type == "adhar_id":
            pass
        elif type == "age":
            pass
        elif type == "tc":
            pass
#block end 

#fucntion block for custom table
"""
This is indended as a custom function which can draw tables for this program and the tables drawn will change according to the arguments passed 

-- a input_list is passed first which can be nested list or not nested
-- passing a table name as argument will draw headers with the feilds of the table if its valid in database shipproject
-- passing valid escape_sequences will allow table to follow escape Sequences
-- passing a valid charecter to custom_corner will draw table with that corner
-- passing valid string into table_headers will draw table with it as a head while list_only is true
-- if list only is true it will draw single column table (nested list is not allowed here)
-- enabling full_lined will draw tables with lines in between after the headers
-- enabling numbered will draw numbered single column tables
-- enabling bulleted by giving it a valid charecter to use as bullets wull draw bulleted single column tables
-- enabling warning box draws a box with "!" containing the content passed into input_string indicating warning 
-- enabling error_box draws a box with "#" containing the content passed into input_string indicating a error
"""
def tableconv(input_data,table_name = "NA",escape_sequences = "\n",custom_corner = "o",table_headers = "NA",list_only = False,full_lined = False,numbered = False,bulleted = "NA",warning_box = False, error_box = False,menu = False):
    
    input_string = "NA"     #this is would mean you can pass data without worrying about list or strings 
    if type(input_data) is str:
        input_string = input_data
    elif type(input_data) is list:
        input_list = input_data

    #this will take advantage of single column table drawing part if the function and line2
    if input_string != "NA":
        list_only = True
        if menu == True:
            input_list = input_string.split(",")
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "|"
            box_char2 = "-"
        elif warning_box == True: 
            input_list = [input_string,]
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "!"
            box_char2 = "!"
            custom_corner = "!"
        elif error_box == True:
            input_list = [input_string,]
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "#"
            box_char2 = "#"
            custom_corner = "#"
    else:
        box_char = "|"
        box_char2 = "-"


    #prints the table lines for [()]    (rows and columns)
    def line1():
        print(escape_sequences+custom_corner+"-",end="")
        for column in range(0,column_no):
            print("-"*lengthiest_data_list[column],end="")
            if column==column_no-1:
                print("-"+custom_corner)
                break
            print("-"+custom_corner+"-",end="")

    #prints the table lines for []  (single column)
    def line2():
        print(escape_sequences + custom_corner + box_char2,end="")
        print(box_char2 * lengthiest_data,end="")
        print(box_char2 + custom_corner)

    #calculates the padding and prints it along for [()] (rows and columns)
    def calc_padding1(row,column,content):
        padding_length=lengthiest_data_list[column]-len(str(input_list[row][column]))    
        content+=" "*padding_length
        return content

    #calculates the padding and prints it along for [] (single column)
    def calc_padding2(index,content):
        padding_length=lengthiest_data-len(str(input_list[index]))
        padding=" "*padding_length
        content+=padding
        return content

    #takes normal list for table conversation
    if list_only==True:
        
        #inserts table headers if present same like below but diffrent value which take input
        if table_headers!="NA":
            input_list.insert(0,table_headers)

        #for numbered single column tables
        if numbered == True:
            if table_headers == "NA":   #makes an exception for numbering if headers are given
                for index in range(0,len(input_list)):
                    number = str(index+1) + "."
                    input_list[index] = number + input_list[index]
            else:
                for index in range(1,len(input_list)):
                    number=str(index) + "."
                    input_list[index] = number + input_list[index]

        #for bulleted single column tables
        if bulleted != "NA":
            for index in range(1,len(input_list)):
                input_list[index] = bulleted + " " + input_list[index]

        #sets number of columns 
        index_count=len(input_list)

        #creates a variable named lengthiest_data containing the largest data length in the whole list
        lengthiest_data=0   #common for both variants of tables
        for index in range(0,index_count):
            if len(input_list[index]) > lengthiest_data:
                lengthiest_data=len(input_list[index])

        #prints the single columed table variant
        line2()
        escape_sequences=escape_sequences.replace("\n","")
        for index in range(0,index_count):
            if index==0 and table_headers!="NA":
                content=escape_sequences + box_char + " " + input_list[index]
                content=calc_padding2(index,content)
                content += " " + box_char
                print(content)
                line2()
            else:
                content = escape_sequences + box_char + " " + input_list[index]
                content = calc_padding2(index,content)
                content+=" " + box_char
                print(content)
                if full_lined==True:    #activates if full_lined is enabled
                    line2()
        if full_lined==False:
            line2()

    #prints the table variant with rows and columns
    if list_only==False:
        #sets number of rows and number of columns
        row_no=len(input_list) 
        column_no=len(input_list[0])

        #inserts table headers if table name given
        if table_name!="NA":
            table_headers=[]    
            cur1.execute("desc "+table_name)
            table_desc=cur1.fetchall()
            for desc_row in range(0,len(table_desc)):
                table_headers.append(table_desc[desc_row][0])
            input_list.insert(0,table_headers)
            row_no=len(input_list) 
            column_no=len(input_list[0])
            headers_flag=0
        else:
            headers_flag=1

        #creates a list named lengthiest_data_list containing the largest data lengths in each column 
        lengthiest_data_list=[]
        for column in range(0,column_no):
            lengthiest_data=0
            for row in range(0,row_no):
                if len(str(input_list[row][column]))>lengthiest_data:
                    lengthiest_data=len(str(input_list[row][column]))
            lengthiest_data_list.append(lengthiest_data)

        #actual part which converts to table
        line1()
        escape_sequences=escape_sequences.replace("\n","")
        for row in range(0,row_no):
            full_content=""     #this is done so that no error occurs in idle since all data is stored in ram before printing
            for column in range(0,column_no):
                if column==0:
                    content=escape_sequences+"| "
                    content+=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" | "
                    full_content+=content
                    continue
                if column==column_no-1 and headers_flag==0:
                    content=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" |"
                    full_content+=content
                    print(full_content)
                    line1()
                    headers_flag=1
                    continue
                if column==column_no-1:
                    content=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" |"
                    full_content+=content
                    print(full_content)
                    if full_lined==True:
                        line1()
                    continue
                content=str(input_list[row][column])
                content=calc_padding1(row,column,content)
                content+=" | "
                full_content+=content
        if full_lined==False: #activates if full_lined is enabled
            line1()
#block end

# function block for loggging something
def log(log_input,escape_sequences="",error=False):
    timestamp=str(datetime.now())[:23:]     #sliced the string to avoid too much precision
    if error==True:
        l=open("error_log.txt","a") #if it was a error which was not intented for user will be logged in error_log.txt
    else:
        l=open("log.txt","a") #if it was a normal log it will be logged here but still wont be showed to user
    l.write(escape_sequences+"["+timestamp+"] "+log_input+"\n")
    l.close()
if module_error_flag==True: #logs import errors if any 
    log(module_error,error=True)
# block end 

# Function blocks end here 











# actual command line interface code

first_run() # Routes you back to the intialization run of the program in theroy this function runs first 

#main menu
print("\n")
print("               __-------___")
print("             _(            )__----- _")
print("            (  --Developed by        )")             # just an ASCII art for looks
print("             (___  Milan Tom Suresh   )_")
print("                 (___ Abhiram Dinesh    )")
print("                     (__                ) ")
print("                         (__      _   _  ) \t\t#-----------------------------------------------#")
print("                            (    ) (  )(  )\t\t|                                               |")
print("                            (   )   ( ) ( )\t\t|      WELCOME TO SHIP MANANGEMENT SOFTWARE     |")
print("                             ( )  ()( ) ( )\t\t|                                               |")
print("                             __    __    __\t\t#-----------------------------------------------#")
print("                            |==|  |==|  |==|")
print("                          __|__|__|__|__|__|__")
print("                        __|___________________|___")     # I copied that table from my own tableconv funtion
print("                     __|__[]__[]__[]__[]__[]__[]__|___")
print("                    |............................o.../")
print(r"""                    \.............................../""")
print("               hjw_,~')_,~')_,~')_,~')_,~')_,~')_,~')/,~')_")



while con1.is_connected() == True:   # This puts program into loop untill user quits
    log("user entered the main program")   
    print("\n\nPlease log in or register ( chose options 1, 2, 3 ) :")
    tableconv("1.log in,2.register ( If you don't have an account already ),3.exit program",menu = True)
    try:
        opt=input("\nPlease enter 1, 2, 3 : ") #opt will be used for main menu options
        if opt not in ["1","2","3"]:
            print("### please choose appropriate option ###".upper())
#end of main menu


        #login menu 
        while opt=="1":
            log("user entred login menu")
            tableconv("1.login,2 login,3.go back to main menu",escape_sequences = "\n\t",menu = True)
            opt4=input("\n\tPlease enter 1, 2, 3 : ") #opt4 will be used for login menu
            if opt4=="1":
                log("user choosed normal login")
                login_check=login()         #redirects you to login and catches the value it returns 
            if opt4=="2":
                log("user choosed staff login")
                login_check=staff_login()   #redirects you to login as above and does same but for staff
            if opt4=="3":
                log("user returned to main menu")
                break                       #redirects you back to the main menu
            if opt4 not in ["1","2","3"]:
                login_check=[None]
                print("\n\t#### Error : Please enter appropriate values above ####".upper())
            if login_check==0: #login check see if user is logged in since if it is zero the loop will break
                break          #and user will end up in main menu 
            #end of login menu


            #customer menu
            while login_check[0]==1:
                print("\n\t1.Book tickets")
                print("\t2.See tickets")
                print("\t3.Prebooking")
                print("\t4.Food booking")       
                print("\t5.go back to main menu")
                opt3 = int(input("\n\tPlease enter 1, 2, 3, 4, 5: "))
                while opt3 == 1:
                    print("\n\t\t\b\bchoose from the following ships and routes")
                    print("\n\t\t\b\b1.MV Kavaratti ( Kochi --> Kavaratti ))")
                    print("\t\t\b\b2.MV Arabian Sea ( Kochi --> Minicoy )")
                    print("\t\t\b\b3.MV Lakshadweep Sea ( Kochi --> Kalpeni )")
                    print("\t\t\b\b4.MV Amindivi ( Beypore --> Amini )")
                    print("\t\t\b\b5.HSC Parali ( Kochi --> Agatti )")
                    print("\t\t\b\b6.Go back to previous menu")
                    opt4=int(input("\n\t\t\b\bPlease eter 1, 2, 3, 4, 5, 6: "))
                    if opt4==6:
                        see_tickets_for_user(login_check[1])
                    if book_ticket(opt4,login_check[1]) == True:
                          break
                while opt3==2:
                    see_tickets_for_user(login_check[1])
                while opt3==3:
                    print("\n\t\t\b\bChoose from the following ships and routes to prebook from")
                    print("\n\t\t\b\bPre-booking works only for immediatly next trip")
                    print("\n\t\t\b\b1.MV Kavaratti ( Kochi --> Kavaratti )")
                    print("\t\t\b\b2.MV Arabian Sea ( Kochi --> Minicoy )")
                    print("\t\t\b\b3.MV Lakshadweep Sea ( Kochi --> Kalpeni )")
                    print("\t\t\b\b4.MV Amindivi ( Beypore --> Amini )")
                    print("\t\t\b\b5.HSC Parali ( Kochi --> Agatti )")
                    opt8=int(input("\n\t\t\b\bPlease enter 1, 2, 3, 4, 5, 6: "))
                    if opt8==6:
                        break
                    if book_ticket(opt8,login_check[1],booking_type="prebooking") == True:
                        # login_check[1] is user_id
                        break 
                while opt3==4:
                    book_food(login_check[1])
                    break
                if opt3==5:
                    print("\n\t\t\b\bRouting you back to main menu !")
                    break                   
                if opt3 not in [1,2,3,4,5]:
                    print("\n\n\t#### Error : Please enter appropriate values above ####".upper())
                    log("user entered inappropriate option in register menu")
            #end of customer menu 


            #staff menu 
            while login_check[0] in [2,3,4]:
                print("\n\t\t\b\b___staff menu___")
                print("\n\t\t\b\b1.deactivate ticket")
                print("\t\t\b\b2.refund ticket")
                print("\t\t\b\b3.see ship info (current)")
                print("\t\t\b\b4 see ship info (prebooking)")
                print("\t\t\b\b5.see ship history")
                print("\t\t\b\b6.see ticket history")
                print("\t\t\b\b7.adminstarative menu")
                print("\t\t\b\b8.exit staff menu")
                opt5=int(input("\n\t\t\b\bPlease choose from the following options 1, 2, 3, 4, 5, 6, 7, 8 :"))
                if opt5==1:
                    update_ticket()
                if opt5==2:
                    update_ticket(update_type="refund")
                if opt5==3:
                    see_info("ship info-current")
                if opt5==4:
                    see_info("ship info-prebooking")
                if opt5==5:
                    see_info("ship history")
                if opt5==6:
                    see_info("ticket history")
                if login_check[0] in [3,4] and opt5==7:
                    while True:
                        if login_check[0]==4:
                            print("\n\t\t\b\b___owner menu___")
                            print("\n\t\t\b\b1.add staff")
                            print("\t\t\b\b2.remove staff")
                            print("\t\t\b\b3.add admin")
                            print("\t\t\b\b4.remove admin")
                            print("\t\t\b\b5.use database console with owner privilages")
                            print("\t\t\b\b6.exit owner menu")
                            opt6=int(input("\n\t\t\b\bPlease choose from the following options 1, 2, 3, 4, 5, 6 :"))
                            while opt6==1:
                                log("staff entered registeration option further")
                                staff_reg_check=staff_registeration1()
                                if staff_reg_check[0]==1:
                                    break
                                staff_registeration2(staff_reg_check[1],staff_reg_check[2],login_check[0],"staff")
                                break
                            print(login_check)
                            if opt6==2:
                                remove_staff(login_check[0],"staff")
                            while opt6==3:
                                log("staff entered registeration option further")
                                staff_reg_check=staff_registeration1()
                                if staff_reg_check[0]==1:
                                    break
                                staff_registeration2(staff_reg_check[1],staff_reg_check[2],login_check[0],"admin")
                                break
                            if opt6==4:
                                remove_staff(login_check[0],"admin")
                            if opt6==5:
                                pass
                            if opt6==6:
                                break
                        else:
                            print("\n\t\t\b\b___admin menu___")
                            print("\n\t\t\b\b1.add staff")
                            print("\t\t\b\b2.remove staff")
                            print("\t\t\b\b3.use database console with admin privilages")
                            print("\t\t\b\b4.exit admin menu")
                            opt7=int(input("\n\t\t\b\bPlease choose from the following options 1, 2, 3, 4 :"))
                            while opt7==1:
                                log("staff entered registeration option further")
                                staff_reg_check=staff_registeration1()
                                if staff_reg_check[0] == 1:
                                    break
                                staff_registeration2(staff_reg_check[1],staff_reg_check[2],login_check[0],"staff")
                                break
                            if opt7==2:
                                remove_staff(login_check[0],"staff")
                            if opt7==3:
                                pass
                            if opt7==4:
                                break
                if opt5==8:
                    break
                #end of staff menu


        #registeration option 
        while opt == "2":
            log("user choose registeration option")
            print("\n\t1.register")
            print("\t2.go back to main menu")
            opt2 = int(input("\n\tPlease enter 1, 2 : "))
            while opt2 == 1:
                log("user entered registeration option further")
                user_reg_check=user_registeration1()
                if user_reg_check[0] == 1:
                    break
                user_registeration2(user_reg_check[1],user_reg_check[2])
                break
            if opt2 == 2:
                log("user exited registeration menu")
                break
            if opt2 not in [1,2]: 
                print("\n\n\t#### Error : Please enter appropriate values above ####".upper())
                log("user entered inappropriate option in register menu")
        if opt =="3":
            log("user exited program")
            break
        #end of registeration option 


    except ZeroDivisionError:
        print("\n\n\t#### Unkwon error please submit code for through inspection ####".upper())
        log("user entered inappropriate option in register menu")


