from kivy.lang import Builder
from kivymd.app import MDApp

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "My Material Application"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(open("ui.kv","r").read())
MainApp().run()