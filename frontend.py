from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen


class MyGrid(Widget):
    loc=ObjectProperty(None)
    time=ObjectProperty(None)
    numOfRec=ObjectProperty(None)

    def btn(self):
        print("location: ",self.loc.text,"time: ",self.time.text,"Recommendation number: ",self.numOfRec.text)
        self.loc.text=""
        self.time.text=""
        self.numOfRec.text=""



class MyApp(App):
    def build(self):
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()