from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList


class Upload(Screen):
    pass


class Folder(Screen):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.icons_item = [
            {"icon": "folder", "text": "My files", "screen": Folder},
            {"icon": "upload", "text": "Upload", "screen": Upload}
        ]
        self.title = "TextWar"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(open("ui.kv", "r").read())
        for page in self.icons_item:
            self.root.ids.sm.add_widget(
                page["screen"](name=page["text"])
            )
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=page["icon"], text=page["text"], on_release=self.changeScreen)
            )

    def changeScreen(self, obj):
        self.root.ids.nav_drawer.set_state()
        self.root.ids.sm.current = obj.text


MainApp().run()
