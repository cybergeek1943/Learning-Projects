"""
Game: Color the Snake!
Isaac Wolford
10/18/2024
"""
# ========================================= Set Defaults and Load Userdata =============================================
import os
import json
import platform


# Global Variables
APP_NAME: str = 'Color the Snake!'
MODE: int = 1
SPEED: int = 2
LENGTH: int = 8
FOOD_ABUNDANCE: int = 2
WALL_TELEPORT: bool = True
HIGHSCORE: int = 0


class UserdataFile:
    """Singleton interface for loading and saving user data."""
    __debug_mode__: bool = False

    def __init__(self):
        os.makedirs(directory:=self.get_appdata_directory(), exist_ok=True)
        self.file_path = os.path.join(directory, 'userdata.json') if not self.__debug_mode__ else '.\\userdata.json'
        self.__load()

    @staticmethod
    def get_appdata_directory() -> str:
        match platform.system():
            case 'Windows':
                return os.path.join(os.getenv('APPDATA'), APP_NAME)
            case 'Darwin':  # Mac OS
                return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', APP_NAME)
            case _:  # Linux and other Unix-like systems
                return os.path.join(os.path.expanduser('~'), f'.{APP_NAME}')

    def save(self) -> None:
        with open(self.file_path, mode='w') as f:
            f.write(json.dumps({'mode': MODE, 'speed': SPEED, 'length': LENGTH, 'food_abundance': FOOD_ABUNDANCE, 'wall_teleport': WALL_TELEPORT, 'highscore': HIGHSCORE}))

    def __load(self) -> None:
        global MODE, SPEED, LENGTH, FOOD_ABUNDANCE, WALL_TELEPORT, HIGHSCORE
        try:
            with open(self.file_path, mode='r') as f:
                data: dict = json.load(f)
                MODE = data['mode']
                SPEED = data['speed']
                LENGTH = data['length']
                FOOD_ABUNDANCE = data['food_abundance']
                WALL_TELEPORT = data['wall_teleport']
                HIGHSCORE = data['highscore']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):  # if error occurs then reload default settings.
            self.save()
            self.__load()
userdata_file: UserdataFile = UserdataFile()




# =================================================== Game Start Menu ==================================================
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Color the Snake!")
root.configure(bg="black")
root.geometry("650x650")
root.wm_resizable(False, False)
root.protocol("WM_DELETE_WINDOW", lambda: (save_settings_changes(), root.after(16, exit)))


# This binary data contains the colored title of game as .GIF image file.
__logo__: bytes = b'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'
logo = tk.PhotoImage(data=__logo__)
title_label = tk.Label(root, image=logo, bg="black")
title_label.pack(pady=20)
font_large = ('System', 17)
font_small = ('System', 16)


class ToggleSwitch(tk.Label):
    def __init__(self, master=None):
        self.unchecked_image = tk.PhotoImage(data=b'R0lGODlhPAAeAHcAACH5BAQAAP8ALAAAAAA8AB4AgwAAAAsLCx8fHy4uLjw8PEVFRWtra3FxcXp6ev/m5gAAAAAAAAAAAAAAAAAAAAAAAASnMMlJq7046827/2AockBpnmiqrixrnUQhz3RNtHj+mgbi/8CgIUdcvQKDwSHIBB6SgaIU8BI0r0zBtFjFen3ara4CsH6xYXGre76m1UayuZ2Fr+X05tuOYueBe3wmfn9ggiqEhYGHiX+Lgo15j3yRdJN2lW2XcJlnm2qdX59ioV6jW0dJS3RPA1GHfWQ8eUOwiLIlMTW7Mze2KTu/sCPExcbHyMnKExEAIf4KUGhvdG9TY2FwZQA7')
        self.checked_image = tk.PhotoImage(data=b'R0lGODlhPAAeAHcAACH5BAQAAP8ALAAAAAA8AB4AgwAAAA42DhJIEhhgGCSQJCecJzDAMED/QP/m5gAAAAAAAAAAAAAAAAAAAAAAAAAAAAS0EMlJq7046827/2AockBpnmiqrixrtTAcEHRt30RwvnGfDoegcEg8DHYVnxIgGBSKUGFhICjxljFDdCs0WJPYLJfrBVzDLO04Wj6jVep1sQ1+r+LyIZ1iT+fnX3x9cH9EexODhIVdgYiJKHiFhxKPkIuMZnWVAJF/kwibJp15n6Elo3KlpqhrqqGsY66bsGSNlKZNT39TVZmCpgBAf0cmbpszOMk0OsWawG8j0dLT1NXW1xMRACH+ClBob3RvU2NhcGUAOw==')
        super().__init__(master, image=self.unchecked_image, bd=0)
        self.toggled = False
        self.bind("<Button-1>", lambda _: self.toggle())

    def set_toggled(self, b: bool):
        self.toggled = b
        self.config(image=self.checked_image if b else self.unchecked_image)

    def toggle(self):
        self.set_toggled(not self.toggled)

    @property
    def is_toggled(self) -> bool:
        return self.toggled


class Settings(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(bg="black")

        # Player Mode
        l = tk.Label(self, text="Mode: ", font=font_large, bg="black", fg="white")
        l.grid(row=0, column=0, sticky="e")
        self._mode = ttk.Combobox(self, values=["Single Player", "Double Player"], font=font_small, state="readonly", width=17)
        self._mode.bind("<<ComboboxSelected>>", lambda _: root.focus())  # so that focus does not cause blue highlight to stay on combobox.
        self._mode.current(MODE-1)
        self._mode.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Speed Slider
        l = tk.Label(self, text="Speed: ", font=font_large, bg="black", fg="white")
        l.grid(row=1, column=0, sticky="e")
        self._speed = tk.Scale(self, from_=1, to=4, orient="horizontal", font=font_small, bg="black", fg="white", length=150)
        self._speed.set(SPEED)
        self._speed.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Length Slider
        l = tk.Label(self, text="Initial Length: ", font=font_large, bg="black", fg="white")
        l.grid(row=2, column=0, sticky="e")
        self._length = tk.Scale(self, from_=4, to=12, orient="horizontal", font=font_small, bg="black", fg="white", length=150)
        self._length.set(LENGTH)
        self._length.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Food Abundance
        l = tk.Label(self, text="Food Abundance: ", font=font_large, bg="black", fg="white")
        l.grid(row=3, column=0, sticky="e")
        self._food = tk.Scale(self, from_=1, to=10, orient="horizontal", font=font_small, bg="black", fg="white", length=150)
        self._food.set(FOOD_ABUNDANCE)
        self._food.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Wall Teleport
        l = tk.Label(self, text="Wall Teleport: ", font=font_large, bg="black", fg="white")
        l.grid(row=4, column=0, sticky="e")
        self._teleport = ToggleSwitch(self)
        self._teleport.set_toggled(WALL_TELEPORT)
        self._teleport.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    @property
    def mode(self) -> int:
        return self._mode.current() + 1

    @property
    def speed(self) -> int:
        return int(self._speed.get())

    @property
    def length(self) -> int:
        return int(self._length.get())
    
    @property
    def food_abundance(self) -> int:
        return int(self._food.get())

    @property
    def wall_teleport(self) -> bool:
        return self._teleport.is_toggled
settings = Settings()
settings.pack()
WINDOW_POS: tuple[int, int] = (0, 0)
def save_settings_changes():
    global WINDOW_POS, MODE, SPEED, LENGTH, FOOD_ABUNDANCE, WALL_TELEPORT
    x, y = root.geometry().split('+', 1)[1].split('+')
    WINDOW_POS = (int(x), int(y))
    MODE = settings.mode
    SPEED = settings.speed
    LENGTH = settings.length
    FOOD_ABUNDANCE = settings.food_abundance
    WALL_TELEPORT = settings.wall_teleport
    userdata_file.save()


# Play Button
play_button = tk.Button(root, text='Play!', font=font_small, bg="#28a2b3", width=48)
play_button.pack(pady=(15, 30))
play_button.bind("<ButtonRelease-1>", lambda _: (save_settings_changes(), root.after(16, root.destroy)))


# User Instructions
instructions: str = """
The goal of the game is to fill up and extend the snake with colors. If a snake crashes into itself then the colors it has gathered will be dispersed across the screen and its tail will be lost.

Instructions:
• The first player uses arrow keys to control their snake.
• The second player uses the WASD keys to control their snake.
• Pressing + or - will speed up and slow down the snake.
• Pressing the Space key will pause/play the game.
"""
instructions_label = tk.Label(root, text=instructions, wraplength=650, font=("Consolas", 10), justify='left', bg="black", fg="white")
instructions_label.pack(padx=20, pady=10)


root.mainloop()




# ===================================================== Snake Game =====================================================
# noinspection PyUnresolvedReferences, PyProtectedMember
from turtle import _Screen, Turtle, TurtleScreen
from random import randint, choice as rand_choice
from enum import Enum
from time import sleep as _sleep
from typing import Callable
COLORS: tuple[str, ...] = "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#33FFA1", "#FF8633", "#33FFD1", "#A133FF", "#FFD133", "#33A1FF", '#A6076B', '#298862', '#FF6600', '#385BB4', '#D91656', '#0D92F4', '#FF885B', '#6EC207', '#B8001F'


class WindowEdge(Enum):
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3


class Window(_Screen):
    """Singleton that manages screen: screen updates, edge wrapping/teleportation, and coordinates."""
    def __init__(self, width: int = 640, height: int = 640, bg_color: str = 'black') -> None:
        super().__init__()
        Turtle._screen = self
        self.title(APP_NAME)
        self.setup(width, height, *WINDOW_POS)
        self.bgcolor(bg_color)
        self.tracer(False)
        self.delay(5)  # to make animation a bit faster when expanding segments
        self.listen()
        self.snakes: list[Snake] = []

        # Attributes
        self.center_to_height = self.window_width() // 2
        self.center_to_width = self.window_height() // 2
        def on_resize(event):
            self.center_to_height = event.height // 2
            self.center_to_width = event.width // 2
        self._root.bind("<Configure>", on_resize, add="+")  # add="+" makes the event propagate beyond the on_resize()
        self.frame_rate = 0.09 / SPEED  # in seconds for the snake to update. This is the speed of snake.
        self.onkey(key='plus', fun=self.increment_frame_rate)
        self.onkey(key='minus', fun=lambda: self.increment_frame_rate(negative=True))

    def increment_frame_rate(self, negative: bool = False) -> None:
        global SPEED
        if (SPEED == 4 and not negative) or (SPEED == 1 and negative):
            return
        SPEED += -1 if negative else 1
        self.frame_rate = 0.09 / SPEED

    def rand_xcor(self, margin: int = 50) -> int:
        return randint(-(_:=self.center_to_width) + margin, _ - margin)

    def rand_ycor(self, margin: int = 50) -> int:
        return randint(-(_:=self.center_to_height) + margin, _ - margin)

    def random_location(self) -> tuple[int, int]:
        center_to_width = self.center_to_width
        center_to_height = self.center_to_height
        return randint(-center_to_width, center_to_width), randint(-center_to_height, center_to_height)

    def teleport_edge_touchers(self) -> None:
        for s in self.snakes:
            if e:=self.snake_collided_with_wall(s):
                match e:
                    case WindowEdge.Right: s.head.setx(-self.center_to_width)
                    case WindowEdge.Left: s.head.setx(self.center_to_width)
                    case WindowEdge.Top: s.head.sety(-self.center_to_height)
                    case WindowEdge.Bottom: s.head.sety(self.center_to_height)

    def snake_collided_with_wall(self, snake: 'Snake') -> WindowEdge | None:
        """If the `snake` collided with wall, then return the edge of the window that it collided with."""
        h: SnakeSegment = snake.head
        right: int = self.center_to_width
        left: int = -self.center_to_width
        top: int = self.center_to_height
        bottom: int = -self.center_to_height
        if h.xcor() > right: return WindowEdge.Right
        elif h.xcor() < left: return WindowEdge.Left
        elif h.ycor() > top: return WindowEdge.Top
        elif h.ycor() < bottom: return WindowEdge.Bottom
        return None

    def register_snake(self, snake: 'Snake') -> None:
        self.snakes.append(snake)

    def timer(self, ms: int, func: Callable = lambda: None) -> None:
        self.delay()
        self.ontimer(func, ms)

    def frame_update(self, pause: float = None) -> None:
        super().update()
        if pause is None: pause = self.frame_rate
        _sleep(pause)

    @staticmethod
    def sleep(seconds: float, func: Callable = lambda: None) -> None:
        _sleep(seconds)
        func()
window: TurtleScreen | Window = Window()  # Singleton


class Food(Turtle):
    def __init__(self, x: int, y: int, color: str) -> None:
        super().__init__()
        self.penup()
        self.shape('circle')
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color(color)
        self.goto(x, y)

    @property
    def food_color(self) -> str:
        return self.color()[0]

    def refresh(self) -> None:
        self.color(rand_choice(COLORS))
        self.goto(window.rand_xcor(), window.rand_ycor())


class FoodManager:
    """Singleton that manages food for the snakes."""
    def __init__(self) -> None:
        super().__init__()
        self.unused_food: list[Food] = []
        self.food: list[Food] = []
        self.snakes: list[Snake] = []
        # for _ in range(FOOD_ABUNDANCE): self.create_food()  # no need since snake initially creates points for us by expanding its initial colors.

    def create_food(self, x: int = None, y: int = None, color: str = None) -> None:
        if not x: x = window.rand_xcor()
        if not y: y = window.rand_ycor()
        if not color: color = rand_choice(COLORS)
        if self.unused_food:
            f: Food = self.unused_food.pop()
            f.goto(x, y)
            f.color(color)
            f.showturtle()
            self.food.append(f)
            return
        self.food.append(Food(x, y, color))

    def register_snake(self, eater: 'Snake') -> None:
        self.snakes.append(eater)

    @property
    def food_touchers(self) -> list[tuple['Snake', Food]]:
        out: list[tuple['Snake', Food]] = []
        for s in self.snakes:
            for f in self.food:
                if f.distance(s.head) < 30:
                    out.append((s, f))
        return out

    def handle_food_collisions(self) -> None:
        for s, f in self.food_touchers:
            s.eat_food(f)
            if len(self.food) <= FOOD_ABUNDANCE:
                f.refresh()
            else:
                f.hideturtle()
                self.food.remove(f)
                self.unused_food.append(f)
food_manager: FoodManager = FoodManager()


class SnakeSegment(Turtle):
    def __init__(self, pos: tuple[float, float], heading: float = 0, color: str = 'white') -> None:
        super().__init__()
        self.penup()
        self.color(color)
        self.shape('square')
        self.goto(pos)
        self.setheading(heading)
        self.speed(9)

    @property
    def is_colored(self) -> bool:
        return self.color()[0] != 'white'

    @property
    def seg_color(self) -> str:
        return self.color()[0]

    def animated_goto(self, x: float, y: float) -> None:
        window.tracer(True)
        self.goto(x, y)
        window.tracer(False)


def key_pressed(func: Callable):  # wrapper to prevent bug of two inputs affecting snakes heading before a move is complete.
    def f(self: 'Snake'):
        if self.input_enabled:
            self.input_enabled = False
            func(self)
    return f


class Snake:
    def __init__(self, snake_length: int = LENGTH, reverse_dir: bool = False) -> None:
        self.score: int = 0
        self.on_score_changed: Callable = lambda: None
        self.segments: list[SnakeSegment] = [SnakeSegment((-x, 50), color=rand_choice(COLORS)) for x in range(0, snake_length * 20, 21)]\
            if not reverse_dir else [SnakeSegment((x, -50), heading=180) for x in range(0, snake_length * 20, 21)]
        self.head: SnakeSegment = self.segments[0]  # will be the head segment
        self.head.shapesize(1.3, 1.3)
        self.last_collision_index: int = 0
        window.register_snake(self)
        food_manager.register_snake(self)
        self.input_enabled: bool = False

    def __len__(self) -> int:
        return len(self.segments)

    def move(self) -> None:
        self.input_enabled = True
        for idx in range(1, len(self)).__reversed__():  # loops through segments from tail to head.
            leading_seg: SnakeSegment = self.segments[idx - 1]
            self.segments[idx].setheading(leading_seg.heading())
            self.segments[idx].goto(leading_seg.xcor(), leading_seg.ycor())
        self.head.forward(20)

    def undo_move(self, max_steps: int = 10, show_steps: bool = True) -> None:
        def reverse_heading() -> None:
            for seg in self.segments:
                match seg.heading():
                    case 0: seg.setheading(180)
                    case 180: seg.setheading(0)
                    case 90: seg.setheading(270)
                    case 270: seg.setheading(90)
        reverse_heading()
        head_heading: float = self.head.heading()
        step: int = 0
        while step != max_steps:
            step += 1
            if head_heading != self.head.heading():
                break
            for idx in range(len(self)-1):
                leading_seg: SnakeSegment = self.segments[idx + 1]
                self.segments[idx].setheading(leading_seg.heading())
                self.segments[idx].goto(leading_seg.xcor(), leading_seg.ycor())
            self.segments[-1].forward(20)
            if show_steps:
                window.frame_update(pause=0.15)
        reverse_heading()

    @property
    def heading(self) -> float:
        return self.head.heading()

    def setheading(self, heading: float) -> None:
        self.head.setheading(heading)

    @key_pressed
    def right(self) -> None:
        if self.heading != 180: self.setheading(0)

    @key_pressed
    def left(self) -> None:
        if self.heading != 0: self.setheading(180)

    @key_pressed
    def up(self) -> None:
        if self.heading != 270: self.setheading(90)

    @key_pressed
    def down(self) -> None:
        if self.heading != 90: self.setheading(270)

    def is_self_collision(self) -> bool:
        for idx, seg in enumerate(self.segments[1:]):
            if self.head.distance(seg) < 10:
                self.last_collision_index = idx + 1
                return True
        return False

    def extend(self, color: str = 'white') -> None:
        tail: SnakeSegment = self.segments[-1]
        self.segments.append(SnakeSegment((tail.xcor(), tail.ycor()), tail.heading(), color=color))

    def eat_food(self, food: Food) -> None:
        self.increment_score()
        color: str = food.food_color
        if self.segments[-1].is_colored:  # if the snake is already fully colored then extends it.
            self.extend(color)
            return
        # elif the snake is still not fully colored then color the next uncolored segment.
        for idx in range(1, len(self)).__reversed__():
            leading_seg: SnakeSegment = self.segments[idx - 1]
            self.segments[idx].color(leading_seg.seg_color)
        self.head.color(color)

    def increment_score(self, negative: bool = False) -> None:
        self.score += (-1 if self.score != 0 else 0) if negative else 1
        self.on_score_changed()

    def set_score(self, n: int = None) -> None:
        if not n: n = self.last_collision_index
        self.score = n
        self.on_score_changed()

    # ---- Visuals ----
    def initial_plot(self) -> None:
        self.plot_food_from_segments(0, retract_after_expand=True)
        self.uncolor_segments()

    def flash_warning(self, start: int = None, end: int = None) -> None:
        if start is None: start = self.last_collision_index
        seg_colors: list[str] = [c.color()[0] for c in self.segments][start:end]
        segments: list[SnakeSegment] = self.segments[start:end]
        for i in range(6):
            for seg, color in zip(segments, seg_colors):
                seg.color('yellow') if i % 2 == 0 else seg.color(color)
            window.frame_update(pause=0.2)

    def plot_food_from_segments(self, start: int = None, end: int = None, retract_after_expand: bool = False) -> None:
        if start is None: start = self.last_collision_index
        segments: list[SnakeSegment] = self.segments[start:end]
        original_locations: list[tuple[float, float]] = [(seg.xcor(), seg.ycor()) for seg in segments]
        for seg in segments[::-1]:
            if not seg.is_colored:
                seg.hideturtle()
                window.frame_update(pause=0.05)
                continue
            seg.animated_goto(rx:=window.rand_xcor(), ry:=window.rand_ycor())
            food_manager.create_food(rx, ry, seg.seg_color if seg.is_colored else rand_choice(COLORS))
        if retract_after_expand:
            for seg, loc in zip(segments, original_locations):
                seg.animated_goto(*loc)
            return
        self.cut_segments(start, end, interval=0)

    def uncolor_segments(self) -> None:
        for seg in self.segments:
            seg.color('white')
            window.frame_update(pause=0.01)

    def cut_segments(self, start: int = 4, end: int = None, interval: float = 0.08) -> None:
        for seg in self.segments[start:end]:
            seg.hideturtle()
            window.frame_update(interval)
        del self.segments[start:end]


class GamePlayManager:
    """Singleton for the snake game play."""
    def __init__(self, two_players: bool = False):
        window.on_play_pressed = self._mainloop
        self.snake1: Snake | None = None
        self.snake2: Snake | None = None
        if two_players:
            self.snake1 = Snake()
            self.snake1.on_score_changed = self.update_scoreboard
            self.snake2 = Snake(reverse_dir=True)
            self.snake2.on_score_changed = self.update_scoreboard
        else:
            self.snake1 = Snake()
            self.snake1.flash_warning()
            self.snake1.on_score_changed = self.update_scoreboard
        self.setup_input_controls()

        # Scoreboard
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color('white')
        self.update_scoreboard()

        # Pause Play Interaction
        self.game_active: bool = True
        window.onkey(key='space', fun=self.pause_play_pressed)

    def pause_play_pressed(self):
        if self.game_active:
            self.game_active = False
        else:
            self.game_active = True
            self._mainloop()

    def write_to_scoreboard(self, text: str) -> None:
        self.pen.clear()
        self.pen.goto(0, window.center_to_height - 35)
        self.pen.write(text, align="center", font=("System", 24, "normal"))

    def update_scoreboard(self) -> None:
        if not self.snake2:
            global HIGHSCORE
            if self.snake1.score > HIGHSCORE:
                HIGHSCORE = self.snake1.score
            self.write_to_scoreboard(f'Score: {self.snake1.score}     |     Highscore: {HIGHSCORE}')
        else:
            self.write_to_scoreboard(f'1st Player: {self.snake1.score}     |     2nd Player: {self.snake2.score}')

    def setup_input_controls(self) -> None:
        if self.snake1:
            window.onkeypress(key='Up', fun=self.snake1.up)
            window.onkeypress(key='Left', fun=self.snake1.left)
            window.onkeypress(key='Down', fun=self.snake1.down)
            window.onkeypress(key='Right', fun=self.snake1.right)
        if self.snake2:
            window.onkeypress(key='w', fun=self.snake2.up)
            window.onkeypress(key='a', fun=self.snake2.left)
            window.onkeypress(key='s', fun=self.snake2.down)
            window.onkeypress(key='d', fun=self.snake2.right)

    @staticmethod
    def collision_reaction(snake: Snake, entire_snake_reaction: bool = False) -> None:
        if entire_snake_reaction:
            snake.flash_warning(0)
            snake.plot_food_from_segments(4)
            snake.uncolor_segments()
            snake.undo_move()
            snake.set_score(snake.score // 4)
        else:
            snake.flash_warning()
            snake.plot_food_from_segments()
            snake.uncolor_segments()
            snake.undo_move()
            snake.set_score()

    def handle_player_collision(self) -> None:
        snake1_head: Turtle = self.snake1.head
        snake2_head: Turtle = self.snake2.head
        for seg in self.snake1.segments:
            if seg.distance(snake2_head) < 20:
                self.collision_reaction(self.snake2, entire_snake_reaction=True)
                return
        for seg in self.snake2.segments:
            if seg.distance(snake1_head) < 20:
                self.collision_reaction(self.snake1, entire_snake_reaction=True)
                return

    def handle_wall_collision(self, snake: Snake) -> None:
        if WALL_TELEPORT:
            window.teleport_edge_touchers()
        elif window.snake_collided_with_wall(snake):
            self.collision_reaction(snake, entire_snake_reaction=True)

    def handle_self_collision(self, snake: Snake):
        if snake.is_self_collision():
            self.collision_reaction(snake, entire_snake_reaction=False)

    def _mainloop(self) -> None:
        # noinspection PyBroadException
        try:
            if not self.snake2:
                while self.game_active:
                    self.snake1.move()
                    self.handle_self_collision(self.snake1)
                    self.handle_wall_collision(self.snake1)
                    food_manager.handle_food_collisions()
                    window.frame_update()
            else:
                while self.game_active:
                    self.snake1.move()
                    self.snake2.move()
                    self.handle_self_collision(self.snake1)
                    self.handle_self_collision(self.snake2)
                    self.handle_wall_collision(self.snake1)
                    self.handle_wall_collision(self.snake2)
                    self.handle_player_collision()
                    food_manager.handle_food_collisions()
                    window.teleport_edge_touchers()
                    window.frame_update()
        except:  # turtle errors if window is destroyed and loop is still trying to execute turtle commands.
            return

    def start_game(self) -> None:
        self.snake1.initial_plot()
        self._mainloop()
game_play_manager: GamePlayManager = GamePlayManager(two_players=MODE == 2)
game_play_manager.start_game()
window.mainloop()  # this is only active when game is paused.
userdata_file.save()
