# -------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------PROGRAM FOR HOTEL MANAGEMENT-----------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import mysql.connector
from tkinter import*
from tkinter import scrolledtext
from tkinter import messagebox as tmsg
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import Menu
from PIL import Image,ImageTk
import os


con=mysql.connector.connect(host="localhost", user="root", passwd="root", database="hotel")
if con.is_connected==False:
    print('error in connecting MySql')

def tbooking():
    cur = con.cursor()
    cur.execute("select * from customer")
    data = cur.fetchall()

    query1 = "insert into customer(customer_id,name,address,city,mob,cheackin,roomno) values ('{}','{}','{}','{}','{}','{}','{}')".format(
        tcst_id, nameval.get(),addressval.get(), cityval.get(), mobval.get(), indateval.get(), roomnoval.get())
    cur.execute(query1)
    query2 = "update room set status='on' where room_no={}".format(roomnoval.get())
    cur.execute(query2)
    con.commit()
    tmsg.showinfo("Success","Room Booked Successfully")

def gcid():
    cur = con.cursor()
    cur.execute("select * from customer")
    tdata = cur.fetchall()
    sd = tdata[-1]
    sd = sd[0]
    global tcst_id
    tcst_id = sd + 1
    #print("customer Id :", tcst_id)
    Label(f1,text=tcst_id,fg="black",bg='#abb6ff',font=('arial',15)).place(x=250,y=40)
    con.commit()

def roomref():
    cur = con.cursor()
    cur.execute("select room_no from room where type='simple' and status='off'")
    simroom=cur.fetchall()
    cur.execute("select room_no from room where type='delux' and status='off'")
    dexroom = cur.fetchall()
    cur.execute("select room_no from room where type='5star' and status='off'")
    starroom = cur.fetchall()

    Label(f1, text=simroom, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=200, y=460)
    Label(f1, text=dexroom, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=200, y=490)
    Label(f1, text=starroom, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=200, y=520)
    con.commit()

def generatebill():

    cur=con.cursor()
    cur.execute("select name from customer where customer_id='{}'".format(p_cuid.get()))
    b_name = cur.fetchall()
    cur.execute("select mob from customer where customer_id='{}'".format(p_cuid.get()))
    b_mobno = cur.fetchall()
    cur.execute("select roomno from customer where customer_id='{}'".format(p_cuid.get()))
    b_roomno = cur.fetchall()
    cur.execute("select cheackin from customer where customer_id='{}'".format(p_cuid.get()))
    b_cheackin = cur.fetchall()
    o=p_odate.get()
    i=str(b_cheackin)
    #print("check in date",i)
    #print("check out date", o)
    id = int(i[3:5])
    im = int(i[6:8])
    iy = int(i[9:13])
    od=int(o[0:2])
    om=int(o[3:5])
    oy=int(o[6:10])
    if ( id<od and im<=om and iy<=oy):

        cur.execute("update customer set cheackout='{}' where customer_id='{}'".format(p_odate.get(),p_cuid.get()))

        cur.execute("select roomno from customer where customer_id={}".format(p_cuid.get()))
        troomno = cur.fetchall()
        troomno = str(troomno)
        #print(troomno)
        scirno = troomno[2:5]
        #print(scirno)
        aa = int(scirno)
        cur.execute("select rent from room where room_no={}".format(aa))
        rent = cur.fetchall()
        #print(rent)
        rent = str(rent)
        rent = rent[2:6]
        #print(rent)
        rent = int(rent)
        #print(rent)
        d,m,y=od-id,om-im,oy-iy
        global bi
        bi = (d * rent)#+(m*30*rent)

        cur.execute("update room set status='off' where room_no={}".format(aa))
        cur.execute( "update customer set bill={} where customer_id={}".format(bi,p_cuid.get()))

        Label(f1, text=b_name, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=150)
        Label(f1, text=b_mobno, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=180)
        Label(f1, text=b_roomno, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=210)
        Label(f1, text=b_cheackin, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=240)
        Label(f1, text=p_odate.get(), fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=270)
        Label(f1, text=bi, fg="black", bg='#abb6ff', font=('arial', 15)).place(x=1100, y=300)
    else:
        tmsg.showerror("DATE INVALID","CHECK OUT DATE IS INVALID")

    con.commit()


def printbill():
    bill1=open("E:\se_bills\mybill.txt",'a')

    cur = con.cursor()
    cur.execute("select name from customer where customer_id='{}'".format(p_cuid.get()))
    b_name = cur.fetchall()
    cur.execute("select mob from customer where customer_id='{}'".format(p_cuid.get()))
    b_mobno = cur.fetchall()
    cur.execute("select roomno from customer where customer_id='{}'".format(p_cuid.get()))
    b_roomno = cur.fetchall()
    cur.execute("select cheackin from customer where customer_id='{}'".format(p_cuid.get()))
    b_cheackin = cur.fetchall()
    List1=["\t\t\tHOTEL CASTEL\n","NAME:\t",b_name,"\nMOBILE NO:\t",b_mobno,"\nROOM NO:\t",b_roomno,"\nCHECK IN DATE\t",
    b_cheackin,"\nCHECK OUT DATE:\t",p_odate.get(),"\nAMOUNT:\t",bi,"\n\t!!!!! THANKS YOU !!! VISIT AGAIN !!!!!!"]
    for i in List1:
        i=str(i)
        bill1.write(i)
    bill1.close()
    os.startfile('E:\se_bills\mybill.txt','print')
    os.remove("E:\se_bills\mybill.txt")
root=Tk()

root.title("Welcome to The Castle")

root.geometry('1530x775')
root.resizable(False,False)

head=Label(text='THE CASTLE',bg='blue',fg='white',font=('arial', 20))
head.pack(fill=X)


nameval=StringVar()
addressval=StringVar()
cityval=StringVar()
mobval=IntVar()
indateval=StringVar()
roomnoval=IntVar()

def booking():
    # INTEFACE CODING FOR BOOKING BUTTON WINDOW ==================================================
    global f1
    f1 = Frame(root, bg="#abb6ff", highlightbackground="blue", highlightthickness=4)
    f1.place(x=158, y=40, width=1370, height=733)

    Label(f1, text='ROOM BOOKING', fg='white', bg='#0746d9', font=('arial', 15, 'bold')).place(x=10, y=5, width=550, height=25)

    cid_btn=Button(f1,text="GENERATE CUSTOMER ID",fg="black",bg='#c7c7c7',command=gcid)
    cid_btn.place(x=5,y=40,width=150,height=35)

    Label(f1,text='NAME',fg="black",bg='#abb6ff',font=('arial',15)).place(x=5,y=90)
    Label(f1, text='ADDRESS', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=120)
    Label(f1, text='CITY', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=150)
    Label(f1, text='MOBILE NO', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=180)
    Label(f1, text='CHECK IN DATE', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=210)
    Label(f1, text='ROOM NO', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=240)


    Entry(f1,textvariable=nameval,font=("arial",15),).place(x=250,y=90)
    Entry(f1, textvariable=addressval, font=("arial", 15), ).place(x=250, y=120)
    Entry(f1, textvariable=cityval, font=("arial", 15), ).place(x=250, y=150)
    Entry(f1, textvariable=mobval, font=("arial", 15), ).place(x=250, y=180)
    Entry(f1, textvariable=indateval, font=("arial", 15), ).place(x=250, y=210)
    Entry(f1, textvariable=roomnoval, font=("arial", 15), ).place(x=250, y=240)

    book_btn = Button(f1, text="CONFORM BOOKING", fg="WHITE", bg='#03960a',font=('arial', 10), command=tbooking)
    book_btn.place(x=100, y=300, width=140, height=30)

    clear_btn = Button(f1, text="CLEAR", fg="WHITE", bg='#ff0000', font=('arial', 10), command=booking)                    #NOT FUNCTIONING
    clear_btn.place(x=300, y=300, width=140, height=30)

   #  SEARCH OF A EMPTY ROOM IN HOTEL ----------------------------------------------------------------------------

    Label(f1, text='EMPTY ROOMS', fg='white', bg='#0746d9', font=('arial', 15, 'bold')).place(x=5,y=390, width=550,height=25)

    ref_btn = Button(f1, text="REFRESH", fg="white", bg='#03960a', command=roomref)
    ref_btn.place(x=435, y=430, width=120, height=30)

    Label(f1, text='SIMPLE', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=460)
    Label(f1, text='DELUX', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=490)
    Label(f1, text='5 STAR', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=5, y=520)

   #BILLING  INTERFACE START HERE      ----------------------------------------------------

    Label(f1,text='GENERATE BILL',fg='white',bg='#0746d9',font=('arial',15,'bold')).place(x=700,y=5,width=550,height=25)

    generate_btn = Button(f1, text="GENERATE BILL", fg="white", bg='#03960a', command=generatebill)
    generate_btn.place(x=700, y=40, width=120, height=30)


    prt_btn = Button(f1, text="PRINT", fg="white", bg='#03960a', command=printbill)
    prt_btn.place(x=1130, y=350, width=120, height=30)

    clear_b_btn = Button(f1, text="CLEAR", fg="WHITE", bg='#ff0000', font=('arial', 10),command=printbill)                        # NOT FUNCTIONING
    clear_b_btn.place(x=1130, y=40, width=120, height=30)

    Label(f1, text='CUSTOMER ID', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=90)
    Label(f1, text='CHECK OUT DATE', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=120)

    global p_cuid
    p_cuid = IntVar()
    global p_odate
    p_odate = StringVar()

    Entry(f1, textvariable=p_cuid, font=("arial", 15), ).place(x=1000, y=90)
    Entry(f1, textvariable=p_odate, font=("arial", 15), ).place(x=1000, y=120)

    Label(f1, text='NAME', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=150)
    Label(f1, text='MOBILE NO', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=180)
    Label(f1, text='ROOM NO', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=210)
    Label(f1, text='CHECK IN DATE', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=240)
    Label(f1, text='CHECK OUT DATE', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=270)
    Label(f1, text='AMOUNT', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=300)



    # SEARECH CUSTOMESR BY NAME OR CUSTOMER ID
    Label(f1, text='SEARCH CUSTOMER', fg='white', bg='#0746d9', font=('arial', 15, 'bold')).place(x=700, y=390, width=550,height=25)

    ser_btn1 = Button(f1, text="SEARCH", fg="white", bg='#03960a', command=gcid)                                                       # need to change command
    ser_btn1.place(x=1130, y=460, width=120, height=30)

    ser_btn2 = Button(f1, text="SEARCH", fg="white", bg='#03960a', command=gcid)                                                       # need to change command
    ser_btn2.place(x=1130, y=530, width=120, height=30)

    Label(f1, text='SEARCH BY NAME', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=430)
    Label(f1, text='SEARCH BY CUSTOMER ID', fg="black", bg='#abb6ff', font=('arial', 15)).place(x=700, y=500)

    s_cuid=IntVar()
    s_name=StringVar()

    Entry(f1, textvariable=s_name, font=("arial", 15), ).place(x=1000, y=430)
    Entry(f1, textvariable=s_cuid, font=("arial", 15), ).place(x=1000, y=500)

    Label(f1, text='SEARCH RESULT', fg='white', bg='#0746d9', font=('arial', 15, 'bold')).place(x=5, y=570, width=1345,height=25)


def restaurant():
    # INTEFACE CODING FOR RESTAURANT BUTTON WINDOW ==================================================

    f2 = Frame(root, bg="#6ef589", highlightbackground="blue", highlightthickness=4)
    f2.place(x=158, y=40, width=1370, height=733)


def staff():
    # INTEFACE CODING FOR STAFF BUTTON WINDOW ==================================================

    f2 = Frame(root, bg="#ffabab", highlightbackground="blue", highlightthickness=4)
    f2.place(x=158, y=40, width=1370, height=733)


def admin():
    # INTEFACE CODING FOR RESTAURANT ADMIN WINDOW ==================================================

    f2 = Frame(root, bg="#d26df7", highlightbackground="blue", highlightthickness=4)
    f2.place(x=158, y=40, width=1370, height=733)


# Side buttons are build here===============================================================

b1=Button(root,text="BOOKING",fg="white",bg="#4760ed",font=("rockwell",16,"bold"),command=booking)
b1.place(x=3,y=40,width=150,height=70)
b1=Button(root,text="RESTAURANT",fg="white",bg="#6ef589",font=("rockwell",16,"bold"),command=restaurant)
b1.place(x=3,y=113,width=150,height=70)
b1=Button(root,text="STAFF",fg="white",bg="#ffabab",font=("rockwell",16,"bold"),command=staff)
b1.place(x=3,y=186,width=150,height=70)
b1=Button(root,text="ADMIN",fg="white",bg="#d26df7",font=("rockwell",16,"bold"),command=admin)
b1.place(x=3,y=259,width=150,height=70)


root.mainloop()