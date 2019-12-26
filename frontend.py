from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from backend import Database


class MyPopup(Popup):

    def __init__(self, **kwargs):
        grid = GridLayout(cols=1)
        super().__init__(title="Input Error", content=grid,size_hint = (.4, .4))
        self.msg = Label(halign="center", valign="middle")
        btn = Button(text="close", size_hint=(1, 0.3))
        btn.bind(on_press=lambda x: self.dismiss())
        grid.add_widget(self.msg)
        grid.add_widget(btn)

    def set_msg(self,text):
        self.msg.text=text


class MyGrid(Widget):
    loc=ObjectProperty(None)
    time=ObjectProperty(None)
    numOfRec=ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database=Database()

    def submit_btn_handler(self):
        loc = self.loc.text
        time = self.time.text
        nor = self.numOfRec.text
        print("location: ",loc,"time: ",time,"Recommendation number: ",nor)
        valid_input = self.validate_input(loc,time,nor)
        if not valid_input:
            return
        x=self.database.recommand(loc,time,nor)

        self.loc.text=""
        self.time.text=""
        self.numOfRec.text=""

    def validate_input(self,location,d_time,rec_number):
        popup=MyPopup()
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