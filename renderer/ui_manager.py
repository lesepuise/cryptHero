from datetime import datetime, timedelta

class UIManager():
    def __init__(self):
        self.menu_lines = []
        self.menu_title = 'Controls'
        self.__status_line = ''
        self.__status_timer = datetime.now()
        self.hover_name = ''
        self.popup = None

    def add_menu_line(self, line:tuple):
        self.menu_lines.append(line)
    
    @property
    def status_line(self):
        if (datetime.now() - self.__status_timer) < timedelta(seconds=2):
            return self.__status_line
        else:
            return ''

    @status_line.setter
    def status_line(self, status:str):
        if status:
            self.__status_timer = datetime.now()
            self.__status_line = status
    
    def set_hover_name(self, name):
        self.hover_name = name

    def show_popup(self, name, description, exit_command):
        self.popup = (name, description, exit_command)
    
    def remove_popup(self):
        self.popup = ()