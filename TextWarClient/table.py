from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, BoundedNumericProperty, NumericProperty
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
Builder.load_string('''
<Row>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0
        Rectangle:
            size: 1, 1
            pos: self.pos
    itemText: ''
    Cell:
        font_size: 20
        size: 0.1, 20 # TODO: column.size_x, 1
        text: root.itemText
        # TODO read BorderImage doc for border values
        font_name: "./Unifont.ttf"


<RV>:
    id: rv
    viewclass: 'Row'
    scroll_type: ['bars', 'content']
    scroll_wheel_distance: dp(114)
    bar_width: dp(10)
    RecycleGridLayout:
        id: rgl
        default_size: None, dp(30) 
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(1)
''')


class Cell(MDFlatButton):
    width = BoundedNumericProperty(
        2, min=2, max=None, errorhandler=lambda x: 2
    )
    increment_width = NumericProperty("2dp")


class RV(RecycleView):
    list_items = ListProperty([])
    def __init__(self, **kwargs, ):
        super(RV, self).__init__(**kwargs)
        self.data = [{'itemText': 'Loading', 'paren': self, 'index': 0}]
    def set_cols(self,cols_):
        self.ids.rgl.cols = cols_



class Row(BoxLayout):
    paren = ObjectProperty() #the instance of the rv

    def __init__(self, **kwargs):
        super(Row, self).__init__(**kwargs)
