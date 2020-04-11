from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList


class Settings_(Screen):
    pass


class Map(Screen):
    pass


class Auth(Screen):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def __init__(self, **kwargs):
        self.before_item = None
        super().__init__(**kwargs)

    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        print(instance_item)
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        self.before_item = instance_item
        instance_item.text_color = self.theme_cls.primary_color


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.before_page= None
        self.icons_item = [
            {"icon": "map-outline", "text": "Map", "screen": Map},
            {"icon": "settings", "text": "Settings", "screen": Settings_},
        ]
        self.title = "TextWar"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(open("ui.kv", "r").read())
        for page in self.icons_item:
            screen = page["screen"](name=page["text"])
            item_drawer = ItemDrawer(icon=page["icon"], text=page["text"], on_release=self.changeScreen)
            self.root.ids.sm.add_widget(
                screen
            )
            self.root.ids.content_drawer.ids.md_list.add_widget(
                item_drawer
            )
            if self.icons_item[0] == page:
                self.root.ids.content_drawer.ids.md_list.set_color_item(item_drawer)
                self.root.ids.sm.current = page["text"]
                self.root.ids.toolbar.title = page["text"]

    def backward(self, a):
        self.root.ids.sm.current = self.before_page[0]
        self.root.ids.toolbar.left_action_items = [['menu', lambda x: self.root.ids.nav_drawer.set_state()]]
        self.root.ids.toolbar.title = self.before_page[0]
        self.root.ids.content_drawer.ids.md_list.set_color_item(self.before_page[1])
    def changeScreen(self, obj):
        print(obj)
        if obj.text == "Settings" or obj.text == "auth":
            self.before_page = (self.root.ids.sm.current, self.root.ids.content_drawer.ids.md_list.before_item)
            self.root.ids.toolbar.left_action_items = [['arrow-left', self.backward]]
        self.root.ids.nav_drawer.set_state()
        self.root.ids.sm.current = obj.text
        self.root.ids.toolbar.title = obj.text


MainApp().run()
