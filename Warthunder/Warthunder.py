from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import tkinter as tk


Parameter_index = [4,5,6,7,8,29,30,34,35,36]


class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widget()
        self.RunBrowser()
        master.attributes('-alpha', 0.5)
        self.update_state()




    def create_widget(self):
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



    def update_label(self,State_value):
        self.AoA.config(text=State_value[0])
        self.AoS.config(text=State_value[1])
        if 	self.Text2Double(State_value[2]) > 5:
            self.Ny.config(text=State_value[2],bg='red2')
        else:
            self.Ny.config(text=State_value[2],bg='snow')
        self.Ny.config(text=State_value[2])
        self.Vy.config(text=State_value[3])
        self.Wx.config(text=State_value[4])
        self.Power.config(text=State_value[5])
        if self.Text2Double(State_value[6]) > 3000:
            self.RPM.config(text=State_value[6],bg='red2')
        else:
            self.RPM.config(text=State_value[6],bg='snow')
        self.Pitch.config(text=State_value[7])
        self.Thrust.config(text=State_value[8])
        self.Efficent.config(text=State_value[9])

    def RunBrowser(self):
        self.driver = webdriver.Edge('msedgedriver.exe')
        self.driver.get("http://localhost:8111/")

    def UpdateElem(self):
        elem = self.driver.find_element_by_id("state")
        source = elem.get_attribute('innerHTML')
        return source

    def SourceParser(self,source):
        State_Value = []
        soup = BeautifulSoup(source, 'html.parser')
        state = soup.findAll("li")
        for i in Parameter_index:
            State_Value.append(state[i].text)
        return State_Value

    def update_state(self):
        source = self.UpdateElem()
        State_value = self.SourceParser(source)
        self.update_label(State_value)
        self.master.after(500, self.update_state)
    
    def Text2Double(self,text):
        index = 0
        for i in text:
            if i.isdigit() and text[index-1] == '=':
                break
            index += 1
        number = text[index:]
        if len(number) ==0:		
            number = 0
        return float(number)














if __name__ == "__main__":
    root = tk.Tk()
    root.title("Warthunder information")
    root.geometry("750x70")
    app = Window(master=root)
    app.mainloop()