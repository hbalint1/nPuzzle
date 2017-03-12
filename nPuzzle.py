from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from gameLogic import GameLogic
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from myButton import MyButton
from kivy.config import Config
from node import Node
from solver import Solver
from solver import AlgorithmTye

kivy.require('1.0.1')

__author__ = 'Balint'
"""nPuzzle game with Python."""

# Set window size.
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '450')


class NPuzzle(App):
    """Class for the game."""

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.box_layout = BoxLayout(orientation='vertical', spacing=10)
        box_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        text_input = TextInput(text='Hello World!', multiline=False)
        random_btn = Button(text='Random')
        solve_btn = Button(text='Solve')
        start_btn = Button(text='Start')
        box_layout2.add_widget(text_input)
        box_layout2.add_widget(start_btn)
        box_layout3 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        box_layout3.add_widget(random_btn)
        box_layout3.add_widget(solve_btn)
        self.box_layout.add_widget(box_layout2)
        self.grid_layout = GridLayout(cols=self.model.size, size_hint=(1, .8))
        self.box_layout.add_widget(self.grid_layout)
        self.box_layout.add_widget(box_layout3)
        self.draw_layout()

    def draw_layout(self):
        for i in range(self.model.size):
            for j in range(self.model.size):
                btn = MyButton(i, j, text=str(self.model.grid[i][j]), font_size=24)
                if self.model.grid[i][j] == 0:
                    btn.background_color = 0, 0, 0, 1
                    btn.text = ''
                btn.bind(on_press=self.btn_pressed)
                self.grid_layout.add_widget(btn)

    def build(self):
        return self.box_layout

    def btn_pressed(self, instance):
        # print('My button <%s>' % (instance))
        btn = instance
        # print(btn.grid_x, btn.grid_y)
        if self.model.grid[btn.grid_x][btn.grid_y] != 0:
            self.model.step(btn.grid_x, btn.grid_y)
            # self.model.print_grid()
            self.grid_layout.clear_widgets()
            self.draw_layout()

if __name__ == '__main__':
    gameModel = GameLogic(4)
    game = NPuzzle(gameModel)
    solver = Solver(game.model.grid, game.model.size)
    solver.run(AlgorithmTye.ASTAR, 0)
    steps = solver.astar2(Node(game.model.grid, None),
                          Node([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]], None))
    game.run()