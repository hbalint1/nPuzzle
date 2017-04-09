from functools import partial
import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from gameLogic import GameLogic
from myButton import MyButton
from kivy.config import Config
from solver import Solver, AlgorithmTye

__author__ = 'Balint'

kivy.require('1.0.1')


# Set window size.
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '450')


class NPuzzle(App):
    """Class for the game."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.model = model
        self.initialize_layout()
        # self.draw_layout()

    def build(self):
        return self.box_layout

    # region Methods

    def initialize_layout(self):
        self.box_layout = BoxLayout(orientation='vertical', spacing=10)
        box_layout2 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        self.text_input = TextInput(text='14,5,13,0,4,7,8,9,3,15,10,1,11,2,12,6', multiline=False)
        random_btn = Button(text='Random')
        random_btn.bind(on_press=self.random_btn_pressed)
        solve_btn = Button(text='Solve')
        solve_btn.bind(on_press=self.solve_btn_pressed)
        start_btn = Button(text='Start')
        start_btn.bind(on_press=self.start_btn_pressed)
        box_layout2.add_widget(self.text_input)
        box_layout2.add_widget(start_btn)
        box_layout3 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        box_layout3.add_widget(random_btn)
        box_layout3.add_widget(solve_btn)
        self.box_layout.add_widget(box_layout2)
        # self.grid_layout = GridLayout(cols=self.model.size, size_hint=(1, .8))
        self.grid_layout = GridLayout(cols=4, size_hint=(1, .8))
        self.box_layout.add_widget(self.grid_layout)
        self.box_layout.add_widget(box_layout3)

    def draw_layout(self):
        self.grid_layout.clear_widgets()
        for i in range(self.model.size):
            for j in range(self.model.size):
                btn = MyButton(i, j, text=str(self.model.grid[i][j]), font_size=24)
                if self.model.grid[i][j] == 0:
                    btn.background_color = 0, 0, 0, 1
                    btn.text = ''
                btn.bind(on_press=self.btn_pressed)
                self.grid_layout.add_widget(btn)

    #endregion

    # region Event Handlers

    def btn_pressed(self, instance):
        # print('My button <%s>' % (instance))
        btn = instance
        # print(btn.grid_x, btn.grid_y)
        if self.model.grid[btn.grid_x][btn.grid_y] != 0:
            self.model.step(btn.grid_x, btn.grid_y)
            # self.model.print_grid()
            self.grid_layout.clear_widgets()
            self.draw_layout()

    def random_btn_pressed(self, instance):
        self.model = GameLogic(4)
        self.draw_layout()

    def solve_btn_pressed(self, instance):
        solver = Solver(self.model.grid, self.model.size)
        steps = solver.run(AlgorithmTye.ASTAR, 0)
        if(steps is None):
            box = BoxLayout(orientation='vertical', spacing=10)
            box.add_widget(Label(text='A feladat megoldhatatlan!'))
            btn = Button(text='ok')
            box.add_widget(btn)
            popup = Popup(title='Hiba!',
                          content=box,
                          auto_dismiss=False)
            btn.bind(on_press=popup.dismiss)
            popup.open()
            return

        steps = steps[1:]
        a = 0
        for i in steps:
            a += 1
            Clock.schedule_once(partial(self.worker, i, 'my key'), a * 0.5)

    def start_btn_pressed(self, instance):
        gridTxt = self.text_input.text
        print(gridTxt)
        self.model = GameLogic(4)
        self.model.grid_from_text(gridTxt)
        self.draw_layout()
        pass

    #endregion

    def worker(self, value, key, *largs):
        print(value, key, *largs)
        self.model.grid = value
        self.draw_layout()
