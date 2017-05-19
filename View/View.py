from functools import partial

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from Model.gameLogic import GameLogic
from Solver.solver import Solver, AlgorithmType, HeuristicType
from View.myButton import MyButton

__author__ = 'Balint'

kivy.require('1.0.1')


# Set window size.
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '450')


class Controller(BoxLayout):
    algo_types = ListProperty()
    heur_types = ListProperty()

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        for alg in AlgorithmType:
            self.algo_types.append(alg.name)
        for heur in HeuristicType:
            self.heur_types.append(heur.name)


class NPuzzle(App):
    """Class for the game."""

    Builder.load_file('kv_templates/my.kv')

    def build(self):
        self.controller = Controller()

        # Setting event handlers
        self.controller.ids.start_btn.bind(on_press=self.start_btn_pressed)
        self.controller.ids.random_btn.bind(on_press=self.random_btn_pressed)
        self.controller.ids.solve_btn.bind(on_press=self.solve_btn_pressed)
        return self.controller

    # region Methods

    def draw_layout(self):
        self.controller.ids.grid_layout.clear_widgets()
        for i in range(self.model.size):
            for j in range(self.model.size):
                btn = MyButton(i, j, text=str(self.model.grid[i][j]), font_size=24)
                if self.model.grid[i][j] == 0:
                    btn.background_color = 0, 0, 0, 1
                    btn.text = ''
                btn.bind(on_press=self.btn_pressed)
                self.controller.ids.grid_layout.add_widget(btn)

    #endregion

    # region Event Handlers

    def btn_pressed(self, instance):
        # print('My button <%s>' % (instance))
        btn = instance
        # print(btn.grid_x, btn.grid_y)
        if self.model.grid[btn.grid_x][btn.grid_y] != 0:
            self.model.step(btn.grid_x, btn.grid_y)
            # self.model.print_grid()
            self.controller.ids.grid_layout.clear_widgets()
            self.draw_layout()

    def random_btn_pressed(self, instance):
        self.model = GameLogic(4)
        self.draw_layout()

    def solve_btn_pressed(self, instance):
        solver = Solver(self.model.grid, self.model.size)
        steps = solver.run(
            AlgorithmType[self.controller.ids.algo_sp.text],
            HeuristicType[self.controller.ids.heur_sp.text])

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
        gridTxt = self.controller.ids.text_input.text
        print(gridTxt)
        self.model = GameLogic(4)
        self.model.grid_from_text(gridTxt)
        self.draw_layout()
        pass

    #endregion

    def worker(self, value, key, *largs):
        # print(value, key, *largs)
        print(value)
        self.model.grid = value
        self.draw_layout()
