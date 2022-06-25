# BombSquadDetails

# You can change the code but please don't share the changed code

# If you have a problem, you can contact me here: Discord OnurV2#7194
# YouTube: OnurV2

# Made by OnurV2

# ba_meta require api 7
import os
import ssl
import time
import json
import math
import shutil
import threading
import urllib.error
import urllib.request
from datetime import datetime
from _thread import start_new_thread

from typing import TYPE_CHECKING, Sequence, Optional, cast

import ba, _ba

from bastd.ui.settings.allsettings import AllSettingsWindow
from bastd.ui.settings.advanced import AdvancedSettingsWindow
from bastd.ui.settings.plugins import PluginSettingsWindow

from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.account.settings import AccountSettingsWindow
from bastd.ui.gather import GatherWindow
from bastd.ui.party import PartyWindow
from bastd.ui.onscreenkeyboard import OnScreenKeyboardWindow

from bastd.ui.confirm import ConfirmWindow
from bastd.ui.fileselector import FileSelectorWindow
from bastd.ui.popup import PopupMenu, PopupMenuWindow
from bastd.ui.account import show_sign_in_prompt
from bastd.ui.tabs import TabRow

from bastd.actor.playerspaz import PlayerSpaz

_ba.set_party_icon_always_visible(True)
filter_value = ''
gather_window_detected = False
show_mainmenu = False
in_server = False

platform = ba.app.platform
config = ba.app.config

plugin_path = ba.app.python_directory_user

main_path = plugin_path + '/BombSquadDetailsFolder/'
if not os.path.exists(main_path):
    os.mkdir(main_path)

default_config = {'Leave The Server Directly': False,
                  'End The Game Directly': False,
                  'End The Replay Directly': False,
                  'Exit The Game Directly': False,
                  'Show Reconnect Button': True,
                  'Show The Details Button': True,
                  'Show Exit Game Button': True,
                  'Show Gather Button': True,
                  'In-game Buttons On The Left': False,
                  'Show Quick Language Button': True,
                  'Show Quick Language Button In Main Menu': True,
                  'Language Order Is 1': True,
                  'Language 1': _ba.app.config.get('Lang', None),
                  'Language 2': 'English',
                  'Check For Updates': False,
                  'Copy Message Directly': False,
                  'Open Link Directly': False,
                  'Share Ping In Chat': False,
                  'Ping Command': '!ping',
                  'Ping Message': 'Ping: !',
                  'Show Ping Button': True,
                  'Reconnect Server Directly': False,
                  'Hide In-game Messages': False,
                  'Mute Chat': False,
                  'Spark Particles': False,
                  'Ice Particles': False,
                  'Slime Particles': False,
                  'Sweat Particles': False,
                  'Save History': False}
for key in default_config:
    if not key in config:
        config[key] = default_config[key]

class DetailSettingsManagerWindow(ba.Window):
    def __init__(self, transition, custom_tab):
        global current_tab
        self._uiscale = uiscale = ba.app.ui.uiscale
        self._width = width = (1150 if uiscale is ba.UIScale.SMALL else
            1100 if uiscale is ba.UIScale.MEDIUM else 1050)
        self._height = height = (700 if uiscale is ba.UIScale.SMALL else
            790 if uiscale is ba.UIScale.MEDIUM else 790)
        self._extra = extra = 300 if uiscale is ba.UIScale.SMALL else 0
        self._main_scale = 1.4 if self._uiscale is ba.UIScale.MEDIUM else 1.35

        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.19 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.80),
                         transition=transition))

        self._back_button = ba.buttonwidget(
            parent=self._root_widget,
            label='',
            position=(90+self._extra/100, height-85-extra/5),
            size=(50, 50),
            scale=1.3,
            on_activate_call=self._back,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

        tabdefs = [('main_tab', 'Settings'),
                   ('pw_tab', 'Party Window'),
                   ('effects_tab', 'Effects')]

        self._tab_row = TabRow(self._root_widget,
                               tabdefs,
                               pos=(width-width/1.34, height-155-extra/5),
                               size=(width-width/2.01, 50),
                               on_select_call=ba.Call(self._set_tab, False))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         scale=1.5,
                                         color=(0.83, 1, 0))

        if not custom_tab:
            try: self._set_tab(tab_id=current_tab, road_is_open=True)
            except Exception: self._set_tab(tab_id='main_tab', road_is_open=True)
        else:
            self._set_tab(tab_id='pw_tab', road_is_open=True)

    def _set_tab(self, road_is_open, tab_id):
        global current_tab
        try:
            if not road_is_open:
                if tab_id == current_tab:
                    return
        except Exception: pass

        self._tab_row.update_appearance(tab_id)
        current_tab = tab_id

        try: self._scrollwidget.delete()
        except Exception: pass

        if tab_id == 'main_tab':
            _ba.set_party_icon_always_visible(True)
            ba.textwidget(edit=self._title_text,
                          text='Settings',
                          position=(self._width-self._width/1.82+self._extra/35,
                            self._height/1.085-self._extra/5))

            self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                                 position=(100,100),
                                                 size=(self._width-180-self._extra/18,
                                                    self._height-250-self._extra/5),
                                                 highlight=False)
            self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                                 selection_loops_to_parent=True)

            language_1 = config['Language 1']
            language_2 = config['Language 2']

            self._ms_title_text(text='Confirmation Preferences', first_title=True)
            self._ms_checkboxwidget(text='Don\'t ask when leaving server', cfg_name='Leave The Server Directly', must_restart=False)
            self._ms_checkboxwidget(text='Don\'t ask when ending the game', cfg_name='End The Game Directly', must_restart=False)
            self._ms_checkboxwidget(text='Don\'t ask when ending the replay', cfg_name='End The Replay Directly', must_restart=False)
            self._ms_checkboxwidget(text='Don\'t ask when exiting the game', cfg_name='Exit The Game Directly', must_restart=False)
            self._ms_checkboxwidget(text='Don\'t ask when reconnecting to server', cfg_name='Reconnect Server Directly', must_restart=False)

            self._ms_title_text(text='User Preferences', first_title=False)
            self._ms_checkboxwidget(text='Show reconnect button in in-game menu', cfg_name='Show Reconnect Button', must_restart=False)
            self._ms_checkboxwidget(text='Show the details button in in-game menu', cfg_name='Show The Details Button', must_restart=False)
            self._ms_checkboxwidget(text='Show exit game button in in-game menu', cfg_name='Show Exit Game Button', must_restart=False)
            self._ms_checkboxwidget(text='Show gather button in in-game menu', cfg_name='Show Gather Button', must_restart=False)
            self._ms_checkboxwidget(text='In-game buttons are on the left', cfg_name='In-game Buttons On The Left', must_restart=False)

            self._ms_title_text(text='Quick Language Settings', first_title=False)
            self._ms_checkboxwidget(text='Show quick language button in in-game menu', cfg_name='Show Quick Language Button', must_restart=False)
            self._ms_checkboxwidget(text='Show quick language button in main menu', cfg_name='Show Quick Language Button In Main Menu', must_restart=False)

            languages = _ba.app.lang.available_languages

            PopupMenu(parent=self._subcontainer,
                      position=(0, 0),
                      autoselect=False,
                      on_value_change_call=ba.Call(self._set_language, 'Language 1'),
                      choices=languages,
                      button_size=(275, 75),
                      current_choice=language_1)

            PopupMenu(parent=self._subcontainer,
                      position=(0, 0),
                      autoselect=False,
                      on_value_change_call=ba.Call(self._set_language, 'Language 2'),
                      choices=languages,
                      button_size=(275, 75),
                      current_choice=language_2)

            if platform == 'windows' or platform == 'linux' or platform == 'mac':
                self._ms_title_text(text='Check BombSquad Version', first_title=False)
                ba.checkboxwidget(parent=self._subcontainer,
                                  text='Check for updates when the game starts (can affect boot time)',
                                  size=(760, 47),
                                  value=config['Check For Updates'],
                                  on_value_change_call=ba.Call(change_value, 'Check For Updates', False),
                                  scale=(1.2 if self._uiscale is ba.UIScale.SMALL else
                                    1.155 if self._uiscale is ba.UIScale.MEDIUM else 1.11))
                ba.buttonwidget(parent=self._subcontainer,
                                label='Check for BombSquad updates',
                                size=(350,90),
                                on_activate_call=self._check_new_bs_version)
                ba.buttonwidget(parent=self._subcontainer,
                                label='BombSquad builds',
                                size=(350,90),
                                on_activate_call=confirm_show_bombsquad_builds)
        elif tab_id == 'pw_tab':
            _ba.set_party_icon_always_visible(False)
            ba.textwidget(edit=self._title_text,
                          text='Party Window',
                          position=(self._width-self._width/1.697+self._extra/27,
                            self._height/1.085-self._extra/5))

            self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                                 position=(100,100),
                                                 size=(self._width-180-self._extra/18,
                                                    self._height-250-self._extra/5),
                                                 highlight=False)
            self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                                 selection_loops_to_parent=True)

            self._ms_title_text(text='Main Settings', first_title=True)
            self._ms_checkboxwidget(text='Don\'t ask when copying messages', cfg_name='Copy Message Directly', must_restart=False)
            self._ms_checkboxwidget(text='Don\'t ask when opening links', cfg_name='Open Link Directly', must_restart=False)
            self._ms_checkboxwidget(text='Share my ping in chat', cfg_name='Share Ping In Chat', must_restart=False)
            self._ms_checkboxwidget(text='Use ping button to show ping', cfg_name='Show Ping Button', must_restart=False)

            self._ms_title_text(text='Commands', first_title=False)
            self._ms_textwidget(text=config["Ping Command"] + ': Shows your ping')
            self._ms_textwidget(text='!ip: Writes the ip of the server in the text field')
            self._ms_textwidget(text='!copyip: Copies the server\'s ip')
            self._ms_textwidget(text='!pws: Opens this window')
            self._ms_textwidget(text='!dsw: Opens the detail settings window')

            self._ms_title_text(text='Info', first_title=False)
            self._ms_textwidget(text='Your ping command: ' + config['Ping Command'])
            self._ms_textwidget(text='Your ping message: ' + config['Ping Message'])

            self._ms_title_text(text='How to set ping command', first_title=False)
            self._ms_textwidget(text='Type in the party window:')
            self._ms_textwidget(text='!set ping command Example')

            self._ms_title_text(text='How to set ping message (! = Your ping)', first_title=False)
            self._ms_textwidget(text='Type in the party window:')
            self._ms_textwidget(text='!set ping message My Sample Ping: !')
        elif tab_id == 'effects_tab':
            _ba.set_party_icon_always_visible(True)
            ba.textwidget(edit=self._title_text,
                          text='Effects',
                          position=(self._width-self._width/1.86+self._extra/70,
                            self._height/1.085-self._extra/5))

            self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                                 position=(100,100),
                                                 size=(self._width-180-self._extra/18,
                                                    self._height-250-self._extra/5),
                                                 highlight=False)
            self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                                 selection_loops_to_parent=True)

            self._ms_title_text(text='Particles', first_title=True)
            self._ms_checkboxwidget(text='Spark particles', cfg_name='Spark Particles', must_restart=False)
            self._ms_checkboxwidget(text='Ice particles', cfg_name='Ice Particles', must_restart=False)
            self._ms_checkboxwidget(text='Slime particles', cfg_name='Slime Particles', must_restart=False)
            self._ms_checkboxwidget(text='Sweat particles', cfg_name='Sweat Particles', must_restart=False)

    def _ms_title_text(self, text, first_title):
        if not first_title:
            ba.textwidget(parent=self._subcontainer,
                          text='',
                          size=(0, 40),
                          scale=self._main_scale)
        ba.textwidget(parent=self._subcontainer,
                      text=text,
                      size=(0, 40),
                      scale=self._main_scale,
                      v_align='center')

    def _ms_checkboxwidget(self, text, cfg_name, must_restart):
        ba.checkboxwidget(parent=self._subcontainer,
                          text=text,
                          size=(500, 47),
                          value=config[cfg_name],
                          on_value_change_call=ba.Call(change_value, cfg_name, must_restart),
                          scale=self._main_scale)

    def _ms_textwidget(self, text):
        ba.textwidget(parent=self._subcontainer,
                      text=text,
                      size=(0, 40),
                      maxwidth=self._height/0.97+self._extra/1.66,
                      v_align='center',
                      color=(0,0.50,0.70),
                      scale=self._main_scale)

    def _set_language(self, language, choice: str):
        config[language] = choice

    def _check_new_bs_version(self):
        ba.screenmessage(message='Checking for BombSquad updates...', color=(1,1,0))
        start_new_thread(check_new_bs_version, ())

    def _back(self):
        ba.containerwidget(edit=self._root_widget, transition='out_scale')
        _ba.set_party_icon_always_visible(True)

class LocalAccountManagerWindow(ba.Window):
    def __init__(self, transition):
        self._uiscale = uiscale = ba.app.ui.uiscale
        self._width = width = (1150 if uiscale is ba.UIScale.SMALL else
            1100 if uiscale is ba.UIScale.MEDIUM else 1050)
        self._height = height = (700 if uiscale is ba.UIScale.SMALL else
            790 if uiscale is ba.UIScale.MEDIUM else 790)
        self._extra = extra = 300 if uiscale is ba.UIScale.SMALL else 0
        b_color = (0.6, 0.53, 0.63)
        
        self._accounts_folder_path = main_path + 'Accounts/'
        self._old_text = ''
        self._bs_path = '/'.join(plugin_path.split('/' if platform == 'linux' else '\\')[0:-1])

        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.19 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.80),
                         transition=transition))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         scale=1.5,
                                         color=(0.83, 1, 0),
                                         text='Accounts',
                                         position=(width-width/1.82+extra/35,
                                            height/1.085-extra/5))

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(250+extra/10,100),
                                             size=(width/1.46-extra/18,
                                                height-260-extra/5),
                                             highlight=False)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)

        self._filter_text = ba.textwidget(parent=self._root_widget,
                                          text=filter_value,
                                          position=(335+extra/8, height-150-extra/5),
                                          size=(width/1.9-extra/18, height/17),
                                          v_align='center',
                                          maxwidth=width/1.9-extra/18-40,
                                          description='Filter',
                                          editable=True)

        self._load_accounts()

        self._add_account_button = ba.buttonwidget(parent=self._root_widget,
                                                   button_type='square',
                                                   label='Add This Account',
                                                   color=(0.29,0.50,0.32),
                                                   size=(210,70),
                                                   position=(770+extra/8,
                                                    height-85-extra/5),
                                                   on_activate_call=self._add_account)

        self._set_account_button = ba.buttonwidget(parent=self._root_widget,
                                                   button_type='square',
                                                   label='Set\nAccount',
                                                   size=(100,100-extra/15),
                                                   textcolor=(0.75, 0.7, 0.8),
                                                   color=b_color,
                                                   scale=(1.3 if uiscale is ba.UIScale.SMALL else
                                                    1.4 if uiscale is ba.UIScale.MEDIUM else 1.5),
                                                   position=(83+extra/6.8,
                                                    self._height-346-self._extra/60),
                                                   on_activate_call=self._set_account)

        self._accounts_folder_button = ba.buttonwidget(parent=self._root_widget,
                                                   button_type='square',
                                                   label='Accounts\nFolder',
                                                   size=(100,100-extra/15),
                                                   textcolor=(0.75, 0.7, 0.8),
                                                   color=b_color,
                                                   scale=(1.3 if uiscale is ba.UIScale.SMALL else
                                                    1.4 if uiscale is ba.UIScale.MEDIUM else 1.5),
                                                   position=(83+extra/6.8,
                                                    self._height-501+self._extra/7.7),
                                                   on_activate_call=self._show_accounts_folder)

        self._delete_account_button = ba.buttonwidget(parent=self._root_widget,
                                                   button_type='square',
                                                   label='Delete\nAccount',
                                                   size=(100,100-extra/15),
                                                   textcolor=(0.75, 0.7, 0.8),
                                                   color=b_color,
                                                   scale=(1.3 if uiscale is ba.UIScale.SMALL else
                                                    1.4 if uiscale is ba.UIScale.MEDIUM else 1.5),
                                                   position=(83+extra/6.8,
                                                    self._height-657+self._extra/3.6),
                                                   on_activate_call=self._confirm_delete_account)

        self._back_button = ba.buttonwidget(
            parent=self._root_widget,
            label='',
            position=(90+extra/100, height-85-extra/5),
            size=(50, 50),
            scale=1.3,
            on_activate_call=self._back,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

        self._update_timer = ba.Timer(0.1, self._update, repeat=True, timetype=ba.TimeType.REAL)

    def _load_accounts(self):
        if not os.path.exists(self._accounts_folder_path):
            os.mkdir(self._accounts_folder_path)

        accounts = os.listdir(self._accounts_folder_path)
        for account in accounts:
            if '.bsuuid' in account:
                account_name_text = account.split('.bsuuid')[0] if len(account.split('.bsuuid')) == 2 and account.split('.bsuuid')[0] else account
                if ba.textwidget(query=self._filter_text) in account:
                    ba.textwidget(parent=self._subcontainer,
                                  text='\ue030'+account_name_text,
                                  v_align='center',
                                  size=(self._width/1.8-self._extra/20, 38),
                                  corner_scale=1.15,
                                  color=(0,1,1),
                                  maxwidth=self._width/1.8-self._extra/18,
                                  on_select_call=ba.Call(self._select_account, account),
                                  always_highlight=True,
                                  selectable=True,
                                  on_activate_call=self._set_account)

    def _select_account(self, account_name):
        self._selected_account = account_name

    def _add_account(self):
        if _ba.get_v1_account_state() != 'signed_in':
            show_sign_in_prompt()
            return
        elif _ba.get_v1_account_type() != 'Local':
            ba.screenmessage(message='You cannot add an online account! Please sign in with an local account.',
                             color=(1,0,0))
            ba.playsound(ba.getsound('error'))
            return

        try:
            account_ds = _ba.get_v1_account_display_string()
            shutil.copyfile(src=self._bs_path+'/.bsuuid', dst=self._accounts_folder_path+f'{account_ds[1:]}.bsuuid')
            self._reload_accounts()

            ba.screenmessage(message='Account successfully added',
                             color=(0,1,0))
            ba.playsound(ba.getsound('ding'))
        except Exception:
            ba.screenmessage(message='An unexpected error occurred', color=(1,0,0))
            ba.playsound(ba.getsound('error'))
            return

    def _set_account(self):
        try:
            shutil.copyfile(src=self._accounts_folder_path+self._selected_account, dst=self._bs_path+'/.bsuuid')
            ba.screenmessage(message=f'Account set to "{self._selected_account}". Please restart the game.',
                             color=(0,1,0))
            ba.playsound(ba.getsound('ding'))
        except Exception: pass

    def _show_accounts_folder(self):
        os.startfile(os.path.realpath(self._accounts_folder_path))

    def _confirm_delete_account(self):
        try:
            if not self._selected_account:
                return
            ConfirmWindow(text=f'Are you sure you want to delete {self._selected_account}?',
                          action=ba.Call(self._delete_account),
                          ok_text='Yes', cancel_text='No',
                          cancel_is_selected=True)
        except Exception: pass

    def _delete_account(self):
        try: os.unlink(self._accounts_folder_path+self._selected_account)
        except Exception: pass

        self._selected_account = ''
        self._reload_accounts()
        ba.playsound(ba.getsound('shieldDown'))

    def _reload_accounts(self):
        self._subcontainer.delete()
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)
        self._load_accounts()

    def _update(self):
        global filter_value
        if not ba.textwidget(query=self._filter_text) == self._old_text:
            self._old_text = ba.textwidget(query=self._filter_text)
            self._reload_accounts()
        filter_value = ba.textwidget(query=self._filter_text)

    def _back(self):
        self._update_timer = None
        ba.containerwidget(edit=self._root_widget, transition='out_scale')

class NewMainMenu:
    global quick_language, show_gather_window, confirm_reconnect_server, reconnect_server
    MainMenuWindow._old_refresh = MainMenuWindow._refresh
    def _new_refresh(self):
        self._old_refresh()

        uiscale = ba.app.ui.uiscale
        b_posX = -128
        b_posY = (-20.5 if uiscale is ba.UIScale.SMALL else
            -53 if uiscale is ba.UIScale.MEDIUM else -78)
        extra = (5 if uiscale is ba.UIScale.SMALL else
            2 if uiscale is ba.UIScale.MEDIUM else 0)
        ingm_btn_pos_x = -60 if config['In-game Buttons On The Left'] else self._width+25
        ingm_btn_pos_y = 0

        if platform == 'windows' or platform == 'linux' or platform == 'mac':
            if uiscale is ba.UIScale.LARGE:
                if config['Show Exit Game Button']:
                    exit_posY = -80
                    icon = ba.gettexture('achievementOutline') if config['Exit The Game Directly'] else ba.gettexture('achievementEmpty')
                    if _ba.is_in_replay():
                        exit_posY = 200
                    if self._in_game:
                        ba.containerwidget(parent=self._root_widget,
                                           size=(222, 60),
                                           position=(19, exit_posY),
                                           scale=1)
                        self._quit_button = ba.buttonwidget(
                            parent=self._root_widget,
                            label=ba.Lstr(resource=self._r + ('.quitText' if 'Mac' in
                                ba.app.user_agent_string else '.exitGameText')),
                            on_activate_call=self._quit,
                            size=(200, 45),
                            position=(27, exit_posY+8),
                            icon=icon,
                            iconscale=1.1)
            else:
                if self._in_game:
                    if config['Show Exit Game Button']:
                        ingm_btn_pos_y += 50-extra
                        self._quit_button = ba.buttonwidget(
                            parent=self._root_widget,
                            label='',
                            on_activate_call=self._quit,
                            size=(45-extra, 45-extra),
                            position=(ingm_btn_pos_x-0.5, self._height-ingm_btn_pos_y),
                            texture=ba.gettexture('textClearButton'),
                            color=(1,0,0))

            if not self._in_game:
                if platform == 'windows' or platform == 'linux' and not self._in_game:
                    self._local_account_manager_button = ba.buttonwidget(
                        parent=self._root_widget,
                        button_type='square',
                        label='',
                        position=(b_posX-b_posX*4.5, b_posY),
                        size=(81, 76+extra),
                        transition_delay=self._tdelay,
                        on_activate_call=ba.Call(LocalAccountManagerWindow, 'in_scale'))
                    ba.imagewidget(parent=self._root_widget,
                                   texture=ba.gettexture('googlePlayLeaderboardsIcon'),
                                   size=(40, 40),
                                   position=(b_posX-b_posX*4.66, b_posY-b_posY/3+extra*5),
                                   transition_delay=self._tdelay,
                                   color=(0.5,0.60,1))
                    ba.textwidget(parent=self._root_widget,
                                  text='Accounts',
                                  color=(0.83, 1, 0),
                                  scale=0.6,
                                  position=(b_posX-b_posX*4.5, b_posY-b_posY/59+extra/1.5),
                                  transition_delay=self._tdelay)

        else:
            if self._in_game:
                if config['Show Exit Game Button']:
                    ingm_btn_pos_y += 50-extra
                    self._quit_button = ba.buttonwidget(
                        parent=self._root_widget,
                        label='',
                        on_activate_call=self._quit,
                        size=(45-extra, 45-extra),
                        position=(ingm_btn_pos_x-0.5, self._height-ingm_btn_pos_y),
                        texture=ba.gettexture('textClearButton'),
                        color=(1,0,0))

        if not self._in_game:
            self._detail_settings_manager_button = ba.buttonwidget(
                parent=self._root_widget,
                button_type='square',
                transition_delay=self._tdelay,
                position=(b_posX, b_posY),
                size=(81, 76+extra),
                label='',
                on_activate_call=ba.Call(DetailSettingsManagerWindow, 'in_scale', ''))
            ba.imagewidget(parent=self._root_widget,
                           texture=ba.gettexture('lock'),
                           size=(40, 40),
                           position=(b_posX-b_posY/3.5+extra*2.9, b_posY-b_posY/3+extra*5),
                           color=(0.55,0.55,0.55),
                           transition_delay=self._tdelay)
            ba.textwidget(parent=self._root_widget,
                          text='Details',
                          color=(0.83, 1, 0),
                          scale=0.74,
                          position=(b_posX-b_posY/12+extra/1.5, b_posY-b_posY/59+extra/1.5),
                          transition_delay=self._tdelay)

            if config['Show Quick Language Button In Main Menu']:
                quick_posX = (-160 if uiscale is ba.UIScale.SMALL else 
                    -240 if uiscale is ba.UIScale.MEDIUM else -380)
                self._quick_language_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type='square',
                    position=(quick_posX, 50+extra*10),
                    size=(40, 40),
                    icon=ba.gettexture('logIcon'),
                    iconscale=1.25,
                    transition_delay=self._tdelay,
                    on_activate_call=quick_language)
        else:
            if config['Show Reconnect Button']:
                ingm_btn_pos_y += 50-extra
                self._reconnect_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type='square',
                    position=(ingm_btn_pos_x, self._height-ingm_btn_pos_y),
                    size=(40-extra, 40-extra),
                    icon=ba.gettexture('replayIcon'),
                    iconscale=1.2,
                    on_activate_call=confirm_reconnect_server)
                if config['Reconnect Server Directly']:
                    ba.buttonwidget(edit=self._reconnect_button, on_activate_call=reconnect_server)
            if config['Show The Details Button']:
                ingm_btn_pos_y += 50-extra
                self._detail_settings_manager_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type='square',
                    position=(ingm_btn_pos_x, self._height-ingm_btn_pos_y),
                    size=(40-extra, 40-extra),
                    icon=ba.gettexture('lock'),
                    iconscale=1.25,
                    on_activate_call=ba.Call(DetailSettingsManagerWindow, 'in_scale', ''),
                    icon_color=(0.55,0.55,0.55))
            if config['Show Quick Language Button']:
                ingm_btn_pos_y += 50-extra
                self._quick_language_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type='square',
                    position=(ingm_btn_pos_x, self._height-ingm_btn_pos_y),
                    size=(40-extra, 40-extra),
                    icon=ba.gettexture('logIcon'),
                    iconscale=1.25,
                    on_activate_call=quick_language,
                    icon_color=(0.45,0.65,0.65))
            if config['Show Gather Button']:
                ingm_btn_pos_y += 50-extra
                self._quick_gather_window = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type='square',
                    position=(ingm_btn_pos_x, self._height-ingm_btn_pos_y),
                    size=(40-extra, 40-extra),
                    icon=ba.gettexture('usersButton'),
                    iconscale=1.225,
                    on_activate_call=show_gather_window)
            global show_mainmenu, in_server
            if _ba.is_in_replay():
                in_server = False
                show_mainmenu = False
            elif _ba.get_foreground_host_session() is not None:
                in_server = False
                show_mainmenu = False
            else:
                in_server = True
                show_mainmenu = True
    MainMenuWindow._refresh = _new_refresh

    """Remove Confirmation Requests"""
    MainMenuWindow._old_confirm_leave_party = MainMenuWindow._confirm_leave_party
    def _new_confirm_leave_party(self):
        global in_server
        in_server = False
        _ba.disconnect_from_host() if config['Leave The Server Directly'] else self._old_confirm_leave_party()
    MainMenuWindow._confirm_leave_party = _new_confirm_leave_party

    MainMenuWindow._old_confirm_end_game = MainMenuWindow._confirm_end_game
    def _new_confirm_end_game(self):
        if config['End The Game Directly']:
            if not self._root_widget:
                return
            ba.containerwidget(edit=self._root_widget, transition='out_left')
            ba.app.return_to_main_menu_session_gracefully(reset_ui=False)
        else:
            self._old_confirm_end_game()
    MainMenuWindow._confirm_end_game = _new_confirm_end_game

    MainMenuWindow._old_confirm_end_replay = MainMenuWindow._confirm_end_replay
    def _new_confirm_end_replay(self):
        if config['End The Replay Directly']:
            if not self._root_widget:
                return
            ba.containerwidget(edit=self._root_widget, transition='out_left')
            ba.app.return_to_main_menu_session_gracefully(reset_ui=False)
        else:
            self._old_confirm_end_replay()
    MainMenuWindow._confirm_end_replay = _new_confirm_end_replay

    MainMenuWindow._old_quit = MainMenuWindow._quit
    def _new_quit(self):
        if config['Exit The Game Directly']:
            _ba.fade_screen(False,
                            time=0.2,
                            endcall=lambda: ba.quit(soft=True, back=False))
        else:
            self._old_quit()
    MainMenuWindow._quit = _new_quit

    def quick_language():
        language_1 = config['Language 1']
        language_2 = config['Language 2']

        if config['Language Order Is 1']:
            ba.app.lang.setlanguage(language_2)
            config['Language Order Is 1'] = False
        else:
            ba.app.lang.setlanguage(language_1)
            config['Language Order Is 1'] = True

    def show_gather_window():
        global gather_window_detected
        gather_window_detected = True
        GatherWindow(transition='in_scale')

    def confirm_reconnect_server():
        if _ba.get_connection_to_host_info().get('name', False):
            ConfirmWindow(text='Are you sure you want to reconnect to the server?',
                          cancel_text='No', ok_text='Yes',
                          action=reconnect_server)
        else:
            ba.screenmessage('You are not on a server', color=(1,0,0))
            ba.playsound(ba.getsound('error'))

    def reconnect_server():
        if _ba.get_connection_to_host_info().get('name', False):
            _ba.disconnect_from_host()
            ba.timer(0.1, ba.Call(_ba.connect_to_party, server_ip, server_port, _print_progress))
        else:
            ba.screenmessage('You are not on a server', color=(1,0,0))
            ba.playsound(ba.getsound('error'))

AllSettingsWindow._old_init = AllSettingsWindow.__init__
def _new_init(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
    self._old_init()
    uiscale = ba.app.ui.uiscale
    width = 120 if uiscale is ba.UIScale.SMALL else 95
    height = 380 if uiscale is ba.UIScale.SMALL else 388
    extra = 50 if uiscale is ba.UIScale.SMALL else 0

    self._new_plugins_button = ba.buttonwidget(parent=self._root_widget,
                    size=(width, 30),
                    scale=1.5,
                    label='',
                    position=(width*4+extra, height),
                    on_activate_call=ba.Call(show_plugin_settings_window, self._root_widget))
    ba.textwidget(parent=self._root_widget,
                  text='Plugins',
                  color=(0.75, 1.0, 0.7),
                  position=(width*4.54+extra*1.15, height*1.02))
    ba.imagewidget(parent=self._root_widget,
                   texture=ba.gettexture('file'),
                   size=(45, 45),
                   position=(width*4.03+extra*1.3, height-2.5))
AllSettingsWindow.__init__ = _new_init

class NewPluginSettingsWindow:
    global back_to_allsettings_window, show_delete_window, confirm_deletion, delete_plugin
    PluginSettingsWindow._old_init = PluginSettingsWindow.__init__
    def _new_init(self, transition='in_right'):
        self._old_init(transition=transition)
        uiscale = ba.app.ui.uiscale
        w = (285 if uiscale is ba.UIScale.SMALL else
            127 if uiscale is ba.UIScale.MEDIUM else 57)
        h = (62 if uiscale is ba.UIScale.SMALL else
            60 if uiscale is ba.UIScale.MEDIUM else 58)

        self._delete_button = ba.buttonwidget(parent=self._root_widget,
                                              button_type='square',
                                              size=(50, 50),
                                              label='',
                                              position=(self._height+w, self._height-h),
                                              scale=0.87,
                                              icon=ba.gettexture('textClearButton'),
                                              iconscale=(1.22 if uiscale is ba.UIScale.SMALL else
                                                1.235 if uiscale is ba.UIScale.MEDIUM else 1.23),
                                              on_activate_call=ba.Call(show_delete_window))

        ba.buttonwidget(edit=self._back_button, on_activate_call=ba.Call(back_to_allsettings_window, self._root_widget, AllSettingsWindow))
    PluginSettingsWindow.__init__ = _new_init

    def back_to_allsettings_window(root_widget, window):
        ba.containerwidget(edit=root_widget, transition='out_scale')
        window(transition='in_scale')

    def show_delete_window():
        global root_widget
        root_widget = FileSelectorWindow(path=plugin_path,
                                         valid_file_extensions=['py'],
                                         allow_folders=False).get_root_widget()

    def confirm_deletion(file_name, *args):
        if os.path.isdir(f'{plugin_path}/{file_name}'):
            ba.screenmessage('You cannot delete a folder',
                             color=(1,0,0))
            ba.playsound(ba.getsound('error'))
        else:
            ConfirmWindow(text=f'Are you sure you want to delete {file_name}?',
                          action=ba.Call(delete_plugin, file_name),
                          ok_text='Yes', cancel_text='No',
                          cancel_is_selected=True)

    def delete_plugin(file_name):
        global root_widget
        try: os.unlink(f'{plugin_path}/{file_name}')
        except FileNotFoundError: pass
        finally:
            ba.playsound(ba.getsound('shieldDown'))
            ba.screenmessage(message=ba.Lstr(resource='settingsWindowAdvanced.mustRestartText'),
                             color=(1.0, 0.5, 0.0))
            ba.containerwidget(edit=root_widget, transition='out_scale')
            root_widget = FileSelectorWindow(path=plugin_path,
                                             valid_file_extensions=['py'],
                                             allow_folders=False).get_root_widget()

    def _new_on_entry_activated(self, entry: str):
        ba.playsound(ba.getsound('swish'))
        confirm_deletion(entry)
    FileSelectorWindow._on_entry_activated = _new_on_entry_activated

class NewAccountSettingsWindow:
    global copy_pb
    AccountSettingsWindow._old_init = AccountSettingsWindow.__init__
    def _new_init(self, transition: str = 'in_right', modal: bool = False,
                  origin_widget: ba.Widget = None, close_once_signed_in: bool = False):
        self._old_init()

        pb_id = _ba.get_v1_account_misc_read_val_2('resolvedAccountID', '')
        if _ba.get_v1_account_state() == 'signed_in':
            ba.textwidget(parent=self._subcontainer,
                          text=f'Your PB ID: {pb_id}',
                          position=(80, 0),
                          maxwidth=(300),
                          v_align='center',
                          size=(0,43))
            ba.buttonwidget(parent=self._subcontainer,
                            label='Copy',
                            position=(420, 8),
                            size=(50,25),
                            on_activate_call=ba.Call(copy_pb, pb_id))
    AccountSettingsWindow.__init__ = _new_init

    def copy_pb(pb):
        _ba.clipboard_set_text(pb)
        ba.screenmessage(message=f'PB ID is copied to clipboard',
                         color=(0,1,0))
        ba.playsound(ba.getsound('ding'))

class PingThread(threading.Thread):
    def __init__(self, address: str, port: int):
        super().__init__()
        self._address = address
        self._port = port

    def run(self) -> None:
        sock: Optional[socket.socket] = None
        try:
            import socket
            from ba.internal import get_ip_address_type
            socket_type = get_ip_address_type(self._address)
            sock = socket.socket(socket_type, socket.SOCK_DGRAM)
            sock.connect((self._address, self._port))

            starttime = time.time()

            sock.settimeout(1)
            for _i in range(3):
                sock.send(b'\x0b')
                result: Optional[bytes]
                try:
                    # 11: BA_PACKET_SIMPLE_PING
                    result = sock.recv(10)
                except Exception:
                    result = None
                if result == b'\x0c':
                    # 12: BA_PACKET_SIMPLE_PONG
                    break
                time.sleep(1)
            ping = (time.time() - starttime) * 1000.0
        except Exception as exc:
            from efro.error import is_udp_network_error
            if is_udp_network_error(exc):
                pass
            else:
                ba.print_exception('Error on gather ping', once=True)
        finally:
            try:
                if sock is not None:
                    sock.close()
            except Exception:
                ba.print_exception('Error on gather ping cleanup', once=True)
        ba.pushcall(ba.Call(check_ping, ping), from_other_thread=True)

class NewPartyWindow:
    global confirm_copy_message, copy_message, confirm_open_url, vote_kick_player, add_friend_window, add_friend
    def _new_init(self, origin: Sequence[float] = (0, 0)):
        _ba.set_party_window_open(True)
        self._r = 'partyWindow'
        self._popup_type: Optional[str] = None
        self._popup_party_member_client_id: Optional[int] = None
        self._popup_party_member_is_host: Optional[bool] = None
        self._width = 500
        uiscale = ba.app.ui.uiscale
        self._height = (365 if uiscale is ba.UIScale.SMALL else
                        480 if uiscale is ba.UIScale.MEDIUM else 600)
        config['Chat Muted'] = config['Mute Chat']
        config.apply_and_commit()
        ba.Window.__init__(self,
            root_widget=ba.containerwidget(
            size=(self._width, self._height),
            transition='in_scale',
            color=(0.40, 0.55, 0.20),
            parent=_ba.get_special_widget('overlay_stack'),
            on_outside_click_call=self.close_with_sound,
            scale_origin_stack_offset=origin,
            scale=(2.0 if uiscale is ba.UIScale.SMALL else
                   1.35 if uiscale is ba.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -10) if uiscale is ba.UIScale.SMALL else (
                240, 0) if uiscale is ba.UIScale.MEDIUM else (330, 20)))

        self._cancel_button = ba.buttonwidget(parent=self._root_widget,
                                              scale=0.7,
                                              position=(30, self._height - 47),
                                              size=(50, 50),
                                              label='',
                                              on_activate_call=self.close,
                                              autoselect=True,
                                              color=(0.45, 0.63, 0.15),
                                              icon=ba.gettexture('crossOut'),
                                              iconscale=1.2)
        ba.containerwidget(edit=self._root_widget, cancel_button=self._cancel_button)

        self._menu_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(self._width-60, self._height-47),
            size=(50, 50),
            label='',
            autoselect=True,
            button_type='square',
            icon=ba.gettexture('settingsIcon'),
            on_activate_call=ba.WeakCall(self._on_menu_button_press),
            color=(0.55, 0.73, 0.25),
            icon_color=(0.55,0.55,0.55),
            iconscale=1.2)

        if config['Show Ping Button']:
            self._ping_button = ba.buttonwidget(
                parent=self._root_widget,
                scale=0.7,
                position=(self._width-105, self._height-47),
                size=(50, 50),
                label='Ping',
                autoselect=True,
                button_type='square',
                on_activate_call=lambda: PingThread(server_ip, server_port).start(),
                color=(0.55, 0.73, 0.25),
                icon_color=(0.55,0.55,0.55),
                iconscale=1.2)

        self._friends_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(79, self._height-45.5),
            size=(50, 50),
            icon=ba.gettexture('usersButton'),
            iconscale=1.17,
            on_activate_call=ba.Call(FriendsWindow, 'in_scale', self._root_widget))

        info = _ba.get_connection_to_host_info()
        if info.get('name', '') != '':
            title = ba.Lstr(value=info['name'])
        else:
            title = ba.Lstr(resource=self._r + '.titleText')

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         scale=0.9,
                                         color=(0.5, 0.7, 0.5),
                                         text=title,
                                         size=(0, 0),
                                         position=(self._width * 0.51,
                                                   self._height - 29),
                                         maxwidth=self._width * 0.5,
                                         h_align='center',
                                         v_align='center')

        self._empty_str = ba.textwidget(parent=self._root_widget,
                                        scale=0.75,
                                        size=(0, 0),
                                        position=(self._width * 0.5,
                                                  self._height - 65),
                                        maxwidth=self._width * 0.85,
                                        h_align='center',
                                        v_align='center')

        self._scroll_width = self._width - 50
        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             size=(self._scroll_width,
                                                   self._height - 200),
                                             position=(30, 80),
                                             color=(0.4, 0.6, 0.3))
        self._columnwidget = ba.columnwidget(parent=self._scrollwidget,
                                             border=2,
                                             margin=0)
        ba.widget(edit=self._menu_button, down_widget=self._columnwidget)

        self._muted_text = ba.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=ba.Lstr(resource='chatMutedText'))
        self._chat_texts: list[ba.Widget] = []

        # add all existing messages if chat is not muted
        if not ba.app.config.resolve('Chat Muted'):
            msgs = _ba.get_chat_messages()
            for msg in msgs:
                self._add_msg(msg)

        self._text_field = txt = ba.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(530, 40),
            position=(44, 39),
            text='',
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            description=ba.Lstr(resource=self._r + '.chatMessageText'),
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        ba.widget(edit=self._scrollwidget,
                  autoselect=True,
                  left_widget=self._cancel_button,
                  up_widget=self._cancel_button,
                  down_widget=self._text_field)
        ba.widget(edit=self._columnwidget,
                  autoselect=True,
                  up_widget=self._cancel_button,
                  down_widget=self._text_field)
        ba.containerwidget(edit=self._root_widget, selected_child=txt)
        btn = ba.buttonwidget(parent=self._root_widget,
                              size=(50, 35),
                              label=ba.Lstr(resource=self._r + '.sendText'),
                              button_type='square',
                              autoselect=True,
                              position=(self._width - 70, 35),
                              on_activate_call=self._send_chat_message)
        ba.textwidget(edit=txt, on_return_press_call=btn.activate)
        self._name_widgets: list[ba.Widget] = []
        self._roster: Optional[list[dict[str, Any]]] = None
        self._update_timer = ba.Timer(1.0,
                                      ba.WeakCall(self._update),
                                      repeat=True,
                                      timetype=ba.TimeType.REAL)
        self._update()
    PartyWindow.__init__ = _new_init

    PartyWindow._old_add_msg = PartyWindow._add_msg
    def _new_add_msg(self, msg: str):
        txt = ba.textwidget(parent=self._columnwidget,
                            text=msg,
                            h_align='left',
                            v_align='center',
                            size=(self._scroll_width * 2, 21),
                            scale=1,
                            corner_scale=0.60,
                            maxwidth=self._scroll_width * 1.55,
                            shadow=0.3,
                            selectable=True,
                            click_activate=True,
                            on_activate_call=ba.Call(confirm_copy_message, msg))
        if config['Copy Message Directly']:
            ba.textwidget(edit=txt, on_activate_call=ba.Call(copy_message, msg))
        if 'https://' in msg:
            split_msg = msg.split(' ')
            for i in split_msg:
                if i.startswith('https://'):
                    ba.textwidget(edit=txt, on_activate_call=ba.Call(confirm_open_url, i),
                                  color=(0,0.90,1))
                    if config['Open Link Directly']:
                        ba.textwidget(edit=txt, on_activate_call=ba.Call(ba.open_url, i))
        self._chat_texts.append(txt)
        if len(self._chat_texts) > 40:
            first = self._chat_texts.pop(0)
            first.delete()
        ba.containerwidget(edit=self._columnwidget, visible_child=txt)
    PartyWindow._add_msg = _new_add_msg

    PartyWindow._old_send_chat_message = PartyWindow._send_chat_message
    def _new_send_chat_message(self):
        msg = ba.textwidget(query=self._text_field)
        if msg == config['Ping Command']:
            PingThread(server_ip, server_port).start()
            ba.textwidget(edit=self._text_field, text='')
        elif msg == '!ip':
            if _ba.get_connection_to_host_info().get('name', False):
                ba.textwidget(edit=self._text_field, text=f'{server_ip} {server_port}')
            else:
                ba.screenmessage('You are not on a server', color=(1,0,0))
                ba.playsound(ba.getsound('error'))
                ba.textwidget(edit=self._text_field, text='')
        elif msg == '!copyip':
            if _ba.get_connection_to_host_info().get('name', False):
                _ba.clipboard_set_text(f'{server_ip} {server_port}')
                ba.screenmessage(message=f'Server ip copied to clipboard.', color=(0,1,0))
                ba.playsound(ba.getsound('ding'))
            else:
                ba.screenmessage('You are not on a server', color=(1,0,0))
                ba.playsound(ba.getsound('error'))
            ba.textwidget(edit=self._text_field, text='')
        elif msg == '!pws':
            DetailSettingsManagerWindow(transition='in_scale', custom_tab='pw_tab')
            ba.containerwidget(edit=self._root_widget, transition='out_scale')
            ba.textwidget(edit=self._text_field, text='')
        elif msg == '!dsw':
            DetailSettingsManagerWindow(transition='in_scale', custom_tab='')
            ba.containerwidget(edit=self._root_widget, transition='out_scale')
            ba.textwidget(edit=self._text_field, text='')
        elif '!set ping command' in msg:
            if len(msg.split('!set ping command')) < 3:
                is_unlined = msg.split('!set ping command')[1].split(' ')
                if len(is_unlined) == 2:
                    config['Ping Command'] = str(is_unlined[1])
                    ba.screenmessage(message=f'Ping command set to "{is_unlined[1]}"',
                                     color=(0,1,0))
                    ba.playsound(ba.getsound('ding'))
                else:
                    ba.screenmessage(message='Error!',
                                     color=(1,0,0))
                    ba.playsound(ba.getsound('error'))
            else:
                ba.screenmessage(message='Error!',
                                 color=(1,0,0))
                ba.playsound(ba.getsound('error'))
            ba.textwidget(edit=self._text_field, text='')
        elif '!set ping message' in msg:
            if len(msg.split('!set ping message')) < 3:
                if not msg.split('!set ping message')[1][1:] or not msg.split('!set ping message')[1][0:1] == ' ':
                    ba.screenmessage(message='Error!',
                                     color=(1,0,0))
                    ba.playsound(ba.getsound('error'))
                else:
                    if '!' in msg.split('!set ping message')[1][1:] and len(msg.split('!set ping message')[1][1:].split('!')) < 3:
                        config['Ping Message'] = msg.split('!set ping message')[1][1:]
                        ba.screenmessage(f'Ping message set to "{msg.split("!set ping message")[1][1:]}"',
                                         color=(0,1,0))
                        ba.playsound(ba.getsound('ding'))
                    else:
                        ba.screenmessage(message='Error!',
                                         color=(1,0,0))
                        ba.playsound(ba.getsound('error'))
            else:
                ba.screenmessage(message='Error!',
                                 color=(1,0,0))
                ba.playsound(ba.getsound('error'))
            ba.textwidget(edit=self._text_field, text='')
        else:
            self._old_send_chat_message()
    PartyWindow._send_chat_message = _new_send_chat_message

    PartyWindow._old_popup_menu_selected_choice = PartyWindow.popup_menu_selected_choice
    def _new_popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str):
        """Called when a choice is selected in the popup."""
        try:
            uiscale = ba.app.ui.uiscale
            if self._popup_type == 'partyMemberPress':
                player_details = {}
                for i in _ba.get_game_roster():
                    if i['client_id'] == player_id:
                        player_details['display_string'] = i['display_string']
                        player_details['players'] = i['players']
                        break

                playerlist = [player_details['display_string']]
                for player in player_details['players']:
                    name = player['name_full']
                    if not name in playerlist:
                        playerlist.append(name)
                try:
                    with open(main_path+'Friends.bsd', 'r') as file:
                        old_file_text = file.readlines()
                        for f in old_file_text:
                            f_ds = json.loads(f)
                            if f_ds['display string'] == player_details['display_string']:
                                playerlist.append(f_ds['custom tag'])
                        file.close()
                except Exception: pass
                playerlist.append(str(player_id))
                
                if choice == 'kick':
                    if self._popup_party_member_is_host:
                        ba.playsound(ba.getsound('error'))
                        ba.screenmessage(
                            ba.Lstr(resource='internal.cantKickHostError'),
                            color=(1, 0, 0))
                    else:
                        ConfirmWindow(
                            text=f'Are you sure you want to kick {player_details["display_string"]}?',
                            action=ba.Call(vote_kick_player,
                                           self._popup_party_member_is_host,
                                           self._popup_party_member_client_id),
                            cancel_text='No', ok_text='Yes',
                            cancel_is_selected=True)
                elif choice == 'players':
                    PopupMenuWindow(position=popup_window.root_widget.get_screen_space_center(),
                                    scale=(2.4 if uiscale is ba.UIScale.SMALL else
                                        1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
                                    choices=playerlist,
                                    current_choice=playerlist[0],
                                    delegate=self)
                elif choice == 'add friend' or choice == 'edit details':
                    add_friend_window(player_details["display_string"])
                elif choice == f'/kick {player_id}':
                    confirm_kick_player = ConfirmWindow(
                        text=f'Are you sure you want to kick {player_details["display_string"]}?',
                        action=ba.Call(_ba.chatmessage, f'/kick {player_id}'),
                        cancel_text='No', ok_text='Yes',
                        cancel_is_selected=True)
                for player in playerlist:
                    if choice == player:
                        ba.textwidget(edit=self._text_field,
                            text=ba.textwidget(query=self._text_field) + player)
                    elif choice == player_id:
                        ba.textwidget(edit=self._text_field,
                            text=ba.textwidget(query=self._text_field) + player_id)
            elif self._popup_type == 'menu':
                message_status_text = 'show in-game messages' if config['Hide In-game Messages'] else 'hide in-game messages'
                if choice in ('mute', 'unmute'):
                    cfg = ba.app.config
                    cfg['Chat Muted'] = (choice == 'mute')
                    cfg.apply_and_commit()
                    config['Mute Chat'] = False if config['Mute Chat'] else True
                    self._update()
                elif choice == message_status_text:
                    config['Hide In-game Messages'] = False if config['Hide In-game Messages'] else True
                elif choice == 'party window settings':
                    DetailSettingsManagerWindow(transition='in_scale', custom_tab='pw_tab')
                    ba.containerwidget(edit=self._root_widget, transition='out_scale')
            else:
                print(f'unhandled popup type: {self._popup_type}')
        except Exception as e: print(str(e)+' Error')
    PartyWindow.popup_menu_selected_choice = _new_popup_menu_selected_choice

    PartyWindow._old_on_party_member_press = PartyWindow._on_party_member_press
    def _new_on_party_member_press(self, client_id: int, is_host: bool,
                               widget: ba.Widget) -> None:
        global player_id
        
        player_id = client_id
        selection_text = 'add friend'

        try:
            with open(main_path+'Friends.bsd', 'r') as file:
                for i in _ba.get_game_roster():
                    if i['client_id'] == player_id:
                        ds = i['display_string']
                old_file_text = file.readlines()
                for f in old_file_text:
                    f_ds = json.loads(f)['display string']
                    if f_ds == ds:
                        selection_text = 'edit details'
                file.close()
        except Exception: pass

        # if we're the host, pop up 'kick' options for all non-host members
        if _ba.get_foreground_host_session() is not None:
            kick_str = ba.Lstr(resource='kickText')
        else:
            # kick-votes appeared in build 14248
            if (_ba.get_connection_to_host_info().get('build_number', 0) <
                    14248):
                return
            kick_str = ba.Lstr(resource='kickVoteText')
        uiscale = ba.app.ui.uiscale
        PopupMenuWindow(
            position=widget.get_screen_space_center(),
            scale=(2.3 if uiscale is ba.UIScale.SMALL else
                   1.65 if uiscale is ba.UIScale.MEDIUM else 1.23),
            choices=['kick', 'players', selection_text, f'/kick {player_id}'],
            choices_display=[kick_str],
            current_choice='kick',
            delegate=self)
        self._popup_type = 'partyMemberPress'
        self._popup_party_member_client_id = client_id
        self._popup_party_member_is_host = is_host
    PartyWindow._on_party_member_press = _new_on_party_member_press

    PartyWindow._old_on_menu_button_press = PartyWindow._on_menu_button_press
    def _on_menu_button_press(self) -> None:
        is_muted = ba.app.config.resolve('Chat Muted')
        uiscale = ba.app.ui.uiscale
        message_status_text = 'show in-game messages' if config['Hide In-game Messages'] else 'hide in-game messages'
        PopupMenuWindow(
            position=self._menu_button.get_screen_space_center(),
            scale=(2.3 if uiscale is ba.UIScale.SMALL else
                   1.65 if uiscale is ba.UIScale.MEDIUM else 1.23),
            choices=['unmute' if is_muted else 'mute', message_status_text, 'party window settings'],
            choices_display=[
                ba.Lstr(
                    resource='chatUnMuteText' if is_muted else 'chatMuteText')
            ],
            current_choice='unmute' if is_muted else 'mute',
            delegate=self)
        self._popup_type = 'menu'
    PartyWindow._on_menu_button_press = _on_menu_button_press

    def _new_update(self):
        if ba.app.config.resolve('Chat Muted'):
            ba.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.3))
            if self._chat_texts:
                while self._chat_texts:
                    first = self._chat_texts.pop()
                    first.delete()
        else:
            ba.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.0))

        # update roster section
        roster = _ba.get_game_roster()
        if roster != self._roster:
            self._roster = roster

            # clear out old
            for widget in self._name_widgets:
                widget.delete()
            self._name_widgets = []
            if not self._roster:
                top_section_height = 60
                ba.textwidget(edit=self._empty_str,
                              text=ba.Lstr(resource=self._r + '.emptyText'))
                ba.scrollwidget(edit=self._scrollwidget,
                                size=(self._width - 50,
                                      self._height - top_section_height - 110),
                                position=(30, 80))
            else:
                columns = 1 if len(
                    self._roster) == 1 else 2 if len(self._roster) == 2 else 3
                rows = int(math.ceil(float(len(self._roster)) / columns))
                c_width = (self._width * 0.9) / max(3, columns)
                c_width_total = c_width * columns
                c_height = 24
                c_height_total = c_height * rows
                for y in range(rows):
                    for x in range(columns):
                        index = y * columns + x
                        if index < len(self._roster):
                            t_scale = 0.65
                            pos = (self._width * 0.53 - c_width_total * 0.5 +
                                   c_width * x - 23,
                                   self._height - 65 - c_height * y - 15)

                            # if there are players present for this client, use
                            # their names as a display string instead of the
                            # client spec-string
                            try:
                                if self._roster[index]['players']:
                                    # if there's just one, use the full name;
                                    # otherwise combine short names
                                    if len(self._roster[index]
                                           ['players']) == 1:
                                        p_str = self._roster[index]['players'][
                                            0]['name_full']
                                    else:
                                        p_str = ('/'.join([
                                            entry['name'] for entry in
                                            self._roster[index]['players']
                                        ]))
                                        if len(p_str) > 25:
                                            p_str = p_str[:25] + '...'
                                else:
                                    p_str = self._roster[index][
                                        'display_string']
                            except Exception:
                                ba.print_exception(
                                    'Error calcing client name str.')
                                p_str = '???'

                            party_member_text_color = (1,1,1)
                            try:
                                with open(main_path+'Friends.bsd', 'r') as file:
                                    old_file_text = file.readlines()
                                    for f in old_file_text:
                                        f_ds = json.loads(f)
                                        if f_ds['display string'] == self._roster[index]['display_string']:
                                            party_member_text_color = (0.0,0.5,0.6)
                            except Exception: pass

                            widget = ba.textwidget(parent=self._root_widget,
                                                   position=(pos[0], pos[1]),
                                                   scale=t_scale,
                                                   size=(c_width * 0.85, 30),
                                                   maxwidth=c_width * 0.85,
                                                   color=party_member_text_color,
                                                   selectable=True,
                                                   autoselect=True,
                                                   click_activate=True,
                                                   text=ba.Lstr(value=p_str),
                                                   h_align='left',
                                                   v_align='center')
                            self._name_widgets.append(widget)

                            if self._roster[index]['client_id'] is not None:
                                is_host = self._roster[index][
                                    'client_id'] == -1
                            else:
                                is_host = (index == 0)

                            ba.textwidget(edit=widget,
                                          on_activate_call=ba.Call(
                                              self._on_party_member_press,
                                              self._roster[index]['client_id'],
                                              is_host, widget))
                            pos = (self._width * 0.53 - c_width_total * 0.5 +
                                   c_width * x,
                                   self._height - 65 - c_height * y)

                            if is_host:
                                twd = min(
                                    c_width * 0.85,
                                    _ba.get_string_width(
                                        p_str, suppress_warning=True) *
                                    t_scale)
                                self._name_widgets.append(
                                    ba.textwidget(
                                        parent=self._root_widget,
                                        position=(pos[0] + twd + 1,
                                                  pos[1] - 0.5),
                                        size=(0, 0),
                                        h_align='left',
                                        v_align='center',
                                        maxwidth=c_width * 0.96 - twd,
                                        color=(0.1, 1, 0.1, 0.5),
                                        text=ba.Lstr(resource=self._r +
                                                     '.hostText'),
                                        scale=0.4,
                                        shadow=0.1,
                                        flatness=1.0))
                ba.textwidget(edit=self._empty_str, text='')
                ba.scrollwidget(edit=self._scrollwidget,
                                size=(self._width - 50,
                                      max(100, self._height - 139 -
                                          c_height_total)),
                                position=(30, 80))
    PartyWindow._update = _new_update

    PartyWindow._old_close = PartyWindow.close
    def _new_close(self):
        self._old_close()
        message_status = config['Hide In-game Messages']
        config['Chat Muted'] = message_status
        config.apply_and_commit()
        self._update()
    PartyWindow.close = _new_close

    def confirm_copy_message(message):
        ba.playsound(ba.getsound('swish'))
        ConfirmWindow(text='Do you want to copy this message?',
                      action=ba.Call(copy_message, message),
                      cancel_text='No', ok_text='Yes')

    def copy_message(message):
        msg_with_name = message.split(' ')
        name_detected = False
        msg = ''
        for i in msg_with_name:
            if i == msg_with_name[0] and not name_detected:
                name_detected = True
                continue
            else:
                msg += i + ' '
        msg = msg[0:-1]
        _ba.clipboard_set_text(msg)
        ba.screenmessage('Message copied to clipboard.', color=(0,1,0))
        ba.playsound(ba.getsound('ding'))

    def confirm_open_url(url):
        ba.playsound(ba.getsound('swish'))
        ConfirmWindow(text='Are you sure you want to open this link?',
                      cancel_text='No', ok_text='Yes',
                      action=(ba.Call(ba.open_url, url)))

    def vote_kick_player(host_id, player_id):
        if host_id:
            ba.playsound(ba.getsound('error'))
            ba.screenmessage(
                ba.Lstr(resource='internal.cantKickHostError'),
                color=(1, 0, 0))
        else:
            assert player_id is not None

            # Ban for 5 minutes.
            result = _ba.disconnect_client(
                player_id, ban_time=5 * 60)
            if not result:
                ba.playsound(ba.getsound('error'))
                ba.screenmessage(
                    ba.Lstr(resource='getTicketsWindow.unavailableText'),
                    color=(1, 0, 0))

    def add_friend_window(display_string):
        uiscale = ba.app.ui.uiscale

        root_widget = ba.containerwidget(parent=_ba.get_special_widget('overlay_stack'),
                                         size=(450, 250),
                                         transition='in_scale',
                                         scale=(1.6 if uiscale is ba.UIScale.SMALL else 
                                            1.2 if uiscale is ba.UIScale.MEDIUM else 1.1))

        title_text = ba.textwidget(parent=root_widget,
                                   h_align='center',
                                   v_align='center',
                                   text=display_string,
                                   position=(200, 188),
                                   maxwidth=200)

        name_entry_field = ba.textwidget(parent=root_widget,
                                         position=(53,135),
                                         size=(350,30),
                                         v_align='center',
                                         editable=True,
                                         description='Name',
                                         maxwidth=310)

        cancel_button = ba.buttonwidget(parent=root_widget,
                                        label='Cancel',
                                        size=(170, 50),
                                        position=(50, 50),
                                        on_activate_call=ba.Call(ba.containerwidget, edit=root_widget, transition='out_scale'))
        ba.containerwidget(edit=root_widget, cancel_button=cancel_button)

        ok_button = ba.buttonwidget(parent=root_widget,
                                    label='Ok',
                                    size=(170, 50),
                                    position=(233, 50),
                                    on_activate_call=lambda: add_friend(
                                        display_string=display_string,
                                        custom_tag=ba.textwidget(query=name_entry_field),
                                        root_widget=root_widget))
        ba.containerwidget(edit=root_widget, start_button=ok_button)

    def add_friend(display_string, custom_tag, root_widget):
        road_is_open = True
        if not custom_tag:
            ba.screenmessage(message='Name cannot be empty',
                             color=(1,0,0))
            ba.playsound(ba.getsound('error'))
            return

        ba.containerwidget(edit=root_widget, transition='out_scale')
        friend = {'display string': display_string,
                  'custom tag': custom_tag}
        try:
            with open(main_path+'Friends.bsd', 'r') as file:
                old_file_text = file.readlines()
                for i, f in enumerate(old_file_text):
                    if display_string == json.loads(f)['display string']:
                        old_file_text[i] = json.dumps(friend)
                        road_is_open = False
                _old_file_text = old_file_text
                old_file_text = ''
                for f in _old_file_text:
                    if not f or f == '\n':
                        continue
                    f = f[0:-1] if f[-1] == '\n' else f
                    f = f[1:] if f[1] == '\n' else f
                    old_file_text += f+'\n'
                old_file_text = old_file_text[0:-1]
                file.close()
        except Exception: pass
        with open(main_path+'Friends.bsd', 'w') as file:
            if road_is_open:
                file.write(json.dumps(friend))
            try:
                file.write('\n'+old_file_text) if road_is_open else file.write(old_file_text)
            except Exception: pass
            file.close()
        ba.screenmessage(message=f'{display_string} added to friends', color=(0,1,0))
        ba.playsound(ba.getsound('ding'))

class FriendsWindow(ba.Window):
    def __init__(self, transition, previous_widget):
        _ba.set_party_icon_always_visible(False)
        try: ba.containerwidget(edit=previous_widget, transition='out_scale')
        except Exception: pass

        self._uiscale = uiscale = ba.app.ui.uiscale
        self._width = width = (680 if uiscale is ba.UIScale.SMALL else
            700 if uiscale is ba.UIScale.MEDIUM else 800)
        self._height = height = (700 if uiscale is ba.UIScale.SMALL else
            790 if uiscale is ba.UIScale.MEDIUM else 890)
        self._extra = extra = 300 if uiscale is ba.UIScale.SMALL else 0

        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.0 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.70),
                         transition=transition))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         position=(width-width/1.8-extra/90, height/1.085-extra/10),
                                         text='Friends',
                                         scale=1.5,
                                         color=(0.83, 1, 0))

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(95-extra/30,90-extra/30),
                                             size=(width-180+extra/20, height-220+extra/90),
                                             highlight=False)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)

        self._load_friends()

        self._edit_details_button = ba.buttonwidget(parent=self._root_widget,
                                                    label='Edit\nDetails',
                                                    on_activate_call=self._edit_details_window,
                                                    position=(-160, height/1.5-extra/10),
                                                    text_scale=1.3,
                                                    size=(150, 150),
                                                    color=(0.6, 0.53, 0.63),
                                                    button_type='square')

        self._remove_friend_button = ba.buttonwidget(parent=self._root_widget,
                                                     label='Remove\nFriend',
                                                     on_activate_call=self._confirm_remove_friend,
                                                     position=(-160, height/2.05-extra/5.9),
                                                     text_scale=1.3,
                                                     size=(150, 150),
                                                     color=(0.6, 0.53, 0.63),
                                                     button_type='square')

        self._back_button = ba.buttonwidget(
            parent=self._root_widget,
            label='',
            position=(90, height-85-extra/20),
            size=(60, 60),
            scale=1.3,
            on_activate_call=self._back,
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

    def _load_friends(self):
        try:
            with open(main_path+'Friends.bsd', 'r') as file:
                self._friends = file.readlines()
                file.close()
            for f in self._friends:
                friend = json.loads(f)
                ba.textwidget(parent=self._subcontainer,
                              size=(self._width-400+self._extra/20, 40),
                              maxwidth=self._width-400+self._extra/6-20,
                              corner_scale=1.5,
                              v_align='center',
                              text=friend['custom tag'],
                              color=(0.0,0.5,0.6),
                              selectable=True,
                              always_highlight=True,
                              on_select_call=ba.Call(self._select_friend, friend['display string']),
                              on_activate_call=self._edit_details_window)
        except Exception: pass

    def _reload_friends(self):
        self._subcontainer.delete()
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)
        self._load_friends()

    def _select_friend(self, display_string):
        self._selected_friend = display_string

    def _edit_details_window(self):
        try:
            if not self._selected_friend:
                return
            display_string = self._selected_friend
            self._root_widget2 = ba.containerwidget(parent=_ba.get_special_widget('overlay_stack'),
                                                    size=(450, 250),
                                                    transition='in_scale',
                                                    scale=(1.6 if self._uiscale is ba.UIScale.SMALL else
                                                        1.2 if self._uiscale is ba.UIScale.MEDIUM else 1.1))

            self._title_text2 = ba.textwidget(parent=self._root_widget2,
                                              h_align='center',
                                              v_align='center',
                                              text=display_string,
                                              position=(200, 188),
                                              maxwidth=200)

            self._name_entry_field = ba.textwidget(parent=self._root_widget2,
                                                   position=(53,135),
                                                   size=(350,30),
                                                   v_align='center',
                                                   editable=True,
                                                   description='Name',
                                                   maxwidth=310)

            self._cancel_button = ba.buttonwidget(parent=self._root_widget2,
                                                  label='Cancel',
                                                  size=(170, 50),
                                                  position=(50, 50),
                                                  on_activate_call=ba.Call(ba.containerwidget, edit=self._root_widget2, transition='out_scale'))
            ba.containerwidget(edit=self._root_widget2, cancel_button=self._cancel_button)

            self._ok_button = ba.buttonwidget(parent=self._root_widget2,
                                              label='Ok',
                                              size=(170, 50),
                                              position=(233, 50),
                                              on_activate_call=lambda: self._edit_details(
                                                display_string=display_string,
                                                custom_tag=ba.textwidget(query=self._name_entry_field),
                                                root_widget=self._root_widget2))
            ba.containerwidget(edit=self._root_widget2, start_button=self._ok_button)
        except Exception: pass

    def _edit_details(self, display_string, custom_tag, root_widget):
        if not custom_tag:
            ba.screenmessage(message='Name cannot be empty',
                             color=(1,0,0))
            ba.playsound(ba.getsound('error'))
            return

        ba.containerwidget(edit=root_widget, transition='out_scale')
        friend = {'display string': display_string,
                  'custom tag': custom_tag}
        try:
            with open(main_path+'Friends.bsd', 'r') as file:
                old_file_text = file.readlines()
                for i, f in enumerate(old_file_text):
                    if display_string == json.loads(f)['display string']:
                        old_file_text[i] = json.dumps(friend)
                _old_file_text = old_file_text
                old_file_text = ''
                for f in _old_file_text:
                    if not f or f == '\n':
                        continue
                    f = f[0:-1] if f[-1] == '\n' else f
                    f = f[1:] if f[1] == '\n' else f
                    old_file_text += f+'\n'
                old_file_text = old_file_text[0:-1]
                file.close()
            with open(main_path+'Friends.bsd', 'w') as file:
                file.write(old_file_text)
                file.close()
            ba.screenmessage(message=f'{self._selected_friend} details changed succesfully',
                             color=(0,1,0))
            ba.playsound(ba.getsound('ding'))
            self._reload_friends()
        except Exception: pass

    def _confirm_remove_friend(self):
        try:
            if not self._selected_friend:
                return
            ConfirmWindow(text=f'Remove {self._selected_friend}?',
                          cancel_text='No', ok_text='Yes',
                          cancel_is_selected=True, action=self._remove_friend)
        except Exception: pass

    def _remove_friend(self):
        try:
            with open(main_path+'Friends.bsd', 'r') as file:
                _old_file_text = file.readlines()
                old_file_text = ''
                for f in _old_file_text:
                    f_ds = json.loads(f)['display string']
                    if not f or f == '\n' or f_ds == self._selected_friend:
                        continue
                    f = f[0:-1] if f[-1] == '\n' else f
                    f = f[1:] if f[1] == '\n' else f
                    old_file_text += f+'\n'
                old_file_text = old_file_text[0:-1]
                file.close()
            with open(main_path+'Friends.bsd', 'w') as file:
                file.write(old_file_text)
                file.close()
            self._selected_friend = ''
            ba.playsound(ba.getsound('shieldDown'))
            self._reload_friends()
        except Exception: pass

    def _back(self):
        ba.containerwidget(edit=self._root_widget, transition='out_scale')
        _ba.set_party_icon_always_visible(True)

class NewOnScreenKeyboardWindow:
    global paste
    def _new_init(self, textwidget: ba.Widget, label: str, max_chars: int):
        self._target_text = textwidget
        self._width = 700
        self._height = 400
        uiscale = ba.app.ui.uiscale
        top_extra = 20 if uiscale is ba.UIScale.SMALL else 0
        ba.Window.__init__(self, root_widget=ba.containerwidget(
                                 parent=_ba.get_special_widget('overlay_stack'),
                                 size=(self._width, self._height + top_extra),
                                 transition='in_scale',
                                 scale_origin_stack_offset=self._target_text.
                                 get_screen_space_center(),
                                 scale=(2.0 if uiscale is ba.UIScale.SMALL else
                                        1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
                                 stack_offset=(0, 0) if uiscale is ba.UIScale.SMALL else (
                                     0, 0) if uiscale is ba.UIScale.MEDIUM else (0, 0)))
        self._done_button = ba.buttonwidget(parent=self._root_widget,
                                            position=(self._width - 200, 44),
                                            size=(140, 60),
                                            autoselect=True,
                                            label=ba.Lstr(resource='doneText'),
                                            on_activate_call=self._done)
        ba.containerwidget(edit=self._root_widget,
                           on_cancel_call=self._cancel,
                           start_button=self._done_button)

        ba.textwidget(parent=self._root_widget,
                      position=(self._width * 0.5, self._height - 41),
                      size=(0, 0),
                      scale=0.95,
                      text=label,
                      maxwidth=self._width - 140,
                      color=ba.app.ui.title_color,
                      h_align='center',
                      v_align='center')

        self._text_field = ba.textwidget(
            parent=self._root_widget,
            position=(70, self._height - 116),
            max_chars=max_chars,
            text=cast(str, ba.textwidget(query=self._target_text)),
            on_return_press_call=self._done,
            autoselect=True,
            size=(self._width - 230, 55),
            v_align='center',
            editable=True,
            maxwidth=self._width - 270,
            force_internal_editing=True,
            always_show_carat=True)

        self._key_color_lit = (1.4, 1.2, 1.4)
        self._key_color = (0.69, 0.6, 0.74)
        self._key_color_dark = (0.55, 0.55, 0.71)

        self._paste_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(self._width-140, self._height - 115),
            label='Paste',
            button_type='square',
            size=(60, 50),
            color=self._key_color,
            textcolor=(1,1,1),
            on_activate_call=ba.Call(paste, field=self._text_field))

        self._shift_button: Optional[ba.Widget] = None
        self._backspace_button: Optional[ba.Widget] = None
        self._space_button: Optional[ba.Widget] = None
        self._double_press_shift = False
        self._num_mode_button: Optional[ba.Widget] = None
        self._emoji_button: Optional[ba.Widget] = None
        self._char_keys: list[ba.Widget] = []
        self._keyboard_index = 0
        self._last_space_press = 0.0
        self._double_space_interval = 0.3

        self._keyboard: ba.Keyboard
        self._chars: list[str]
        self._modes: list[str]
        self._mode: str
        self._mode_index: int
        self._load_keyboard()
    OnScreenKeyboardWindow.__init__ = _new_init

    def paste(field):
        ba.textwidget(edit=field, text=ba.textwidget(query=field) + ba.clipboard_get_text())

class NewGatherWindow:
    GatherWindow._old_init = GatherWindow.__init__
    def _new_init(self, transition: Optional[str] = 'in_right',
                  origin_widget: ba.Widget = None):
        self._old_init(transition=transition, origin_widget=origin_widget)
        uiscale = ba.app.ui.uiscale
        extra = (-75 if uiscale is ba.UIScale.SMALL else
            23 if uiscale is ba.UIScale.MEDIUM else 20)
        ba.buttonwidget(parent=self._root_widget,
                        button_type='square',
                        label='History',
                        size=(78,50),
                        position=(self._scroll_width-extra,self._scroll_height-15),
                        on_activate_call=ba.Call(HistoryWindow, 'in_scale'))
    GatherWindow.__init__ = _new_init

if config['Save History']:
    history_label_color = (0.83, 1, 0)
    history_date_text_color = (0,1,1)
    history_item_color = (1,1,1)
else:
    history_label_color = (0.70, 0.70, 0.70)
    history_date_text_color = (0.60,0.60,0.60)
    history_item_color = (0.35,0.35,0.35)
class HistoryWindow(ba.Window):
    def __init__(self, transition):
        self._uiscale = uiscale = ba.app.ui.uiscale
        self._width = width = (1300 if uiscale is ba.UIScale.SMALL else
            1100 if uiscale is ba.UIScale.MEDIUM else 1200)
        self._height = height = (800 if uiscale is ba.UIScale.SMALL else
            790 if uiscale is ba.UIScale.MEDIUM else 890)
        self._extra = extra = 300 if uiscale is ba.UIScale.SMALL else 0
        self._main_scale = 1.4 if uiscale is ba.UIScale.MEDIUM else 1.6
        
        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.0 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.70),
                         transition=transition))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         position=(width-width/1.9+extra/35, height/1.085-extra/4),
                                         text='History',
                                         scale=1.5,
                                         color=history_label_color)

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(100,100),
                                             size=(width-180-extra/18, height-220-extra/5),
                                             highlight=False)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)

        self._load_history()

        self._clear_history_button = ba.buttonwidget(parent=self._root_widget,
                                                     icon=ba.gettexture('textClearButton'),
                                                     label='Clear',
                                                     button_type='square',
                                                     size=(width/10, height/10),
                                                     position=(width/1.2-extra/4.4,
                                                        height/1.13-extra/4.4),
                                                     on_activate_call=self._confirm_clear_history)

        self._history_activation_button = ba.checkboxwidget(
            parent=self._root_widget,
            text='',
            scale=2,
            size=(35, 35),
            position=(width/1.33-extra/4.4,
                height/1.13-extra/4.4),
            value=config['Save History'],
            on_value_change_call=self._change_history_value)

        self._back_button = ba.buttonwidget(
            parent=self._root_widget,
            label='',
            position=(90, height-85-extra/5),
            size=(60, 60),
            scale=1.3,
            on_activate_call=ba.Call(ba.containerwidget, edit=self._root_widget, transition='out_scale'),
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

    def _load_history(self):
        try:
            with open(main_path+'History.bsd', 'r') as file:
                self._history = file.readlines()
                file.close()
            for i in self._history:
                self._history_info = json.loads(i)
                ba.textwidget(parent=self._subcontainer,
                              v_align='top',
                              h_align='center',
                              text=self._history_info['entry_time']+' --- '+self._history_info['time'],
                              size=(self._width-180-self._extra/18-250, 40),
                              corner_scale=1.3,
                              scale=1,
                              color=history_date_text_color,
                              maxwidth=self._width-180-self._extra/9-270)
                ba.textwidget(parent=self._subcontainer,
                              v_align='center',
                              text=f'Server: {self._history_info["server_name"]}',
                              size=(self._width-180-self._extra/18-250, 40),
                              corner_scale=1.3,
                              scale=1,
                              color=history_item_color,
                              maxwidth=self._width-180-self._extra/9-270,
                              selectable=True,
                              click_activate=True,
                              on_activate_call=ba.Call(_ba.connect_to_party,
                                address=self._history_info['server_ip'],
                                port=self._history_info['server_port'],
                                print_progress=self._history_info['print_progress']))
                ba.textwidget(parent=self._subcontainer,
                              v_align='center',
                              text=f'Replay: {self._history_info["time"]}',
                              size=(self._width-180-self._extra/18-250, 40),
                              corner_scale=1.3,
                              scale=1,
                              maxwidth=self._width-180-self._extra/9-270,
                              color=history_item_color,
                              selectable=True,
                              click_activate=True,
                              on_activate_call=ba.Call(self._watch_replay,
                                self._history_info['replay']))
                ba.textwidget(parent=self._subcontainer,
                              v_align='center',
                              text=f'Chat Log: {self._history_info["time"]}',
                              size=(self._width-180-self._extra/18-250, 40),
                              corner_scale=1.3,
                              scale=1,
                              maxwidth=self._width-180-self._extra/9-270,
                              color=history_item_color,
                              selectable=True,
                              click_activate=True,
                              on_activate_call=ba.Call(self._show_chat_log,
                                self._history_info['chat_log']))
                ba.textwidget(parent=self._subcontainer,
                              v_align='center',
                              h_align='center',
                              text='-'*500,
                              size=(self._width-180-self._extra/18-250, 40),
                              corner_scale=1.3,
                              scale=1,
                              maxwidth=self._width-180-self._extra/9-270)
        except Exception: pass

    def _reload_history(self):
        self._subcontainer.delete()
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)
        self._load_history()

    def _show_chat_log(self, chat_log_path):
        saved_chat_messages = open(chat_log_path, 'r').read()
        if not saved_chat_messages:
            ba.screenmessage('No chat messages')
            return
        self._root_widget2 = ba.containerwidget(
            size=(self._width, self._height),
            scale=(1.0 if self._uiscale is ba.UIScale.SMALL else
            0.80 if self._uiscale is ba.UIScale.MEDIUM else 0.70),
            transition='in_scale')

        self._title_text2 = ba.textwidget(parent=self._root_widget2,
                                          position=(self._width-self._width/1.9+self._extra/35,
                                            self._height/1.085-self._extra/4),
                                          text='Chat Log',
                                          scale=1.5,
                                          color=(0.83, 1, 0))

        self._scrollwidget2 = ba.scrollwidget(parent=self._root_widget2,
                                              position=(100,100),
                                              size=(self._width-180-self._extra/18,
                                                self._height-220-self._extra/5),
                                              highlight=False)
        self._subcontainer2 = ba.columnwidget(parent=self._scrollwidget2,
                                              selection_loops_to_parent=True)

        with open(chat_log_path) as file:
            chat_messages = file.readlines()
            file.close()
        for i in chat_messages:
            ba.textwidget(parent=self._subcontainer2,
                          text=i,
                          size=(0, 40),
                          maxwidth=self._height/0.92+self._extra/1.9,
                          scale=1.3)

        self._back_button2 = ba.buttonwidget(
            parent=self._root_widget2,
            label='',
            position=(90, self._height-85-self._extra/5),
            size=(60, 60),
            scale=1.3,
            on_activate_call=ba.Call(ba.containerwidget, edit=self._root_widget2, transition='out_scale'),
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget2, cancel_button=self._back_button2)

    def _change_history_value(self, *args):
        global history_label_color, history_date_text_color, history_item_color
        if config['Save History']:
            history_label_color = (0.70, 0.70, 0.70)
            history_date_text_color = (0.60,0.60,0.60)
            history_item_color = (0.35,0.35,0.35)
        else:
            history_label_color = (0.83, 1, 0)
            history_date_text_color = (0,1,1)
            history_item_color = (1,1,1)
        change_value('Save History', False)
        self._reload_history()
        self._title_text.delete()
        self._title_text = ba.textwidget(parent=self._root_widget,
                                         position=(self._width-self._width/1.9+self._extra/35,
                                            self._height/1.085-self._extra/4),
                                         text='History',
                                         scale=1.5,
                                         color=history_label_color)

    def _confirm_clear_history(self):
        if not os.path.exists(main_path+'History.bsd'):
            ba.screenmessage('History not found', color=(1,0,0))
            ba.playsound(ba.getsound('error'))
            return
        ConfirmWindow(text='Are you sure you want to clear the history?',
                      cancel_text='No', ok_text='Yes',
                      cancel_is_selected=True, action=self._clear_history)

    def _clear_history(self):
        replay_list = os.listdir(main_path+'History/Replays')
        for i in replay_list:
            try: os.unlink(main_path+'History/Replays/'+i)
            except Exception: pass
        
        chat_log_list = os.listdir(main_path+'History/ChatLog')
        for i in chat_log_list:
            try: os.unlink(main_path+'History/ChatLog/'+i)
            except Exception: pass

        try: os.unlink(main_path+'History.bsd')
        except Exception: pass
        self._reload_history()
        ba.playsound(ba.getsound('shieldDown'))

    def _watch_replay(self, replay_path):
        _ba.set_replay_speed_exponent(0)
        _ba.fade_screen(True)
        _ba.new_replay_session(replay_path)

def change_value(value, must_restart: bool, *args):
    config[value] = False if config[value] else True
    if must_restart:
        ba.screenmessage(message=ba.Lstr(resource='settingsWindowAdvanced.mustRestartText'),
                         color=(1.0, 0.5, 0.0))

old_connect_to_party = _ba.connect_to_party
def new_connect_to_party(address: str, port: int = 43210, print_progress: bool = True) -> None:
    global server_ip, server_port, _print_progress, entry_time
    entry_time = time.strftime('%m/%d/%Y ~ %X')
    server_ip = address
    server_port = port
    _print_progress = print_progress
    old_connect_to_party(server_ip, server_port, print_progress)
_ba.connect_to_party = new_connect_to_party

old_disconnect_from_host = _ba.disconnect_from_host
def _new_disconnect_from_host():
    _time = time.strftime('%m-%d-%Y ~ %H-%M-%S')
    replays_dir = _ba.get_replays_dir()
    if not os.path.exists(main_path + 'History'):
        os.mkdir(main_path + 'History')
    if not os.path.exists(main_path + 'History/Replays'):
        os.mkdir(main_path + 'History/Replays')
    if not os.path.exists(main_path + 'History/ChatLog'):
        os.mkdir(main_path + 'History/ChatLog')

    if config['Save History']:
        shutil.copyfile(src=replays_dir+'/__lastReplay.brp', dst=f'{main_path}History/Replays/{_time}')
        with open(f'{main_path}History/ChatLog/{_time}', 'w') as file:
            chat_messages = _ba.get_chat_messages()
            for i in chat_messages:
                file.write(i+'\n')
            file.close()
        _history = {'entry_time': entry_time,
                    'time': time.strftime('%m/%d/%Y ~ %X'),
                    'server_name': _ba.get_connection_to_host_info().get('name', False),
                    'server_ip': server_ip,
                    'server_port': server_port,
                    'print_progress': _print_progress,
                    'replay': f'{main_path}History/Replays/{_time}',
                    'chat_log': f'{main_path}History/ChatLog/{_time}'}
        try:
            with open(main_path + 'History.bsd', 'r') as file:
                old_file_text = file.read()
                file.close()
        except Exception: pass
        with open(main_path + 'History.bsd', 'w') as file:
            file.write(json.dumps(_history))
            try:
                if old_file_text:
                    file.write('\n'+old_file_text)
            except Exception: pass
            file.close()
    old_disconnect_from_host()
_ba.disconnect_from_host = _new_disconnect_from_host

def check_ping(ping):
    if _ba.get_connection_to_host_info().get('name', False):
        strPing = str(ping).split('.')
        ping_color = ((0,1,0) if int(strPing[0]) < 100 else
            (1,1,0) if int(strPing[0]) < 500 else (1,0,0))
        short_ping = strPing[0] + '.' + strPing[1][0:3]
        if config['Share Ping In Chat']:
            _ba.chatmessage(message=config['Ping Message'].replace('!', short_ping))
        else:
            ba.screenmessage(message=config['Ping Message'].replace('!', short_ping),
                             color=ping_color)
    else:
        ba.screenmessage('You are not on a server', color=(1,0,0))
        ba.playsound(ba.getsound('error'))

def show_plugin_settings_window(root_widget):
    ba.containerwidget(edit=root_widget, transition='out_scale')
    PluginSettingsWindow()

def confirm_show_bombsquad_builds():
    ConfirmWindow(text='Do you want to go to "BombSquad builds" page?',
                  cancel_text='No', ok_text='Yes',
                  action=show_bombsquad_builds)

def show_bombsquad_builds():
    ba.open_url('https://tools.ballistica.net/builds')

def is_latest_bs_version():
    try:
        if latest_bs_version == True:
            ba.screenmessage(message='You are using the latest version of BombSquad',
                             color=(0,1,0))
        elif latest_bs_version == False:
            ConfirmWindow(text='New BombSquad updates available!\nDo you want to go to "BombSquad builds" page?',
                          cancel_text='No', ok_text='Yes',
                          action=show_bombsquad_builds)
        elif latest_bs_version == None:
            ba.screenmessage(message='Please check your internet connection',
                             color=(1,0,0))
            ba.playsound(ba.getsound('error'))
    except Exception:
        ba.screenmessage(message='An unexpected error occurred while checking for updates', color=(1,0,0))
        ba.playsound(ba.getsound('error'))

def check_new_bs_version():
    global latest_bs_version
    bs_version = _ba.env().get('version')
    url = 'https://files.ballistica.net/bombsquad/builds/'
    try:
        latest_bs_builds = urllib.request.urlopen(url).read().decode('utf-8')
        if bs_version in latest_bs_builds:
            latest_bs_version = True
        else:
            latest_bs_version = False
    except Exception as e:
        if str(e) == '<urlopen error [Errno 11001] getaddrinfo failed>':
            latest_bs_version = None

    ba.pushcall(is_latest_bs_version, from_other_thread=True)

PlayerSpaz._old_init = PlayerSpaz.__init__
def _new_init(self,
              player: ba.Player,
              color: Sequence[float] = (1.0, 1.0, 1.0),
              highlight: Sequence[float] = (0.5, 0.5, 0.5),
              character: str = 'Spaz',
              powerups_expire: bool = True):
    self._old_init(player, color, highlight, character, powerups_expire)

    def emitSparkParticles():
        try:
            ba.emitfx(position=self.node.position,
                      velocity=self.node.velocity,
                      count=4,
                      scale=0.9,
                      spread=0.10,
                      chunk_type='spark',
                      tendril_type='smoke')
        except Exception:
            return

    def emitIceParticles():
        try:
            ba.emitfx(position=self.node.position,
                      velocity=self.node.velocity,
                      count=2,
                      scale=0.8,
                      spread=0.10,
                      chunk_type='ice',
                      tendril_type='smoke')
        except Exception:
            return

    def emitSlimeParticles():
        try:
            ba.emitfx(position=self.node.position,
                      velocity=self.node.velocity,
                      count=3,
                      scale=0.8,
                      spread=0.19,
                      chunk_type='slime')
        except Exception:
            return

    def emitSweatParticles():
        try:
            ba.emitfx(position=self.node.position,
                      velocity=self.node.velocity,
                      count=20,
                      scale=2,
                      spread=0.30,
                      chunk_type='sweat')
        except Exception:
            return

    if config['Spark Particles']:
        ba.timer(0.1, emitSparkParticles, repeat=True)
    if config['Ice Particles']:
        ba.timer(0.2, emitIceParticles, repeat=True)
    if config['Slime Particles']:
        ba.timer(0.2, emitSlimeParticles, repeat=True)
    if config['Sweat Particles']:
        ba.timer(0.2, emitSweatParticles, repeat=True)
PlayerSpaz.__init__ = _new_init

# def new_uiscale(self) -> None:
#     return ba.UIScale.LARGE
# ba._ui.UISubsystem.uiscale = new_uiscale

# ba_meta export plugin
class Plugin(ba.Plugin):
    def on_app_launch(self) -> None:
        if platform == 'windows' or platform == 'linux' or platform == 'mac':
            if config['Check For Updates']:
                start_new_thread(check_new_bs_version, ())
        app_starttime = time.time()

    """Bug Fixes"""
    AdvancedSettingsWindow._old_init = AdvancedSettingsWindow.__init__
    def _new_init(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
        self._old_init()
        ba.buttonwidget(edit=self._plugins_button,
                        on_activate_call=ba.Call(show_plugin_settings_window, self._root_widget))
    AdvancedSettingsWindow.__init__ = _new_init

    def _new_save_state(self):
        try:
            for tab in self._tabs.values():
                tab.save_state()

            sel = self._root_widget.get_selected_child()
            selected_tab_ids = [
                tab_id for tab_id, tab in self._tab_row.tabs.items()
                if sel == tab.button
            ]
            if sel == self._back_button:
                sel_name = 'Back'
            elif selected_tab_ids:
                assert len(selected_tab_ids) == 1
                sel_name = f'Tab:{selected_tab_ids[0].value}'
            elif sel == self._tab_container:
                sel_name = 'TabContainer'
            else:
                raise ValueError(f'unrecognized selection: \'{sel}\'')
            ba.app.ui.window_states[type(self)] = {
                'sel_name': sel_name,
            }
        except Exception:
            pass
    GatherWindow._save_state = _new_save_state

    GatherWindow._old_back = GatherWindow._back
    def _new_back(self):
        global gather_window_detected, show_mainmenu, in_server
        if gather_window_detected:
            gather_window_detected = False
            ba.containerwidget(edit=self._root_widget, transition='out_scale')
            if show_mainmenu:
                if not in_server:
                    show_mainmenu = False
                    in_server = False
                    MainMenuWindow(transition='in_left')
            else:
                ba.app.ui.set_main_menu_location('Main Menu')
        else:
            self._old_back()
        ba.timer(0.30, ba.Call(_ba.set_party_icon_always_visible, True))
    GatherWindow._back = _new_back