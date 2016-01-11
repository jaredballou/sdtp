# -*- coding: utf-8 -*-

from PyQt4 import QtCore
#from PySide import QtCore
import re
import socket
import sys
import telnetlib
import time
import threading

class telnet ( QtCore.QThread ):

    connectable = QtCore.pyqtSignal ( )
    disconnectable = QtCore.pyqtSignal ( )
    
    def __init__ ( self, controller ):
        super ( self.__class__, self ).__init__ ( )

        self.controller = controller
        self.keep_running = True

        self.auto_connect = False
        self.connectivity_level = 0
        self.latest_handshake = 0
        self.output_matchers = [ re.compile ( b'^.*\n' ),
                                 re.compile ( b'^Day [\d]+, [\d]{2}:[\d]{2} ' ),
                                 re.compile ( b'Total of [\d]+ in the game' ) ]
        self.telnet = None

    def run ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )

        self.controller.dispatcher.register_callback ( "password incorrect", self.close_connection_wrapper )

        while ( self.keep_running ):

            if ( not self.check_connection ( ) ):
                time.sleep ( 1 )
                continue

            line = self.chomp ( )
            if line == '':
                continue

            try:
                line_string = ""
                if line:
                    line_string = line.decode ( 'utf-8' )
                    line_string = line_string.strip ( )
            except Exception as e:
                self.controller.log ( "error", "Error {} while processing line.decode ( '{}' )".format ( e, line ) )
                
            self.controller.log ( "debug", prefix + " " + line_string )
            self.controller.parser.enqueue ( line_string )

        self.close_connection ( )
        self.controller.log ( "info", prefix + " returns." )
        
    def stop ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )

        self.keep_running = False

    # Connection methods
    ####################
        
    def check_connection ( self ):
        """
        Should return True if everything is fine with the connection.
        Do not rely on metadata for this; this function is supposed to be reliable, and the metadata set according to its results.
        """

        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "debug", prefix + " ( )".format ( ) )

        if self.controller.config.values [ "auto_connect" ]:
            self.open_connection ( )

        if self.connectivity_level != 2:
            return False
        if self.telnet == None:
            return False
        if not isinstance ( self.telnet.get_socket ( ), socket.socket ):
            return False
        return True

    def close_connection ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )

        if self.connectivity_level == 2:
            self.handshake_bye ( )
        self.controller.telnet_ongoing = False
        self.telnet = None
        self.connectivity_level = 0
        self.connectable.emit ( )

    def handshake_bye ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )
        
        self.write ( "exit" )
        self.telnet.close ( )
        self.connectivity_level = 1
        self.controller.log ( "info", prefix + " Telnet connection closed." )

    def close_connection_wrapper ( self, match_groups ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )
        
        self.close_connection ( )

    def create_telnet_object ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )

        self.telnet = telnetlib.Telnet ( timeout = 10 )
        if self.telnet != None:
            self.connectivity_level = 1
        
        self.controller.log ( "info", prefix + " telnet step 1 completed" )
        
    def handshake_hi ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "info", prefix + " ( )".format ( ) )

        if time.time ( ) - self.latest_handshake < 10:
            self.controller.log ( "info", prefix + " sleeping 10 seconds before attempting to connect again." )
            time.sleep ( 10 )

        self.latest_handshake = time.time ( )
            
        try:
            self.telnet.open ( self.controller.config.values [ 'telnet_IP' ], self.controller.config.values [ 'telnet_port' ], timeout = 5 )
            self.telnet.read_until ( b"Please enter password:" )
            self.controller.log ( "info", prefix + " password requested by server." )
            self.write ( self.controller.config.values [ 'telnet_password' ] )
            self.controller.log ( "info", prefix + " password was sent to server." )
        except Exception as e:
            self.controller.log ( "error", prefix + " Error while opening connection: %s." % str ( e ) )
            return

        self.controller.log ( "info", prefix + " waiting for 'Logon successful'" )
        try:
            linetest = self.telnet.read_until ( b'Logon successful.' )
        except Exception as e:
            self.controller.log ( "error", prefix + " linetest exception: {}.".format ( e ) )
            return
            
        if b'Logon successful.' in linetest:
            self.controller.log ( "info", prefix + linetest.decode ( 'utf-8' ) )
            self.controller.log ( "info", prefix + " Telnet connected successfully." )
        else:
            self.controller.log ( "error", prefix + " Logon failed.")
            return
        
        self.controller.log ( "info", prefix + " Telnet step 2 completed." )
        self.connectivity_level = 2
        
    def open_connection ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "debug", prefix + " ( )".format ( ) )

        if self.connectivity_level == 2:
            self.controller.log ( "debug", prefix + " attempted to re-open connection, ignoring call." )
            return
        if self.connectivity_level == 0:
            self.create_telnet_object ( )
        if self.connectivity_level == 1:
            self.handshake_hi ( )
            
        if self.connectivity_level != 2:
            self.controller.log ( "warning", prefix + " open_connection failed." )
            self.close_connection ( )
            return
        
        self.controller.telnet_ongoing = True
        self.disconnectable.emit ( )

    # I/O methods
    #############
    
    def chomp ( self ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "debug", prefix + " ( )".format ( ) )

        try:
            result = self.telnet.expect ( self.output_matchers, 5 )
            if len ( result ) == 3:
                line = result [ 2 ]
                if result [ 0 ] == -1:
                    if result [ 2 ] != b'':
                        self.controller.log ( "debug", "expect timed out on '{}'.".format ( result [ 2 ] ) )
                        return
                elif result [ 0 ] != 0:
                    self.controller.log ( "info",  "output_matcher [ {} ] hit".format ( result [ 0 ] ) )
        except EOFError as e:
            self.controller.log ( "warning", "chomp EOFError '{}'.".format ( e ) )
            self.close_connection ( )
            return
        except Exception as e:
            if not self.check_connection ( ):
                self.controller.log ( "warning", "chomp had an exception, because the connection is off." )
                self.close_connection ( )
                return
            if "[Errno 104] Connection reset by peer" in str ( e ):
                self.controller.log ( "warning", "chomp: game server closed the connection." )
                self.close_connection ( )
                return
            self.controller.log ( "error", "Exception in chomp: {}, sys.exc_info = '{}'.".format ( e, sys.exc_info ( ) ) )
            self.controller.log ( "error", "type ( self.telnet ) == {}".format ( type ( self.telnet ) ) )
            self.controller.log ( "error", "isinstance ( self.telnet.get_socket ( ), socket.socket ) = {}".format ( self.check_connection ( ) ) )
            self.close_connection ( )
            return
        
        return line
    
    def write ( self, input_msg ):
        prefix = "{}.{}".format ( self.__class__.__name__, sys._getframe().f_code.co_name )
        self.controller.log ( "debug", prefix + " ( {} )".format ( input_msg ) )

        if self.connectivity_level == 0:
            self.controller.log ( "info", prefix + " ignoring attempt to write  with level 0 connectivity." )
            return
        
        if self.connectivity_level == 1:
            self.controller.log ( "info", prefix + " writing with level 1 connectivity." )
        
        self.controller.log ( "debug", prefix + " type ( input_msg ) == {}".format ( type ( input_msg ) ) )

        try:
            msg = input_msg + "\n"
        except Exception as e:
            self.controller.log ( "error", prefix + " newline exception: {}".format ( e ) )
            return

        self.controller.log ( "debug", prefix + " raw write" )
        try:
            self.telnet.write ( msg.encode ( "utf8", "replace" ) )
        except Exception as e:
            self.controller.log ( "error", "telnet.write had exception: {}".format ( e ) )
            return

        self.controller.log ( "debug", prefix + " message written." )