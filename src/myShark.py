from tkinter import *
import subprocess as sub
import os
import PySimpleGUI as sg
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import netifaces
from tkinter import *
from scapy.all import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys
import random, time

class Window(QWidget):
    def __init__(self,table):
        super().__init__()

        self.title = "Packets Data"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        self.data=table


        self.InitWindow()


    def InitWindow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.creatingTables()


        self.show()

    def creatingTables(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.data)*2)
        self.tableWidget.setColumnCount(len(self.data[0]))
        i=0
        j=0
        for row in self.data:
            print(row)
            for item in row:
                print(item)
                self.tableWidget.setItem(i,j, QTableWidgetItem(str(item)))
                j=j+1
            i=i+1
        self.tableWidget.setColumnWidth(1, 150)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)
protoc={
6: 'UDP',
17: 'TCP',
2:'Other'
}

class Table:

    def __init__(self,root,data):
        total_rows = len(data)
        total_columns = len(data[0])
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):

                self.e = Entry(root, width=10, fg='blue',
                               font=('Arial',16,'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, data[i][j])

# take the data

# find total number of rows and
# columns in list


# create root window

def showData(data):
    sg.theme('Dark Amber')
    title_row=['Packet Number','Source IP','Destination IP','Protocol','Length','Info']
    table=[]
    table.append(title_row)
    total_rows = len(table)
    total_columns = len(table[0])
    for row in data:
        table.append(row)
    if data==[]:
        for i in range(11):
            table.append(['','','','','',''])
    #root = Tk()
    #t = Table(root,table)
    #scrollbar = Scrollbar(root)
    #scrollbar.pack(side=RIGHT, fill=Y)
    #scrollbar.config( command = root.yview )
    #root.mainloop()
    #root = Tk()
    #root.geometry("800x500")
    #scrollbar = Scrollbar(root)
    #scrollbar.pack( side = RIGHT, fill = Y )

    #mylist = Listbox(root, yscrollcommand = scrollbar.set,width=800 )
    #for line in table:
    #    mylist.insert(END,line)

    #mylist.pack( side = LEFT, fill = BOTH )
    #scrollbar.config( command = mylist.yview )

    #mainloop()
    App = QApplication(sys.argv)
    window = Window(table)
    sys.exit(App.exec())
    return 0
def capture(d):
    print(d,"is Captured")
    cmd = "C:/WinDump/WinDump.exe -i " + str(d)
    p = sub.Popen(cmd, shell=True, stdout=sub.PIPE)
    data=[]
    while True:
            line = p.stdout.readline().rstrip()
            if not line:
                break
            time.sleep(0.5)
            data.append(line)
            sg.Print(line)

app = QApplication(sys.argv)
widget = QWidget()
ls="C:/WinDump/WinDump -D"
dp=sub.Popen(ls,shell=True,stdout=sub.PIPE)
devices=netifaces.interfaces()
sg.theme('Black')
layout=[[sg.Text('Welcome To Packet Sniffer',font=("Helvetica", 14))],[sg.Text('Choose device for sinffing',font=("Helvetica", 14))]]
for d in devices:
    layout.append([sg.Button(d,key=(devices.index(d)+1))])
layout.append([sg.Text('Read Packets From a File')])
layout.append([sg.Text('Browse to .pcap file'),sg.FileBrowse()])
layout.append([sg.Button('Open')])
window = sg.Window('Packet Sniffer', layout)
# Create the event loop
while True:
    event,values = window.read()
    if event== 'Cancel' or event ==sg.WIN_CLOSED:
        # User closed the Window or hit the Cancel button
        break
    if event == 'Open':
        print('file opened')
        a = rdpcap(values['Browse'])
        data=[]
        for session in a:
            data.append([a.index(session),session.src,session.dst,protoc[session.proto],len(session),session.type])
        showData(data)
    elif event != ' ':
        capture(event)
    print(f'Event: {event}')

window.close()



#        window.FindElement('line').Update(line)



## But do not wait till netstat finish, start displaying output immediately ##
