from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
Screen:
    MDLabel:
        text: "SmartNotes1 placeholder"
        halign: "center"
'''

class SmartNotes1App(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    SmartNotes1App().run()
