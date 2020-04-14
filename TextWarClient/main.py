from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
import json


class Remember(MDSwitch):
    def changeState(self):
        print(self.active)
        if self.active == 0:
            self.active = 1
        else:
            self.active = 0


class Settings_(Screen):
    pass


class Map(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.update_map(open("town_1.json", "r").read())

    def update_map(self, json_):
        from TextWarClient.table import TableView, TableColumn, TableCell, TableRow
        table = TableView((500, 1000), pos_hint={'center_x': .5, 'center_y': .5})  # 在屏幕正中央放一个表格
        json__ = json.loads(json_)  # 读取json
        hash_map = json__["hashmap"]  # 获取hash_map
        map_ = json__["map"]  # 获取map_
        first = True
        row = {}  # 创建dict
        for c in map_:  # 循环map中的每个元素 即每一行 i为第几行 c为那一行对应的列表
            row.clear()
            for ib, b in enumerate(c):  # 循环c中的每个元素 即每一格 ib为第几列 b为某个元素的字符串
                for ic, text in enumerate(hash_map):  # 循环hash_map中的每个元素 ic为第几个元素 text表示字符串
                    if b == ic:  # 如果某一个元素的字符串与hash_map中的某个元素相对应则
                        row[str(ib + 1)] = text.replace("*","")  # 把这一行加入到row
            if first:
                for i in range(len(row)):
                    print(i+1)
                    table.add_column(TableColumn("Col", key=str(i + 1), hint_text='0'))  # 往表格上添加一列
                first = False
            table.add_row(row)  # 在表格中加入这行

        self.add_widget(table)
        # table.add_column(TableColumn("Col1", key="1", hint_text='0'))
        # table.add_column(TableColumn("Col2", key="2", hint_text='0'))
        # table.add_column(TableColumn("Col3", key="3", hint_text='0'))
        # table.add_column(TableColumn("Col3", key="4", hint_text='0'))
        # table.add_column(TableColumn("Col3", key="5", hint_text='0'))
        # table.add_column(TableColumn("Col3", key="6", hint_text='0'))
        # for i in range(30):
        #     row = {'1': "░░", '2': "　", '3': str(2*i+2), '4': str(8*i+2), '5': str(9*i+2), '6': str(9*i+10)}
        #     table.add_row(row)


class Auth(Screen):
    pass


class ItemDrawer(OneLineIconListItem):
    def __repr__(self):
        return self.text

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
        self.before_page = None
        self.hidden_item = [
            {"text": "Auth", "screen": Auth},
        ]
        self.icons_item = [
            {"icon": "map-outline", "text": "Map", "screen": Map},
            {"icon": "settings", "text": "Settings", "screen": Settings_},
        ]
        self.title = "TextWar"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(open("ui.kv", "r").read())
        for page in self.hidden_item:
            screen = page["screen"](name=page["text"])
            self.root.ids.sm.add_widget(
                screen

            )

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
        self.root.ids.nav_drawer.swipe_distance = 10

    def changeScreen(self, obj):
        print(obj)
        if str(obj) == "Settings" or str(obj) == "Auth":
            self.before_page = (self.root.ids.sm.current, self.root.ids.content_drawer.ids.md_list.before_item)
            self.root.ids.toolbar.left_action_items = [['arrow-left', self.backward]]
            self.root.ids.nav_drawer.swipe_distance = 99999
        self.root.ids.nav_drawer.set_state()
        self.root.ids.sm.current = str(obj)
        self.root.ids.toolbar.title = str(obj)


MainApp().run()
