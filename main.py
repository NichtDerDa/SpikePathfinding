import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.graphics import Line, Color, Ellipse, Bezier
from kivy.core.window import Window
from math import sqrt
import math
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from math import sin, cos, radians
from kivy.properties import NumericProperty
import random
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

class LineWidget(Widget):
    def __init__(self, start, stop, color, parent, index, selected, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.stop = stop
        self.index = index
        self.selected = selected
        self.color = color
        self.par = parent
        with self.canvas:
            Color(*color)
            self.line = Line(points=[start[0], start[1], stop[0], stop[1]], width=2)
        self.bind(pos=self.update_line)
        self.update_color()

    def update_line(self, *args):
        self.line.points = [self.start[0], self.start[1], self.stop[0], self.stop[1]]
        self.update_color()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.par.draw:
                self.selected = True

    def update_color(self):
        if self.selected:
            self.canvas.clear()
            with self.canvas:
                Color(0, 1, 0, 1)  # Change color to green when selected
                self.line = Line(points=[self.start[0], self.start[1], self.stop[0], self.stop[1]], width=2)
        else:
            self.canvas.clear()
            with self.canvas:
                Color(*self.color)  # Original color
                self.line = Line(points=[self.start[0], self.start[1], self.stop[0], self.stop[1]], width=2)


class CircleWidget(Widget):
    def __init__(self, start_angle, stop_angle, pos, selected, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.angle1 = start_angle
        self.angle2 = stop_angle
        self.pos = pos
        self.update_canvas()
        self.index = None
        self.selected = selected


    def update_canvas(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(0.5, 0, 0.5, 1)
            center_x, center_y = self.pos
            radius = 50
            if self.angle2 < self.angle1:
                self.angle1, self.angle2 = self.angle2, self.angle1
            start_angle_rad = math.radians(self.angle1)
            stop_angle_rad = math.radians(self.angle2)
            if self.angle2 < self.angle1:
                start_angle_rad, stop_angle_rad = stop_angle_rad, start_angle_rad

            Line(points=[center_x, center_y, center_x + radius * math.cos(start_angle_rad),
                         center_y + radius * math.sin(start_angle_rad)], width=2)

            Line(points=[center_x, center_y, center_x + radius * math.cos(stop_angle_rad),
                         center_y + radius * math.sin(stop_angle_rad)], width=2)

            control_points = self.get_control_points(start_angle_rad, stop_angle_rad)
            Bezier(points=control_points, segments=80, width=6)


    def get_control_points(self, start_angle, stop_angle):
        center_x, center_y = self.pos
        radius = 50
        num_points = 80
        control_points = []

        for i in range(num_points + 1):
            angle = start_angle + (stop_angle - start_angle) * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            control_points.extend([x, y])
        return control_points

class NamePopup(Popup):
    def __init__(self, par, pos, **kwargs):
        super(NamePopup, self).__init__(**kwargs)
        self.title = "Enter name of task"
        self.content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(multiline=False, hint_text='Enter name of task')
        self.content.add_widget(self.name_input)
        self.ok_button = Button(text='OK')
        self.content.add_widget(self.ok_button)
        self.ok_button.bind(on_press=self.on_ok)
        self.par = par
        self.position = pos


    def on_ok(self, instance):
        name = self.name_input.text
        self.par.lines.append(["task", name, self.position])
        self.par.build()
        self.dismiss()

class NamePopup2(Popup):
    def __init__(self, par, pos, **kwargs):
        super(NamePopup2, self).__init__(**kwargs)
        self.title = "Enter name of function"
        self.content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(multiline=False, hint_text='Enter name of function')
        self.content.add_widget(self.name_input)
        self.ok_button = Button(text='OK')
        self.content.add_widget(self.ok_button)
        self.ok_button.bind(on_press=self.on_ok)
        self.par = par
        self.position = pos


    def on_ok(self, instance):
        name = self.name_input.text
        self.par.lines.append(["base", name, self.position])
        self.par.build()
        self.dismiss()

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
''')

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        if self.selected == is_selected:
            return
        self.selected = is_selected
        if is_selected:
            rv.select(index)
        else:
            rv.remove_selection(index)
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    def __init__(self, **kwargs):
        super(SelectableRecycleBoxLayout, self).__init__(**kwargs)
        for child in self.children:
            print(child)
    def set_selected(self):
        print(self.parent)
class RV(RecycleView):
    def __init__(self, par, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.par = par
        self.build()

    def build(self):
        self.data = []
        for line in self.par.lines:
            if line[0] == "line":
                self.data.append({"text": "drive"})
            if line[0] == "turn":
                self.data.append({"text": "turn"})
            if line[0] == "task":
                self.data.append({"text": f"task: {line[1]}"})
    def select(self, index):
        self.par.add_select(index)

    def remove_selection(self, index):
        self.par.remove_selection(index)


class MyPaintWidget(Widget):
    def __init__(self, image, parent, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.im = Image(source=image)
        self.bind(pos=self.update_image_pos_size, size=self.update_image_pos_size)
        self.update_image_pos_size()
        self.add_widget(self.im)
        self.mode = "lines"
        self.start_point = 0
        self.lines = []
        self.wds = []
        self.cur_line = None
        self.current_color = (1, 0, 0, 1)
        self.draw = False
        self.colors = []
        self.last_point = self.pos
        self.par = parent
        self.last_angle = 90
        self.new_angle = -90
        self.circle_eval = False
        self.selected = []
        self.select_var = False
        Clock.schedule_interval(self.build, 1/5)

    def update_image_pos_size(self, *args):
        self.im.pos = self.pos
        self.im.size = self.size
    def clear_selected(self):
        for wd in self.selected:
                self.remove_widget(wd)
                self.lines.remove(wd)
        self.selected = []
        self.build()

    def add_select(self, index):
        self.selected.append(self.lines[index])

    def remove_selection(self, index):
        if self.lines[index] in self.selected:
            self.selected.remove(self.lines[index])

    def on_touch_down(self, touch):
        if not self.select_var:
            if self.mode == "lines":
                if not self.circle_eval:
                    if self.collide_point(touch.pos[0], touch.pos[1]):
                        self.start_point = touch.pos
                        self.draw = True
                        if self.par.last:
                            self.draw = True
                            if self.last_point == None:
                                self.last_point = (0, 0)
            if self.mode == "turns":
                if not self.circle_eval:
                    if self.collide_point(touch.pos[0], touch.pos[1]):
                        self.cur_line = CircleWidget(self.last_angle, self.new_angle, touch.pos, False)
                        self.add_widget(self.cur_line)


    def on_touch_up(self, touch):
        if not self.select_var:
            if self.mode == "lines":
                if not self.circle_eval:
                    if self.draw:
                        if not self.par.last:
                            if self.collide_point(touch.pos[0], touch.pos[1]):
                                self.lines.append(["line", self.start_point, touch.pos, self.current_color, False])
                                if self.cur_line:
                                    self.remove_widget(self.cur_line)
                                self.draw = False
                                self.last_point = touch.pos
                                self.build()
                            else:
                                if self.cur_line:
                                    self.remove_widget(self.cur_line)
                                self.draw = False

                    if self.par.last:
                        if self.draw:
                            if self.collide_point(touch.pos[0], touch.pos[1]):
                                x1, y1 = self.last_point
                                x2, y2 = touch.pos
                                dx = x2- x1
                                dy = y2- y1
                                rads = math.atan2(dy, dx)
                                degs = math.degrees(rads)
                                delta_deg = abs(self.last_angle - degs)
                                if delta_deg > 180:
                                    delta_deg = 360 - delta_deg
                                #print(delta_deg)
                                self.lines.append(["turn", self.last_angle, degs, self.last_point, False])
                                self.last_angle = degs
                                self.lines.append(["line", self.last_point, touch.pos, self.current_color, False])
                                if self.cur_line:
                                    self.remove_widget(self.cur_line)
                                self.build()
                                self.draw = False
                                self.last_point = touch.pos
                            else:
                                if self.cur_line:
                                    self.remove_widget(self.cur_line)
                                self.draw = False

            if self.mode == "turns":
                if not self.circle_eval:
                    if self.collide_point(touch.pos[0], touch.pos[1]):
                        self.circle_eval = True
                        self.par.build_circle_controls()
                        self.last_point = touch.pos
                    else:
                        if self.cur_line:
                            self.remove_widget(self.cur_line)
                            self.cur_line = None

            if self.mode == "task":
                if not self.circle_eval:
                    if self.collide_point(touch.pos[0], touch.pos[1]):
                        if self.par.last:
                            if self.last_point != None:
                                popup = NamePopup(self, self.last_point)
                                popup.open()
                            else:
                                popup = NamePopup(self, (0,0))
                                popup.open()
                        else:
                            popup = NamePopup(self, touch.pos)
                            popup.open()
                    self.build()

            if self.mode == "new_function":
                if not self.circle_eval:
                    if self.collide_point(touch.pos[0], touch.pos[1]):
                        if self.par.last:
                            if self.last_point != None:
                                popup = NamePopup2(self, self.last_point)
                                popup.open()
                            else:
                                popup = NamePopup2(self, (0, 0))
                                popup.open()
                        else:
                            popup = NamePopup2(self, touch.pos)
                            popup.open()
                    self.build()
        self.build()


    def on_touch_move(self, touch):
        if not self.select_var:
            if self.mode == "lines":
                if not self.circle_eval:
                    if self.draw:
                        if self.cur_line:
                            self.remove_widget(self.cur_line)
                        self.cur_line = LineWidget(self.start_point, touch.pos, self.current_color, self, 0, False)
                        self.add_widget(self.cur_line)
                    if self.par.last:
                        if self.cur_line:
                            self.remove_widget(self.cur_line)
                        self.cur_line = LineWidget(self.last_point, touch.pos, self.current_color, self, 0, False)
                        self.add_widget(self.cur_line)
            if self.mode == "turns":
                if not self.circle_eval:
                    if self.cur_line:
                        self.remove_widget(self.cur_line)
                    self.cur_line = CircleWidget(self.last_angle, self.new_angle, touch.pos, False)
                    self.add_widget(self.cur_line)


    def set_drawing_mode(self, mode):
        self.mode = mode

    def set_color(self, color):
        self.current_color = color

    def build(self, instance=False):
        for wd in self.wds:
            self.remove_widget(wd)
        self.wds = []
        for i, line in enumerate(self.lines):
            if line in self.selected:
                if line[0] == "line":
                    new_line = LineWidget(line[1], line[2], line[3], self, i, True)
                    self.wds.append(new_line)
                    self.add_widget(new_line)
                if line[0] == "turn":
                    circle = CircleWidget(line[1], line[2], line[3], True)
                    self.wds.append(circle)
                    self.add_widget(circle)
                if line[0] == "task":
                    label = Label(text=line[1], pos=line[2])
                    self.wds.append(label)
                    self.add_widget(label)
                if line[0] == "base":
                    label = Label(text=line[1], pos=line[2])
                    self.wds.append(label)
                    self.add_widget(label)
            else:
                if line[0] == "line":
                    new_line = LineWidget(line[1], line[2], line[3], self, i, False)
                    self.wds.append(new_line)
                    self.add_widget(new_line)
                if line[0] == "turn":
                    circle = CircleWidget(line[1], line[2], line[3], False)
                    self.wds.append(circle)
                    self.add_widget(circle)
                if line[0] == "task":
                    label = Label(text=line[1], pos=line[2])
                    self.wds.append(label)
                    self.add_widget(label)
                if line[0] == "base":
                    label = Label(text=line[1], pos=line[2])
                    self.wds.append(label)
                    self.add_widget(label)
        self.RV.build()



    def reloadCircle(self):
        self.remove_widget(self.cur_line)
        self.cur_line = CircleWidget(self.last_angle, self.new_angle, self.last_point, False)
        self.add_widget(self.cur_line)

    def add_turn(self):
        self.lines.append(["turn", self.last_angle, self.new_angle, self.last_point])
        self.cur_line = None

    def set_RV(self, rv):
        self.RV = rv

    def set_select(self, sel):
        self.select_var = sel

    def move_selected_up(self):
        for wd in self.selected:
            index = self.lines.index(wd)
            if index != 0:
                self.lines[index - 1], self.lines[index] = self.lines[index], self.lines[index - 1]

    def move_selected_down(self):
        for wd in self.selected:
            index = self.lines.index(wd)
            print(index)
            if index != len(self.lines)-1:
                self.lines[index + 1], self.lines[index] = self.lines[index], self.lines[index + 1]


class MyApp(App):
    def build(self):
        # Create the main layout
        self.main_layout = BoxLayout(orientation='vertical')

        # Create a horizontal layout for buttons
        button_layout = BoxLayout(size_hint_y=None, height=50)
        self.active = "lines"
        self.activities = ["lines", "new_function", "turns", "task"]
        self.last = True
        self.select = False

        # Add some buttons to the button layout
        open_button = Button(text='Open Image')
        close_button = Button(text='Close')
        save_button = Button(text='Save Lines')
        self.last_button = Button(text="Last = True")
        self.select_button = Button(text="select = False")

        open_button.bind(on_release=self.show_file_chooser)
        close_button.bind(on_release=self.stop)
        save_button.bind(on_release=self.save_lines_to_file)
        self.last_button.bind(on_press=self.change_last)
        self.select_button.bind(on_press=self.change_select)

        button_layout.add_widget(open_button)
        button_layout.add_widget(close_button)
        button_layout.add_widget(save_button)
        button_layout.add_widget(self.last_button)
        button_layout.add_widget(self.select_button)

        self.delete_button = Button(text="Delete Selected")
        self.delete_button.bind(on_release=self.delete_selected)
        button_layout.add_widget(self.delete_button)

        # Add the button layout to the main layout
        self.main_layout.add_widget(button_layout)

        self.top_layout = BoxLayout(size_hint_y=None, height=50)
        self.build_top_buttons()
        self.main_layout.add_widget(self.top_layout)

        self.image = MyPaintWidget("image.png", self, size_hint_y=0.8, pos_hint={"x": 0.0, "y":1.0})
        self.main_layout.add_widget(self.image)
        # Add the RV to the image layout
        self.RV = RV(self.image, size_hint_y=0.2)
        self.main_layout.add_widget(self.RV)

        self.image.set_RV(self.RV)

        return self.main_layout

    def delete_selected(self, instance):
        self.image.clear_selected()
        self.RV.build()
    def change_last(self, instance):
        if self.last:
            self.last = False
            self.last_button.text = "Last = False"
        else:
            self.last = True
            self.last_button.text = "Last = True"

    def change_select(self, instance):
        if self.select:
            self.select = False
            self.select_button.text = "Select = False"
            self.image.set_select(False)
        else:
            self.select = True
            self.select_button.text = "Select = True"
            self.image.set_select(True)

    def move_selected_up(self, instance):
        self.image.move_selected_up()

    def move_selected_down(self, instance):
        self.image.move_selected_down()

    def build_top_buttons(self):
        self.top_layout.clear_widgets()
        left_button = Button(text="<")
        middle_label = Label(text=self.active)
        right_button = Button(text=">")
        move_selected_up = Button(text="Up")
        move_selected_down = Button(text="Down")

        left_button.bind(on_press=self.button_left)
        right_button.bind(on_press=self.button_right)
        move_selected_up.bind(on_press=self.move_selected_up)
        move_selected_down.bind(on_press=self.move_selected_down)

        self.top_layout.add_widget(left_button)
        self.top_layout.add_widget(middle_label)
        self.top_layout.add_widget(right_button)
        self.top_layout.add_widget(move_selected_up)
        self.top_layout.add_widget(move_selected_down)

    def button_right(self, instance):
        ind = self.activities.index(self.active)
        if ind + 1 == len(self.activities):
            new_ind = 0
        else:
            new_ind = ind + 1
        self.active = self.activities[new_ind]
        self.image.set_drawing_mode(self.active)
        self.build_top_buttons()

    def button_left(self, instance):
        ind = self.activities.index(self.active)
        if ind == 0:
            new_ind = len(self.activities) - 1
        else:
            new_ind = ind - 1
        self.active = self.activities[new_ind]
        self.image.set_drawing_mode(self.active)
        self.build_top_buttons()

    def show_file_chooser(self, instance):
        # Create a FileChooser to select an image
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        # Create a Popup for the FileChooser
        popup = Popup(title='Choose an Image', content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=self.load_image)
        popup.open()

    def load_image(self, filechooser, selection, touch):
        if selection:
            self.image.im.source = selection[0]
            self.image.im.reload()

        #filechooser._popup.dismiss()

    def calc_degrees(self, deg1, deg2):
        delta_deg = abs(deg1 - deg2)

        if delta_deg > 180:
            delta_deg = 360 - delta_deg
        return delta_deg

    def save_lines_to_file(self, instance):
        real_width_mm = 2000
        image_width_px = self.image.im.size[0] * self.image.im.parent.size[0] / self.image.im.parent.size_hint[0]
        pixel_per_mm = image_width_px / real_width_mm
        data = """
from spike import PrimeHub, Motor, MotorPair
from hub import battery
import hub as hub2
import sys
import time

hub = PrimeHub()
lastAngle = 0
oldAngle = 0
gyroValue = 0
runSmall = True
run_generator = True 
cancel = False
activeMain = False

def write_display(funktionen, index):
    for count, _ in enumerate(funktionen, start=1):
        x, y = divmod(count - 1, 5)
        light = 100 if count == index else 75
        hub.light_matrix.set_pixel(x, y, light)

def breakFunction(args):
    global cancel, activeMain
    if not activeMain:
        cancel = True

def read_battery():
    voltage = battery.voltage()
    status = "battery voltage is too low: " if voltage < 8000 else "battery voltage: "
    print(f"{status}{voltage}>>>> please charge robot <<<<" if voltage < 8000 else "")

def getDrivenDistance(data):
    left_degrees = abs(data.leftMotor.get_degrees_counted() - data.left_Startvalue)
    right_degrees = abs(data.rightMotor.get_degrees_counted() - data.right_Startvalue)
    print(f"{left_degrees} .:. {right_degrees}")
    return (left_degrees + right_degrees) / 2

def driveMotor(rotations, speed, port):
    global runSmall, run_generator, cancel
    if cancel:
        runSmall = run_generator = False
    while runSmall:
        smallMotor = Motor(port)
        smallMotor.set_degrees_counted(0)
        while abs(smallMotor.get_degrees_counted()) <= abs(rotations) * 360 and not cancel:
            smallMotor.start_at_power(speed)
            yield
        smallMotor.stop()
        runSmall = run_generator = False
    yield

def getGyroValue():
    global lastAngle, oldAngle, gyroValue
    angle = hub.motion_sensor.get_yaw_angle()
    if angle != lastAngle:
        oldAngle = lastAngle
    lastAngle = angle
    if angle in [179, -180] and oldAngle == angle - 1:
        hub2.motion.yaw_pitch_roll(0)
        gyroValue += 179 if angle == 179 else -180
    return gyroValue + angle

class DriveBase:
    def __init__(self, hub, leftMotor, rightMotor):
        self.hub = hub
        self.leftMotor = Motor(leftMotor)
        self.rightMotor = Motor(rightMotor)
        self.movement_motors = MotorPair(leftMotor, rightMotor)

    def drive(self, distance, speed, generator=None):
        global run_generator, runSmall, cancel
        if cancel:
            return
        if generator is None:
            run_generator = False
        self.left_Startvalue = self.leftMotor.get_degrees_counted()
        self.right_Startvalue = self.rightMotor.get_degrees_counted()
        rotateDistance = (distance / 17.6) * 360
        drivenDistance = getDrivenDistance(self)
        change, old_change, integral, steeringSum = 0, 0, 0, 0
        invert = -1 if speed > 0 else 1
        hub.motion_sensor.reset_yaw_angle()
        while drivenDistance < rotateDistance and not cancel:
            if run_generator:
                next(generator)
            oldDrivenDistance = drivenDistance
            drivenDistance = getDrivenDistance(self)
            change = getGyroValue()
            steering = max(-50, min(change + integral + steeringSum * 0.02 + (change - old_change), 50))
            print(f"steering: {steering} gyro: {change} integral: {integral}")
            steeringSum += change
            integral += change - old_change
            old_change = change
            self.movement_motors.start_at_power(int(speed), invert * int(steering))
        self.movement_motors.stop()
        run_generator = runSmall = True

    def turn(self, angle, speed):
        global cancel
        if cancel:
            return
        speed = abs(speed)
        steering = 1 if angle > 0 else -2
        angle *= 2400 / 2443
        target_angle = getGyroValue() + angle
        while abs(getGyroValue() - target_angle) > 1 and not cancel:
            current_angle = getGyroValue()
            angle_left = target_angle - current_angle
            current_speed = min(speed, abs(angle_left) + 5)
            self.movement_motors.start_tank_at_power(int(current_speed) * steering, -int(current_speed) * steering)
        self.movement_motors.stop()

db = DriveBase(hub, 'A', 'B')
"""
        funcs = []
        with open("lines.py", "w") as file:
            file.write(data)
            for i, line in enumerate(self.image.lines):
                if i == 0:
                    if line[0] != "base":
                        funcs.append("start_function")
                if line[0] == "base":
                    funcs.append(line[1])
            file.write(f"funktionen = ['{funcs[0]}'")
            data = data + f"funktionen = ['{funcs[0]}'"
            for i, f in enumerate(funcs):
                if i == 0:
                    pass
                else:
                    file.write(f", '{f}'")
                    data = data + f", '{f}'"
            file.write("]\n")
            data = data + "]\n"

            for i, line in enumerate(self.image.lines):
                if i == 0:
                    if line[0] != "base":
                        file.write(f"def start_function():\n")
                        data = data + f"def start_function():\n"
                if line[0] == "line":
                    type_, start, end, color, select = line
                    distance_px = sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    distance_mm = distance_px / pixel_per_mm
                    distance_mm *= 100
                    file.write(f"   db.drive({distance_mm:.2f}, 1100)\n")
                    data = data + f"    db.drive({distance_mm:.2f}, 1100)\n"
                if line[0] == "turn":
                    type_, angle1, angle2, pos, select = line
                    turn = self.calc_degrees(angle1, angle2)
                    file.write(f"   db.turn({turn:.2f}, 1100)\n")
                    data = data + f"    db.turn({turn:.2f}, 1100)\n"
                if line[0] == "task":
                    type_, text, pos = line
                    file.write(f"   # Task: {text}\n")
                    data = data + f"    # Task: {text}\n"
                if line[0] == "base":
                    type_, text, pos = line
                    file.write(f"def {text}():\n")
                    data = data + f"def {text}():\n"
            file.write("""
hub2.button.right.callback(breakFunction)

read_battery()
index = 1
write_display(funktionen, index)

while True:
    activeMain = True
    if hub.left_button.is_pressed():
        index = len(funktionen) if index == 1 else index - 1
        print(funktionen[index - 1])
        write_display(funktionen, index)
        time.sleep(0.15)
    if hub.right_button.is_pressed():
        index = 1 if index == len(funktionen) else index + 1
        print(funktionen[index - 1])
        write_display(funktionen, index)
        time.sleep(0.15)
    
read_battery()
sys.exit("ended program successfully")""")
        data = data + """
hub2.button.right.callback(breakFunction)

read_battery()
index = 1
write_display(funktionen, index)

while True:
    activeMain = True
    if hub.left_button.is_pressed():
        index = len(funktionen) if index == 1 else index - 1
        print(funktionen[index - 1])
        write_display(funktionen, index)
        time.sleep(0.15)
    if hub.right_button.is_pressed():
        index = 1 if index == len(funktionen) else index + 1
        print(funktionen[index - 1])
        write_display(funktionen, index)
        time.sleep(0.15)
    
read_battery()
sys.exit("ended program successfully")
        """
        Clipboard.copy(data=data)

    def build_circle_controls(self):
        self.controls_layout = BoxLayout(size_hint_y=None, height=50)
        self.start_angle_slider = Slider(min=0, max=360, value=self.image.last_angle)
        self.stop_angle_slider = Slider(min=0, max=360, value=self.image.new_angle)
        self.finish_button = Button(text="Finish Circle")

        self.start_angle_slider.bind(value=self.update_start_angle)
        self.stop_angle_slider.bind(value=self.update_stop_angle)
        self.finish_button.bind(on_release=self.finish_circle)

        self.controls_layout.add_widget(self.start_angle_slider)
        self.controls_layout.add_widget(self.stop_angle_slider)
        self.controls_layout.add_widget(self.finish_button)

        self.main_layout.add_widget(self.controls_layout)

    def update_start_angle(self, instance, value):
        self.image.last_angle = value
        self.image.cur_line.angle1 = value
        self.image.cur_line.update_canvas()
        self.image.reloadCircle()

    def update_stop_angle(self, instance, value):
        self.image.new_angle = value
        self.image.cur_line.angle2 = value
        self.image.cur_line.update_canvas()
        self.image.reloadCircle()

    def finish_circle(self, instance):
        self.image.circle_eval = False
        self.image.add_turn()
        self.image.last_angle = self.image.new_angle
        self.main_layout.remove_widget(self.controls_layout)

if __name__ == '__main__':
    MyApp().run()
