import sublime, sublime_plugin
import re
import os

from Default import history_list


class DlangAutoModuleNameCommand( sublime_plugin.TextCommand ):
    def _check_exists( self, edit ):
        # check "module ..."
        regions = self.view.find_all( r"^module\s.*" )

        if regions:
            return regions[ 0 ].b

    def _get_module_name_from_class( self ):
        # grep "class ..."
        extracts = []
        regions = self.view.find_all( r"^class\s[.]*(\w+)", 0, r"\1", extracts )

        if extracts:
            return extracts[ 0 ].lower()


    def _get_module_name_from_interface( self ):
        # grep "class ..."
        extracts = []
        regions = self.view.find_all( r"^interface\s[.]*(\w+)", 0, r"\1", extracts )

        if extracts:
            return extracts[ 0 ].lower()


    def _get_module_name_from_struct( self ):
        # grep "class ..."
        extracts = []
        regions = self.view.find_all( r"^struct\s[.]*(\w+)", 0, r"\1", extracts )

        if extracts:
            return extracts[ 0 ].lower()


    def _get_module_name( self ):
        name = self._get_module_name_from_class()
        if name:
            return name

        name = self._get_module_name_from_interface()
        if name:
            return name

        name = self._get_module_name_from_struct()
        if name:
            return name


    def _at_top( self, edit, name ):
        # at top in file
        insert_string = "module {};\n\n".format( name )

        self.view.insert( edit, 0, insert_string )

        return len( "module " )


    def _select( self, sel_i ):
        sel = self.view.sel()
        sel.clear()
        sel.add( sublime.Region( sel_i, sel_i ) )

        # scroll t show it
        self.view.show( sel_i )


    def run(self, edit, **args):
        history_list.get_jump_history_for_view(self.view).push_selection(self.view)

        # Check 
        exist_point = self._check_exists( edit )
        if exist_point:
            self._select( exist_point )
            return

        # Get Name
        name = self._get_module_name()
        if name:
            inserted = self._at_top( edit, name )

            # Select inserted
            if inserted is not None:
                self._select( inserted )
