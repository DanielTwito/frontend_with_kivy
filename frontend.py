from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from backend import Database


class MyPopup(Popup):
    """
    This Class is custom popup window,
    that allow me to control the title and the msg
    and also include close button
    """
    def __init__(self, **kwargs):
        grid = GridLayout(cols=1)
        super().__init__(content=grid,size_hint = (.4, .4))
        self.msg = Label(halign="center", valign="middle")
        btn = Button(text="close", size_hint=(1, 0.3))
        btn.bind(on_press=lambda x: self.dismiss())
        grid.add_widget(self.msg)
        grid.add_widget(btn)

    def set_msg(self,text):
        self.msg.text=text

    def set_title(self,title):
        self.title = title

class MyGrid(Widget):
    loc=ObjectProperty(None)
    time=ObjectProperty(None)
    numOfRec=ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database=Database()

    def submit_btn_handler(self):
        """
        submit button handler this function
        collect the data from the user input and send it to the backend side
        :return: None if the input is invalid
        """
        loc = self.loc.text
        time = self.time.text
        nor = self.numOfRec.text
        print("location: ",loc,"time: ",time,"Recommendation number: ",nor)
        valid_input = self.validate_input(loc,time,nor)
        if not valid_input:
            return
        recommendation_list = self.database.recommend(loc, time, nor)
        popup = MyPopup()
        popup.set_title("System Recommendation")
        popup.set_msg("We Recommend you to travel to:\n"+"\n".join(recommendation_list))
        popup.open()
        self.loc.text=""
        self.time.text=""
        self.numOfRec.text=""

    def validate_input(self,location,d_time,rec_number):
        """
        This function validate the input of the user
        for date validate that d_time is fro the form of DD/MM/YYYY
        for location must be exist in the database
        for rec_number must be a integer number
        :param location: string location to check
        :param d_time: string duration time to check
        :param rec_number: recommendation number to check
        :return: True if all the variable satisfied the constraints
                 False otherwise
        """
        popup=MyPopup()
        popup.set_title("Input Error")
        """validate if location exist in the DB"""
        if not self.database.is_location_exist(location):
            popup.set_msg("location cant be found")
            popup.open()
            return False
        """check if duration time is an integer number"""
        try:
            int(d_time)
        except:
            popup.set_msg("time must be an integer number")
            popup.open()
            return False
        try:
            int(rec_number)
        except:
            popup.set_msg( "number of recommendation\nmust be an integer number")
            popup.open()
            return False
        return True



class MyApp(App):
    def build(self):
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()