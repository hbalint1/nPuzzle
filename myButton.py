from kivy.uix.button import Button

__author__ = 'Balint'

class MyButton(Button):
    """Custom button for the game."""

    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.grid_x = x
        self.grid_y = y
