# -*- coding: utf-8 -*-
# 0.2.0

import json
import os
import pathlib
import sys

class config ( object ):
    def __init__ ( self, controller = None ):
        super ( self.__class__, self ).__init__ ( )
        self.controller = controller

        self.values = {
            "app_name" : "SDTP",
            "mdi_auto_organizing" : True,
            "auto_updater_url" : "https://github.com/rcbrgs/sdtp/releases/download/0.9.0/",
            "chat_widget_show" : False,
            "chat_input_name" : "",
            "db_engine" : "sqlite",
            "database_widget_show" : True,
            "configuration_file_name" : "default.json",
            "database_file_name" : "sdtp_sqlite.db",
            "forbidden_countries" : [ "" ],
            "enable_per_country_bans" : False,
            "log_file_name" : "sdtp.log",
            "log_file_path" : "",
            "log_widget_show" : False,
            "log_show_debug" : False,
            "log_show_info" : False,
            "log_show_warning" : True,
            "log_show_error" : True,
            "log_show_critical" : True,
            "enable_lp" : True,
            "lp_interval" : 2,
            "metronomer_widget_show" : False,
            "enable_ping_limiter" : False,
            "max_ping" : 10000,
            "show_ping_limiter_window" : False,
            "show_players_window" : False,
            "sdtp_greetings" : "[SDTP] Seven Days To Py: started.",
            "sdtp_goodbye" : "[SDTP] Seven Days To Py: stopped.",
            "telnet_widget_show" : True,
            "telnet_password" : "BEWARE - PASSWORD WILL BE STORED UNENCRYPTED",
            "telnet_IP" : "127.0.0.1",
            "telnet_port" : 8081,
            "auto_connect" : False,
            # mods
            "mods_widget_show" : True,
            "enable_challenge" : False,
            "forbidden_countries_widget_show" : False,
            "ping_limiter_widget_show" : False,
            "show_challenge_window" : False,
            "players_control_widget_show" : True,
            "portals_widget_show" : False,
            "enable_auto_horde_portals" : False,
            "enable_player_portals" : False,
            "show_player_portals_window" : False,
            "max_portals_per_player" : 0,
            "portal_cost" : 0,
            "teleport_cost" : 0,
            "alarm_reboots_time" : -1,
            "enable_alarm_reboots" : False,
            "enable_frequency_reboots" : False,
            "frequency_reboots_interval" : 24,
            "latest_reboot" : 0,
            "server_empty_condition" : True,
            "server_reboots_widget_show" : False,
        }
        if os.name == "nt":
            self.values [ "workdir" ] = os.environ [ "ALLUSERSPROFILE" ]
            self.values [ "separator" ] = "\\\\"
        else:
            self.values [ "workdir" ] = os.path.expanduser ( "~" )
            self.values [ "separator" ] = "/"
        self.values [ "config_file" ] = "{}{}.{}_preconfig.json".format ( self.values [ "workdir" ], self.values [ "separator" ], self.values [ "app_name" ] )
        self.values [ "db_sqlite_file_path" ] = "{}{}.{}_default_db.sqlite".format ( self.values [ "workdir" ], self.values [ "separator" ], self.values [ "app_name" ] )

    def falsify ( self, key ):
        self.controller.log ( )
        self.values [ key ] = False

    def verify ( self, key ):
        self.controller.log ( )
        self.values [ key ] = True

    def get ( self, key ):
        try:
            return self.values [ key ]
        except:
            self.controller.log ( "error", "unable to find key '{}' among configuration values.".format ( key ) )
            return None

    def set ( self, key, value ):
        self.values [ key ] = value

    def load_configuration_file ( self ):
        try:
            preconfig_file = open ( self.get ( "config_file" ), "r" )
        except:
            self.controller.log ( "error", "Could not open the pre-configuration file {}.".format ( self.get ( "config_file" ) ) )
            return
        try:
            preconfig = json.load ( preconfig_file )
            for key in list ( preconfig.keys ( ) ):
                self.controller.log ( "debug", "config [ \"{}\" ] = {}".format ( key, preconfig [ key ] ) )
                self.values [ key ] = preconfig [ key ]
            self.controller.log ( "debug", "Loaded pre-configuration file." )
        except ValueError:
            self.controller.log ( "info", "Configuration file named '{}' is invalid. Using default values.".format ( self.get ( "config_file" ) ) )
            return

        try:
            config_file = open ( self.get ( "config_file" ), "r" )
        except IOError:
            self.controller.log ( "error", "Could not open the configuration file {}.".format ( self.get ( "config_file" ) ) )
            return
        try:
            final_config = json.load ( config_file )
            for key in list ( final_config.keys ( ) ):
                self.controller.log ( "debug", "config [ \"{}\" ] = {}".format ( key, final_config [ key ] ) )
                self.values [ key ] = final_config [ key ]
            self.controller.log ( "debug", "Loaded configuration file." )
        except ValueError:
            self.controller.log ( "info", "Configuration file named '{}' is invalid. Using default values.".format ( self.get ( "config_file" ) ) )

    def save_configuration_file ( self ):
        self.controller.log ( )

        self.controller.log ( "debug", "saving current configuration in '{}'.".format ( self.get ( "config_file" ) ) )
        config_file = open ( self.get ( "config_file" ), "w" )
        json.dump ( self.values, config_file )
        self.controller.log ( "debug", "Configuration file '{}' saved.".format ( self.get ( "config_file" ) ) )

    def toggle ( self, key ):
        self.controller.log ( )

        if self.values [ key ] == True:
            self.values [ key ] = False
            return
        if self.values [ key ] == False:
            self.values [ key ] = True
            return
        self.controller.log ( "error", "config.toggle ( {} ) called, but value for key is not a boolean.".format ( key ) )
