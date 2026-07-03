import mysql.connector as s
con1=s.connect(host="localhost",user="theblackfox",password="theblackarch90",database="shipproject")
if con1.is_connected()==True:
    print("con0 connected !!!")
    cur1=con1.cursor()
    user_id=input("please enter the user_id : ")
    cur1.execute("select password from login_checklist where user_id = '%s'"%user_id)
    c=cur1.fetchall()
    for i in user_id:
        if i not in ("1234567890"):
            print("### Enter proper user id ###")
            c=[("none",)]
            break
hello=c[0][0]
print("out of range")

