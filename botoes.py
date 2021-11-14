from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.metrics import sp


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class MeuLabel(Label):

    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        self.size_hint = (1, None)
    

    def on_size(self,*args):
        self.text_size = (self.width - sp(10), None)


    def on_texture_size(self,*args):
        self.size = self.texture_size
        self.height += sp(20)