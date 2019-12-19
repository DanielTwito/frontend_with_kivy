from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget



class MyGrid(Widget):
    loc=ObjectProperty(None)
    time=ObjectProperty(None)
    numOfRec=ObjectProperty(None)

    def submit_btn_handler(self):
        print("location: ",self.loc.text,"time: ",self.time.text,"Recommendation number: ",self.numOfRec.text)
        is_valid = self.validate_input(self.loc.text,self.time.text,self.numOfRec.text)
        if not is_valid:
            return
        self.loc.text=""
        self.time.text=""
        self.numOfRec.text=""

    def validate_input(self,location,d_time,rec_number):
        msg = Label(halign="center",valign="middle")
        btn = Button(text="close",size_hint=(1,0.3))
        btn.bind(on_press=lambda x:popup.dismiss())
        grid=GridLayout(cols=1)
        grid.add_widget(msg)
        grid.add_widget(btn)
        popup = Popup(title="Input Error",content=grid)
        popup.size_hint=(.4,.4)
        #TODO - valdiation of the location
        try:
            int(d_time)
        except:
            msg.text="time must be an integer number"
            popup.open()
            return False
        try:
            int(rec_number)
        except:
            msg.text = "number of recommendation\nmust be an integer number"
            popup.open()
            return False
        return True



class MyApp(App):
    def build(self):
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()