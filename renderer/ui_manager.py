import tcod
from datetime import datetime, timedelta
from entity.player import Player

class UIManager():
    def __init__(self, player, width, height, order='F'):
        self.menu_lines = []
        self.logs = []
        self.menu_title = 'Controls'
        self.__status_line = ''
        self.__status_timer = datetime.now()
        self.hover_name = ''
        self.popup = None
        self.player = player
        self.console = tcod.console.Console(width, height, order)
        tcod.console_load_xp(self.console, 'levels/ui.xp')

    def add_menu_line(self, line:tuple):
        self.menu_lines.append(line)
    
    def log(self, log):
        self.logs.insert(0, log)
    
    def print_ui(self):
        self.render_menu()
        self.render_stats()
        self.render_logs()
    
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

    def render_menu(self):
        # Draw borders
        line_idx = 2
        for line in self.menu_lines:
            self.console.print(61, line_idx, line[0], tcod.yellow)
            self.console.print(len(line[0]) + 61, line_idx, ':', tcod.grey)
            self.console.print(len(line[0]) + 63, line_idx, line[1], tcod.white)
            line_idx += 1

    def render_stats(self):
        stats = [
            str(self.player.entity_level).ljust(9, ' '),
            '{}/{}'.format(self.player.hp, self.player.max_hp).ljust(9, ' '),
            self.player.get_weapon().name.ljust(9, ' '),
            self.player.get_armor().name.ljust(9, ' '),
            'Empty',
            'Empty',
            'Empty',
        ]
        line_idx = 63
        for stat in stats:
            self.console.print(70, line_idx, stat, tcod.cyan)
            line_idx += 2

    def render_logs(self):
        self.console.print_box(1, 63, 57, 16, '\n'.join(self.logs))