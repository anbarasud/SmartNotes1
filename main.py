# SmartNotes placeholder main.py
from kivy.app import App
from kivy.uix.label import Label

class SmartNotesApp(App):
    def build(self):
        return Label(text='SmartNotes - placeholder')

if __name__ == '__main__':
    SmartNotesApp().run()
