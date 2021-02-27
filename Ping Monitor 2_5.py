import tkinter as tk
from tkinter import *
import tkinter.messagebox as tm
import time
import subprocess
import datetime as dt
import os
import smtplib
import hashlib, binascii
import re
import socket
from datetime import date
from tkinter.ttk import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 
import numpy as np

global Btn_run_flag
global Timer_Interval
Timer_Interval=60
Cell_Rows = 21
Btn_run_flag=True


window = tk.Tk()

window.title('Ping Monitor by Tim Watkins Feb 2021')
window.geometry("1200x660+5+5")

root = tk.Frame(window,width=480,highlightbackground="green", highlightcolor="green", highlightthickness=2,padx=2,pady=2)

frameTracking = tk.Frame(window,bg="darkblue")

txtCountdown = tk.StringVar()

date_now = dt.datetime.now()

global Time_Last_Live
global password
global Selected_Address

Selected_Address = StringVar()
Selected_Address.set("8.8.8.8")

password = StringVar() #Password variable

# Send Email

def Send_Email(Message):
   Save_Log("PingMonitor","Sending Email")
   sender = 'timwatkins20@gmail.com'
   receivers = ['receiver@hotmail.com']

   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, Message)         
      print ("Successfully sent email")
   except SMTPException:
      print ("Error: unable to send email")
      
# End Send Mail

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def Stats(Address):
   global Selected_Address
   global lblFail,lblPass
   
   cwin = Toplevel()
   
   cwin.title =("Ping Monitor File Stats")
   lblTitle   = tk.Label(cwin,text="Statistical Ping Time Search",width=45,padx=5)
   P_Date = time.strftime("%d_%m_%Y")
   lblDate   = tk.Label(cwin,text="Date",width=40,padx=5).pack()
   Entry_Date = tk.Entry(cwin)
   Entry_Date.pack()
   Entry_Date.delete(0,END)
   Entry_Date.insert(0,P_Date)

   lblAddress   = tk.Label(cwin,text="Address",width=40,padx=5).pack()
   Entry_Address = tk.Entry(cwin)
   Entry_Address.pack()
   Entry_Address.delete(0,END)
   Entry_Address.insert(0,Selected_Address.get())
   
   lblPass   = tk.Label(cwin,text="Pass =  ",width=40,padx=5)
   lblFail   = tk.Label(cwin,text="Fail =  ",width=40,padx=5)
   lblAvgTime   = tk.Label(cwin,text="Avg Time",width=40,padx=5)
   lblHiLo  = tk.Label(cwin,text="Hi & Lo Times",width=40,padx=5)
   #fig = Figure(figsize = (6, 4), dpi = 100) 
   #canvas = FigureCanvasTkAgg(fig,master = cwin)   
   #canvas.draw()
   #canvas.get_tk_widget().pack()
   
   

   def Find_Address():

      global lblFail,lblPass
      
      Address  = Entry_Address.get()
      Lines    = []
      LineList = []
      LstTimes = []
      
      Pcount = 0
      Fcount = 0
      Tcount = 0
      TTime  = 0
      pcFail = ""
      pcPass = ""

      

      #TD = str(date.strftime("%d_%m_%y"))
      TD = Entry_Date.get()
      with open("PingMonitor"+TD+".log") as file:
           for line in file:
                   Lines = (line.strip())
                   LineList= Lines.split(",")
                   
                   StringAddress= str(Address).lower()
                   First =  (str(LineList[0])).lower()
                   
                   if First == StringAddress:

                        StrFirst = LineList[1].strip()
                        StrFirst4 = StrFirst[0:4]

                        if StrFirst4 == "Pass" :
                                Pcount += 1
                                Reply_Time = LineList[2].strip()
                                TimeFirst4 = Reply_Time[0:4]
                                if Pcount == 1:
                                      minTime = TTime
                                      maxTime = TTime

                                if TimeFirst4 == "time" :
                                   Tcount += 1
                                   Reply_Time_Time = Reply_Time[5:8]
                                   
                                   TTime += int(str(Reply_Time_Time))
                                   
                                   LstTimes.append(int(str(Reply_Time_Time)))
                                      
                               
                        if StrFirst4 == "Fail":
                                Fcount += 1
                                                                   
           if Pcount !=0:
              pcFail = str(round((Fcount/(Fcount+Pcount))*100))
              
           if Fcount !=0:
              pcPass = str(round((Pcount/(Pcount+Fcount))*100))
              
           
           if Tcount !=0:
              MaxTime = max(LstTimes)
              MinTime = min(LstTimes)
              lblAvgTime.config(text = "AvgTime = " + str(round(TTime/Tcount))+"ms")
              lblHiLo.config   (text = "Max = " + str(MaxTime)+"ms :Min = " + str(MinTime)+"ms")

           lblFail.config(text = "Fail = "+ str(Fcount)+" %"+pcFail)
           lblPass.config(text = "Pass = "+ str(Pcount)+" %"+pcPass)
           
           fig = plt.figure(figsize = (6, 4), dpi = 90)
           plt.subplot(111).plot(LstTimes)
           
           plt.xlabel("Number of Pings")
           plt.ylabel("Time in ms")
           plt.title('Ping Times Graph')
           #plt.boxplot(LstTimes)
           canvas = FigureCanvasTkAgg(fig,master = cwin)   
           canvas.draw()
           canvas.get_tk_widget().pack()
           toolbar = NavigationToolbar2Tk(canvas,cwin) 
           toolbar.update() 
           

   label1 = tk.Label(cwin,text="Date dd_mm_yyy & Address").pack()
   
   
   
   lblPass.pack()
   lblFail.pack()
   lblAvgTime.pack()
   lblHiLo.pack()

   btnOk = tk.Button(cwin,text=" OK ",pady=10,width=5,command=lambda:Find_Address()).pack()
   
   cwin.mainloop()
   

def Help_WINDOW():
   Save_Log("PingMonitor ","Help Window Opened")
   helpwin = Toplevel(root)
   helpwin.geometry("550x300")
   Help_Text=Text(helpwin)
   Help_Text.insert(INSERT,"Enter IP Address, Device DNS name or Internet Web Link.\nPress Scan Now to send instant test Ping request.\n")
   Help_Text.insert(INSERT,"Press START Button to start automatic ping Timer \nThe default rate of 120 seconds.\n")
   Help_Text.insert(INSERT,"Save Button to save Sheet Names and IP Addresses to AddressList.log\n")
   Help_Text.insert(INSERT,"Load Button to Load Address list from .Log file.\n")
   Help_Text.insert(INSERT,"Clear Button to remove all Sheet addresses.\n")
   Help_Text.insert(INSERT,"Countdown Timer in Minutes and Seconds.\n")
   Help_Text.insert(INSERT,"Countdown Timer interval can be altered from the File Menu bar.\n")
   Help_Text.insert(INSERT,"Right mouse click on Cell Address, highlight in yellow, this will auto fill Stats IP/Domain Name Entry.\n")
   
   Help_Text.pack()

   hbutton = Button(helpwin, text="Real Men! don't need a manual")
   hbutton.pack()
  

def Display_About():
   Save_Log("Display About ",":")
   filewin = Toplevel(root)
   filewin.geometry("250x100")
   button = Button(filewin, text="Ping Monitor \n by Tim Watkins Feb 2021")
   button.pack()
   

def Do_End():
    Answer = tm.askquestion("Are You Sure", "Do you wish to close Ping Monitor")
    Save_Log("PingMonitor ","Closed")
    if Answer == "yes" :
       if Btn_run_flag == False:
          StartStop_Button()
          window.update()
          time.sleep(2)
       window.quit()
       window.destroy()



def Ask_For_Password():
   
   global password
   Info_win = Toplevel(window)
   Info_win.title('Ping Monitor by Tim Watkins Feb 2021')
   Info_win.geometry("300x200+5+5")

   def ReturnEntry():
      password =str(entInfo.get())
      Info_win.destroy()

   lblInfo = tk.Label(Info_win,text="Please Enter Email Password\n ").pack()

   entInfo = tk.Entry(Info_win,width = 15)
   entInfo.config(textvariable=password, show='*')
   entInfo.pack()

   btnInfo = tk.Button(Info_win,width = 15,text="OK",command=lambda:ReturnEntry())
   
   btnInfo.pack()

   Info_win.mainloop()
   
   

   

def Change_Interval():
   global Timer_Interval
   child_window = Toplevel() # Child window 
   child_window.geometry("400x100")  # Size of the window 
   child_window.title("Ping Timer Period")
   Plot_Label = tk.Label(child_window, text="Enter period between Pings in Seconds").grid(column=0, row=0)
   PEntry = tk.Entry(child_window)
   PEntry.grid(column=0, row=1)
   PEntry.insert(INSERT,str(Timer_Interval))

   def Set_and_Exit():
      global Timer_Interval
      Timer_Interval = int(PEntry.get())
      obj = dict[cell]
      obj.delete(0, 'end')
      obj.insert(0,str(Timer_Interval))
      txtCountdown.set(str(Timer_Interval)+" Secs")
      child_window.destroy()
      
   btn =tk.Button(child_window,text="OK",command=Set_and_Exit)
   btn.grid(column=0, row=2)
   
      

         


menubar = Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label = "Stats", command = lambda: Stats(Selected_Address))
filemenu.add_command(label = "Clear", command = lambda: Clear_Cells())
filemenu.add_command(label = "SAVE",  command = lambda: Save_Active_Cells())
filemenu.add_command(label = "LOAD",  command = lambda: Load_Cells())
filemenu.add_command(label = "Change Interval", command=Change_Interval)
filemenu.add_command(label = "START", command = lambda: StartStop_Button())
filemenu.add_command(label = "Exit",  command = Do_End)
filemenu.add_separator()

menubar.add_cascade(label = "File", menu = filemenu)
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_separator()
menubar.add_cascade(label = "Edit", menu = editmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command (label = "Help Index", command=Help_WINDOW)
helpmenu.add_command (label = "About...", command=Display_About)
menubar.add_cascade  (label = "Help", menu = helpmenu)
editmenu = tk.Menu(menubar, tearoff=0)
window.config(menu = menubar)

# Naughty List Creation

lblTracking = Label(frameTracking,text="Naughty List")
lblTracking.grid(column=0,row=3,pady=4)
listTracking = Listbox(frameTracking,height=26,width=50,bg="lightblue")
listTracking.grid(column=0,row=4,padx=10)
listTracking.config()

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify="left",
                      background="#ffffe0", relief="solid", borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()






def click(event, cell):
    # can do different things with right (3) and left (1) mouse button clicks
    #window.title("you clicked mouse button %d in cell %s" % (event.num, cell))
    # test right mouse button for equation solving
    # eg. data = '=9-3' would give 6

    if event.num == 3:
        # entry object in use
        obj = dict[cell]
        
        # get data in obj
        data = obj.get()
        Selected_Address.set(data)
        obj.config(bg="yellow", fg ="black")
        
        # if it starts with '=' it's an equation
        if data.startswith('='):
            eq = data.lstrip('=')
            #print (data, eq)
            try:
                # solve the equation
                result = eval(eq)
                #print result, type(result)  # test
                # remove equation data
                obj.delete(0, 'end')
                # update cell with equation result
                obj.insert(0, str(result))
            except:
                
                pass

def key_r(event, cell):
    # return/enter has been pressed
    
    data = dict[cell].get()  # get text/data in given cell
    #print cell, dict[cell], data  # test
    addr1=""

    try:
       addr1 = socket.gethostbyname(data)
    except:
       tm.showwarning("Error","Cannot find DNS of:"+data)
       
    window.title("Domain %s has an IP: %s" % (data, addr1))

# create a dictionary of key:value pairs
dict = {}
w = 20
h = 1
alpha = ["", 'A', 'B', 'C', 'D', 'E', 'F','G','H','I','J']
for row in range(Cell_Rows):
    for col in range(6):
        if col == 0:
            # create row labels
            label1 = tk.Label(root, width=5, text=str(row))
            label1.grid(row=row, column=col, padx = 2, pady=2)
        elif row == 0:
            # create column labels
            label1 = tk.Label(root, width=w, text=alpha[col])
            label1.grid(row=row, column=col, padx = 2, pady=2)            
        else:
            # create entry object
            entry1 = tk.Entry(root, width=w)
            # place the object
            entry1.grid(row=row, column=col, padx = 2, pady=2)
            # create a dictionary of cell:object pair
            cell = "%s%s" % (alpha[col], row)
            dict[cell] = entry1
            # bind the object to a left mouse click
            entry1.bind('<Button-1>', lambda e, cell=cell: click(e, cell))
            # bind the object to a right mouse click
            entry1.bind('<Button-3>', lambda e, cell=cell: click(e, cell))
            # bind the object to a return/enter press
            entry1.bind('<Return>', lambda e, cell=cell: key_r(e, cell))


#print dict  # test

# set the focus on cell A1
dict['A1'].focus()

def btnTest_pressed():
    obj = dict['A5']
    obj.insert(0, "TEST")
    obj.config(bg="blue")

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def btnScan_pressed():
    
    for row in range(Cell_Rows):
        for col in range(5):
            if col !=0 and row!=0:
                cell = str(alpha[col]+str(row))
                obj = dict[cell]
                # get data in obj
                data = obj.get()
                obj.config(bg="grey92",fg="black")
                window.update()
                if data != "":
                    Response=check_ping(data)
                        

                    if Response == "Active":
                        obj.config(bg="lightgreen", fg ="black")
                        CreateToolTip(obj,time.strftime("%d\%m\%y %H:%M:%S"))
                        window.update()
                        #Save_Log(data,"Pass")
                    else:
                        
                        IsIt,Fail_Times,ListItem = IsInNaughtyList(data)
                        
                        toc = time.strftime("%d\%m\%y %H:%M:%S")
                        if  IsIt == False:
                           listTracking.insert(END,data+" : "+str(toc+",Fail= 1 #"))

                        else:
                           listTracking.delete(ListItem)
                           listTracking.insert(END,data+" : "+str(toc+",Fail= "+str(Fail_Times+1)+" #"))
                           
                        obj.config(bg="red", fg ="white")
                        
                        
                        Save_Log(data,"\tFail ,\ttime=999, \t TTL=999,\t "+toc)
                        
                        
                        
def IsInNaughtyList(hostname):

   for i in range(listTracking.size()):
      Item = listTracking.get(i)
      
      found = Item.find(hostname)
      Fail_Index = Item.find("Fail=")
      Hash_Index = Item.find("#")
      Failed = int(Item[(Fail_Index+5):(Hash_Index)])
      if found == 0:
         return (True,Failed,i)
         break
         
      
   return (False,0,0)

      
         
   
                        

def check_ping(hostname):
    DETACHED_PROCESS = 0x00000008
    CREATE_NO_WINDOW = 0x08000000
    sub_index = 1
    pingstatus="Ok Before Ping Call"
    try:
        
        
        response=subprocess.Popen(["ping", "-n", "1", hostname.strip('\ r')],creationflags=CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        stdout, stderr = response.communicate()
        Res_String = str(stdout)
        DidFind = Res_String.find("Reply from")
        #print(DidFind)
        if DidFind != -1 :
            pingstatus = "Active"
            sub_index = Res_String.find('time')
            Res_Time = str( Res_String[(sub_index):(sub_index + 9)]).strip("m s")
            sub_index = Res_String.find('TTL=')
            Res_TTL = str( Res_String[(sub_index):(sub_index + 8)]).strip("\ r")
            
            if Res_TTL == "":
               Res_TTL = "TTL=000"
               
            if Res_Time == "":
               Res_Time ="time=00"
            x = re.findall('[0-9]+', Res_Time.strip())
            Lenx = len(str(x))-4
            Res_Time_Str = "".join(x)
           
            if (Lenx <=3):
               Res_Time = "{:03d}".format(int(Res_Time_Str))
              
               
               
            Save_Log(hostname,"Pass ,\ttime="+ Res_Time+",\t "+Res_TTL )
        else:
            pingstatus = "Cound not find:"
            
                           
        
        
        #print(stdout)
        #print(stderr)
        
        return pingstatus
    except:
        tm.askquestion("Ping Error", "Do you want to Continue")
        

"""
def PingAddress():
    hostname = entAddress.get()
    Response = check_ping(hostname)
    lblIPaddress.config(text=Response)
"""
def Save_Active_Cells():
    Answer = tm.askquestion("Are You Sure", "This action will delete any previously saved Address List")
    if Answer == "No":
       return
    temp=password.get()
    password.set(hash_password(password.get()))
    cell="E10"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.insert(0,str(Timer_Interval))
    Save_Log("PingMonitor ","\tCells Saved,\t")
    
    file = open("AddressList.log",'w')
    root.update()
   
    for row in range(Cell_Rows):
        for col in range(6):
            if col !=0 and row!=0:
                cell = str(alpha[col]+str(row))
                obj = dict[cell]
                # get data in obj

                data = obj.get()
                
                # print(data)
                if data != "":
                    file.write(cell+","+str(data)+"\n")
                    # print(cell+","+str(data)+"\n")
    root.update()
    password.set(temp)
    file.close()

def Load_Cells():
    global Timer_Interval
    global Btn_run_flag
    Save_Log("PingMonitor,\t ","Cells Loaded,\t ")
    L=[]
    try:
        file = open("AddressList.log")
        line = file.readline() 
        #print(line)
        while line !='':
            L += [line.strip().split(",")]
            line = file.readline()

        #del L[-1]
        #print(L)
        

        for cell, Address in L:
            #print("Cell="+cell+" Address="+Address)
            obj = dict[cell]
            obj.delete(0, 'end')
            obj.insert(0,Address)
            if cell =="E10":
               try:
                  Timer_Interval = int(re.sub("[^0-9]", "",Address))
                  txtCountdown.set(str(Timer_Interval)+" Secs")
               except:
                  tm.messagebox.showwarning("Timer Interval","Incorrect Value")
                  
        cell="E2"
        obj = dict[cell]
        data = obj.get()
        if Btn_run_flag==False:
           Btn_run_flag =True
           btnStartStop_Timer['text']="START"

        password.set("")
        if data != "":
           Ask_For_Password()
           
           
    except:
        print("Error Loading Data")

def Clear_Cells():

    Answer = tm.askquestion("Are You Sure", "This will Clear all cells and Naughty List")
    
    if Answer == "no" :
       return
   
    global Btn_run_flag
    Save_Log("PingMonitor Cells Cleared ","Timer Stopped ")
    listTracking.delete(0,END)
    if Btn_run_flag==False:
       
       Btn_run_flag =True
       btnStartStop_Timer['text']="START"

    for row in range(Cell_Rows):
        for col in range(6):
            if col !=0 and row!=0:
                cell = str(alpha[col]+str(row))
                obj = dict[cell]
                obj.config(bg="white", fg ="black")
                obj.delete(0, 'end')
    cell="E1"
    obj = dict[cell]
    obj.config(bg="khaki")
    obj.delete(0, 'end')
    obj.insert(0,'Email')
    cell="E3"
    obj = dict[cell]
    obj.config(bg="khaki")
    obj.delete(0, 'end')
    obj.insert(0,'SMTP')
    cell="E5"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.insert(0,'Password')
    obj.config(bg="khaki")
    cell="E6"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.config(textvariable=password, show='*')
    cell="E7"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.insert(0,'Email Trigger')
    obj.config(bg="khaki")
    cell="E9"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.insert(0,'Timer')
    obj.config(bg="khaki")
    cell="E10"
    obj = dict[cell]
    obj.delete(0, 'end')
    obj.insert(0,str(Timer_Interval))
    obj.config(bg="white")

def Save_Log(Oname,PassOrFail):
    TD = str(date_now.strftime("%d_%m_%Y"))
    file = open("PingMonitor"+TD+".log","a")
    PingOutput = Oname+",\t\t"+PassOrFail+",\t"+ str(date_now.strftime("%d\%m\%y  %H:%M"))

    file.write('%s\n' % PingOutput)
    file.close()
                
Ctl_Row = Cell_Rows+1
    
btnTest =   tk.Button   (frameTracking,width=8,text ="Scan Now",padx=2, command=lambda:btnScan_pressed()).grid(column=0,row=Ctl_Row)
lblStats =  tk.Button   (root,text="Stats",width=10, padx = 2, pady=2,command=lambda:Stats(Selected_Address.get()))
lblStats.config(relief="raised")
lblStats.grid(column=1,row=Ctl_Row)
global lblCountdown
txtCountdown.set(str(Timer_Interval)+" Secs")
lblCountdown = tk.Label(root,font=("Courier",10),textvariable=txtCountdown,bd=2)
lblCountdown.config(width=15,relief="raised",bd=2,height=1)
lblCountdown.grid(column=2,row=Ctl_Row, padx = 2, pady=2)


def StartStop_Button():
    global Btn_run_flag

    if Btn_run_flag == True:
        Btn_run_flag=False
        btnStartStop_Timer['text']="STOP"
        Run_Timer(Timer_Interval)
        Save_Log("PingMonitor ","Timer Started")
    else:
        Btn_run_flag =True
        btnStartStop_Timer['text']="START"
        Save_Log("PingMonitor ","Timer Stopped")


def Run_Timer(seconds):
   
    progress['maximum'] = seconds
    global Btn_run_flag
    btnScan_pressed()
    
   
    for remaining in range(seconds, 0, -1):
        minutes = 0
        seconds = remaining
        if remaining > 60:
            minutes = int(seconds/60)
            seconds = int(seconds%60)
        else:
            seconds = remaining
            
        
        progress['value'] = remaining
        root.update_idletasks()
        countdown = "{:2d} Mins {:2d} Secs".format(minutes,seconds)
        txtCountdown.set(countdown)
        window.update()
        time.sleep(.2)
        window.update()
        time.sleep(.2)
        window.update()
        time.sleep(.2)
        window.update()
        time.sleep(.2)
        window.update()
        time.sleep(.2)
        

        
        if Btn_run_flag == True:
           return
        
    if Btn_run_flag == False:
        Run_Timer(Timer_Interval)
        Save_Log("PingMonitor ","Timer Running")

Logo=PhotoImage(file='PingMonitor_Logo_m.png')
Label(frameTracking,image=Logo).grid(row =0, column=0)
    
Date_label = tk.Label(frameTracking, font=("Courier",10, 'bold'),bg="grey90",fg="black", pady=4,bd =4)      
Date_label.config(width=12,relief="raised")
Date_label.grid(row =1, column=0)

Clock_label = tk.Label(frameTracking, font=("Courier",10, 'bold'),bg="grey90",fg="black", pady=4,bd =4)
Clock_label.config(width=12,relief="raised")
Clock_label.grid(row =2, column=0)

btnStartStop_Timer =tk.Button(root,width =10,text='START',command = lambda: StartStop_Button())

btnStartStop_Timer.grid(column=3,row=Ctl_Row)

btnClear_Cells =  tk.Button(root,width =10,text="Clear", command=Clear_Cells).grid(padx=4,column=0,row=Ctl_Row)
btnSave_Cells  =  tk.Button(root,width =10,text="Save",  command=Save_Active_Cells).grid(column=4,row=Ctl_Row)
btnLoad_Cells  =  tk.Button(root,width =10,text="Load",  command=Load_Cells).grid(column=5,row=Ctl_Row)

s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

progress = Progressbar(root, style="red.Horizontal.TProgressbar", orient = HORIZONTAL, length = 120, mode = 'determinate', maximum=100, value=1)
progress.grid(column=2,row=Ctl_Row+1)
root.update()



def DigitalClock():
   text_input = time.strftime("%H:%M:%S")
   Clock_label.config(text=text_input)
   Clock_label.after(300, DigitalClock)
   hour =0;minute=0;seconds = 1
   if hour == int(dt.datetime.today().strftime("%H")) and minute == int(dt.datetime.today().strftime("%M")) and seconds == int(dt.datetime.today().strftime("%S")):
        Date_label.config(text=time.strftime("%d-%m-%y"))
cell="E1"
obj = dict[cell]
obj.config(bg="khaki")
obj.delete(0, 'end')
obj.insert(0,'Email')
cell="E3"
obj = dict[cell]
obj.config(bg="khaki")
obj.delete(0, 'end')
obj.insert(0,'SMTP')

cell="E5"
obj = dict[cell]
obj.delete(0, 'end')
obj.insert(0,'Password')
obj.config(bg="khaki")
cell="E6"
obj = dict[cell]
obj.delete(0, 'end')
obj.config(textvariable=password, show='*')
cell="E7"
obj = dict[cell]
obj.delete(0, 'end')
obj.insert(0,'Email Trigger')
obj.config(bg="khaki")
cell="E9"
obj = dict[cell]
obj.delete(0, 'end')
obj.insert(0,'Timer')
obj.config(bg="khaki")
cell="E10"
obj = dict[cell]
obj.delete(0, 'end')
obj.insert(0,str(Timer_Interval))
obj.config(bg="white")



Date_label.config(text=time.strftime("%d-%m-%y"))
DigitalClock()
root.pack(side=LEFT,padx=8)
frameTracking.pack(side=RIGHT,padx=10)

Save_Log("PingMonitor ","Program Started ")

window.protocol("WM_DELETE_WINDOW", Do_End)

window.mainloop()
