import serial
from kivy.core.window import Window
import kivy
import os
import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config
Config.set('graphics', 'resizable', 1)


Window.size = (1200, 720)

device = serial.Serial()
# Window.size = (1200, 720)
# Window.fullscreen = 'auto'
dataTestPlan = {
    "name": "",
    "points": [
        {
            "name_test": "Тест эффективности 1",
            "pressure": 0,
            "rpm": 0,
            "flow": 100,
            "delta": 10,
            "back_flow_min": 100
        }
    ]
}
currentTest = 0

comPort = ""
device_data = {
    "flow": 40,
    "overflow": 30,
    "rpm": 1000,
    "pressure": 200
}


class Menu(GridLayout):
    def comPortSelector(self):
        device.close()
        comPort = SelectCOM()
        comPort.serial_ports()
        comPort.bind(on_dismiss=self.com_connect)
        comPort.open()

    def open(self):
        pops = PopupSelectFile()
        pops.init_data()
        pops.bind(on_dismiss=self.new_data)
        pops.open()

    def com_connect(self, instanse):
        self.comButton.text = comPort
        device.close()

    def new_data(self, instanse):
        global currentTest
        global dataTestPlan
        if (instanse.path):
            f = open(instanse.path, "r", encoding="utf-8")
            dataTestPlan = json.loads(f.read())
            f.close()

            self.name_device = dataTestPlan.get('name')
            self.test_name = dataTestPlan.get(
                'points')[currentTest].get('name_test')


    def changeTest(self, instanse):
        global currentTest
        global dataTestPlan
        if(instanse.text == 'Previous screen'):
            if (currentTest > 0):
                currentTest -= 1
                self.test_name = dataTestPlan.get(
                    'points')[currentTest].get('name_test')
        if(instanse.text == 'Next screen'):
            if (currentTest < len(dataTestPlan.get('points'))-1):
                currentTest += 1
                self.test_name = dataTestPlan.get(
                    'points')[currentTest].get('name_test')


class PopupKeyboard(Popup):
    pntnum = '100'
    type = ''

    def init_data(self, data, type):
        self.type = type
        self.pntnum = data
        self.lebel.text = self.pntnum

    def update_lebel(self):
        self.lebel.text = self.pntnum

    def btn_num(self, num):
        if self.pntnum == '100':
            self.pntnum = ''
        self.pntnum += str(num.text)
        self.update_lebel()

    def ok(self, *args):
        self.dismiss()

    def ce(self):
        self.pntnum = ''
        self.lebel.text = self.pntnum


class PopupSelectFile(Popup):
    path = ''

    def init_data(self):
        self.filechooser.path = (os.getcwdb() + b'/tpl').decode("utf-8")

    def load(self, path, selection):
        if (selection):
            self.path = selection[0]
            self.dismiss()


class LeftPanel(GridLayout):
    # ФУНКЦИЮ __init__ НЕ ТРОГАТЬ!
    def __init__(self, **kwargs):
        self._cols = self._rows = None
        super(GridLayout, self).__init__(**kwargs)
        fbind = self.fbind
        update = self._trigger_layout
        fbind('col_default_width', update)
        fbind('row_default_height', update)
        fbind('col_force_default', update)
        fbind('row_force_default', update)
        fbind('cols', update)
        fbind('rows', update)
        fbind('parent', update)
        fbind('spacing', update)
        fbind('padding', update)
        fbind('children', update)
        fbind('size', update)
        fbind('pos', update)
        fbind('orientation', update)

        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        global currentTest
        global dataTestPlan
        global device_data
        # print(serial_ports())
        
        self.current_motor_speed = str(device_data['rpm'])
        self.current_bar = str(device_data['pressure'])

        self.set_motor_speed = str(dataTestPlan.get('points')[
                                   currentTest].get('rpm'))
        self.set_bar = str(dataTestPlan.get('points')[
                           currentTest].get('pressure'))

        global comPort

        if comPort is not "":
            if device.is_open:
                device.write(bytes(self.set_motor_speed + ';' + self.set_bar + "\n", 'ascii'))
            else:
                device.baudrate = 9600
                device.port = comPort
                device.open()
        

    def openKeyboard(self, type):
        pops = PopupKeyboard()
        if (type == "speed"):
            pops.init_data(str(dataTestPlan.get('points')[
                           currentTest].get('rpm')), type)
        if (type == "pressure"):
            pops.init_data(str(dataTestPlan.get('points')[
                           currentTest].get('pressure')), type)
        pops.bind(on_dismiss=self.changeValueOnKeyboard)
        pops.open()

    def changeValueOnKeyboard(self, instance):
        global dataTestPlan
        global currentTest

        if (instance.type == "speed"):
            dataTestPlan['points'][currentTest]['rpm'] = int(
                instance.lebel.text)
        if (instance.type == "pressure"):
            dataTestPlan['points'][currentTest]['pressure'] = int(
                instance.lebel.text)

    def changeValue(self, type, value):
        global dataTestPlan
        global currentTest

        if (type == "speed"):
            dataTestPlan['points'][currentTest]['rpm'] += int(value)
        if (type == "pressure"):
            dataTestPlan['points'][currentTest]['pressure'] += int(value)

class RightPanel(GridLayout):
    # ФУНКЦИЮ __init__ НЕ ТРОГАТЬ!
    def __init__(self, **kwargs):
        self._cols = self._rows = None
        super(GridLayout, self).__init__(**kwargs)
        fbind = self.fbind
        update = self._trigger_layout
        fbind('col_default_width', update)
        fbind('row_default_height', update)
        fbind('col_force_default', update)
        fbind('row_force_default', update)
        fbind('cols', update)
        fbind('rows', update)
        fbind('parent', update)
        fbind('spacing', update)
        fbind('padding', update)
        fbind('children', update)
        fbind('size', update)
        fbind('pos', update)
        fbind('orientation', update)

        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        global currentTest
        global dataTestPlan
        global device_data

        self.flow.flow = dataTestPlan.get('points')[currentTest].get('flow')
        self.flow.delta = dataTestPlan.get('points')[currentTest].get('delta')
        self.flow.current_flow = device_data['flow']

        self.overflow.flow = dataTestPlan.get('points')[currentTest].get('back_flow_min')
        self.overflow.current_flow = device_data['overflow']
        # print(serial_ports())
        
        # self.current_motor_speed = str(device_data['rpm'])
        # self.current_bar = str(device_data['pressure'])

        # self.set_motor_speed = str(dataTestPlan.get('points')[
        #                            currentTest].get('rpm'))
        # self.set_bar = str(dataTestPlan.get('points')[
        #                    currentTest].get('pressure'))

class PumpScreen(Screen):
    pass


class SelectCOM(Popup):
    def serial_ports(self):
        ports = ['COM%s' % (i + 1) for i in range(256)]

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        for port in result:
            btn = Button(text='%s' % port, size_hint_y=None, height=44)
            btn.bind(on_press=self.select)
            self.deviceList.add_widget(btn)
        return result

    def select(self, instanse):
        global comPort 
        comPort = instanse.text
        self.dismiss()


class ViewsApp(App):
    def build(self):
        screens = ScreenManager()
        screens.add_widget(PumpScreen(name='pump'))


        Clock.schedule_interval(self.update, 0.5)
        return screens

    def update(self, dt):
        global device_data
        global comPort

        if comPort is not "":
            if device.is_open:
                if type(device.readline().decode('ascii')):

                    data_from_device = json.loads(device.readline().decode('ascii'))
                    
                    device_data['flow'] = data_from_device.get('flow')
                    device_data['overflow'] = data_from_device.get('overflow')
                    device_data['rpm']= data_from_device.get('rpm')
                    device_data['pressure'] = data_from_device.get('pressure')
            else:
                device.baudrate = 9600
                device.port = comPort
                device.open()

if __name__ == "__main__":
    ViewsApp().run()
