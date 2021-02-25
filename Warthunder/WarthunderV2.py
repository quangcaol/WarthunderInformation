import json
import requests
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
import time


Parameter_index = ["AoA, deg","AoS, deg","Ny","Vy, m/s","Wx, deg/s","power 1, hp","RPM 1","pitch 1, deg","thrust 1, kgs","efficiency 1, %"]
# index of AOA AOS Ny Vy Wx Power RPM Pitch Thrust Efficent 


class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.delay = 500        #declare update interval for HUD
        self.T = 50             #declare sampling rate
        self.create_menubar()
        self.create_widget()


    def create_menubar(self):
        """Function Add menu item include Display quick information, Logging data, Save data"""

        menubar = tk.Menu(root)  
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Connect",command=self.update_state)
        self.filemenu.add_command(label="Record",command=self.startRecord)
        self.filemenu.add_command(label="Save as",command=self.saveRecord,state="disable")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=self.filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.creditPanel)
        menubar.add_cascade(label="Help", menu=helpmenu)


        root.config(menu=menubar)

    def create_widget(self):
        """ Function add label for quick information"""
        self.AoA = tk.Label(root,text="Degree",font = "Verdana 10 bold")
        self.AoA.grid(row=0,column=0,sticky='W',padx = 10, pady = 4)
        self.AoS = tk.Label(root,text="Degree",font = "Verdana 10 bold")
        self.AoS.grid(row=0,column=1,sticky='W',padx = 10, pady = 4)
        self.Ny = tk.Label(root,text="G",font = "Verdana 10 bold")
        self.Ny.grid(row=0,column=2,sticky='W',padx = 10, pady = 4)
        self.Vy = tk.Label(root,text="M/s",font = "Verdana 10 bold")
        self.Vy.grid(row=0,column=3,sticky='W',padx = 10, pady = 4)
        self.Wx = tk.Label(root,text="Deg/s",font = "Verdana 10 bold")
        self.Wx.grid(row=0,column=4,sticky='W',padx = 10, pady = 4)
        self.Power = tk.Label(root,text="HP",font = "Verdana 10 bold")
        self.Power.grid(row=1,column=0,sticky='W',padx = 10, pady = 4)
        self.RPM = tk.Label(root,text="RPM",font = "Verdana 10 bold")
        self.RPM.grid(row=1,column=1,sticky='W',padx = 10, pady = 4)
        self.Pitch = tk.Label(root,text="%",font = "Verdana 10 bold")
        self.Pitch.grid(row=1,column=2,sticky='W',padx = 10, pady = 4)
        self.Thrust = tk.Label(root,text="Kgs",font = "Verdana 10 bold")
        self.Thrust.grid(row=1,column=3,sticky='W',padx = 10, pady = 4)
        self.Efficent = tk.Label(root,text="%",font = "Verdana 10 bold")
        self.Efficent.grid(row=1,column=4,sticky='W',padx = 10, pady = 4)



    def update_label(self,State_value,Value):
        """Function update label value"""
        self.AoA.config(text=State_value[0])
        self.AoS.config(text=State_value[1])
        if 	Value[2] > 5 or Value[2] < -5:   # If G-load larger than 5 both in negative and positive, the Ny label will apear in red
            self.Ny.config(text=State_value[2],bg='red2')
        else:
            self.Ny.config(text=State_value[2],bg='snow')
        self.Ny.config(text=State_value[2])
        self.Vy.config(text=State_value[3])
        self.Wx.config(text=State_value[4])
        self.Power.config(text=State_value[5])
        if Value[6] > 3000:
            self.RPM.config(text=State_value[6],bg='red2')  # Similar to G-load but maximum RPM in warthunder is 3300
        else:
            self.RPM.config(text=State_value[6],bg='snow')
        self.Pitch.config(text=State_value[7])
        self.Thrust.config(text=State_value[8])
        self.Efficent.config(text=State_value[9])


    def UpdateElem(self):
        """Function get state json from localhost
            return Dict of all state
        """
        try:
            elem = requests.get('http://127.0.0.1:8111/state',timeout = 3)
        except requests.exceptions.Timeout:
            mb.showerror("Error","Request timeout")
            try:
                self.master.after_cancel(self.StateUpdate)
            except:
                pass
            try:
                self.master.after_cancel(self.RecordState)
            except:
                pass
            return None
        except requests.exceptions.ConnectionError:
            mb.showerror("Error","Lost connection")
            try:
                self.master.after_cancel(self.StateUpdate)
            except:
                pass
            try:
                self.master.after_cancel(self.RecordState)
            except:
                pass
            return None
        data = elem.json()
        if len(data) < 10:
            return None
        return data

    def SourceParser(self,x):
        """Function get dict of all state
           Return List of string consist of state label and value, List of value (INT)
        """
        Final_Value =[]
        State_Value =[]
        for i in Parameter_index:
                if i in x.keys():
                    Final_Value.append(i+'= '+str(x[i]))
                    State_Value.append(x[i])
                else:
                    Final_Value.append("Dont available")
                    State_Value.append(0)
        return Final_Value,State_Value

    def update_state(self):
        """Function update quick information after a delay time"""
        source = self.UpdateElem()
        if source != None:
            State_value,Value = self.SourceParser(source)
            self.update_label(State_value,Value)
            self.StateUpdate = self.master.after(self.delay, self.update_state)

    def creditPanel(self):
        mb.showinfo(title="Author information",message="Lương Quang Cao, mp32212@gmail.com")

    def startRecord(self):
        """Function delcare necessary variable for recording task """
        self.filemenu.entryconfig("Record",state="disable")
        self.filemenu.entryconfig("Save as",state="normal")
        self.Second = 0
        self.Record = []
        self.RecordState = self.master.after(self.T,self.update_record)

    def update_record(self):
        """Function update Record variable with state value every T milli second """
        self.Second += self.T
        source = self.UpdateElem()
        if source != None:
            State_value,Value = self.SourceParser(source)
            Value.append(self.Second)
            self.stateRecord = self.Record.append(Value)
        else:
            Value = [0,0,0,0,0,0,0,0,0]
            Value.append(self.Second)
            self.stateRecord = self.Record.append(Value)



    def saveRecord(self):
        """Function write Record variable to file"""
        self.master.after_cancel(self.RecordState)
        f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt",filetypes=[("Text", '*.txt'),("CSV type",'*.csv')],title= "Choose file name")
        if f is None:
            return
        f.write("AOA,AOS,Ny,Vy,Wx,Power,RPM,Pitch,Thrust,Efficent,Second\n")
        for i in self.Record:
            listToStr = ','.join([str(elem) for elem in i])
            f.write(listToStr+'\n') 
        f.close()
        self.filemenu.entryconfig("Record",state="normal")
        self.filemenu.entryconfig("Save as",state="disable")

    












if __name__ == "__main__": #main loop
    root = tk.Tk()
    root.title("Warthunder information")
    root.geometry("800x70")
    app = Window(master=root)
    app.mainloop()
