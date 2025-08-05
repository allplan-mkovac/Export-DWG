"""
Script for BatchExportDWG
"""
from typing import TYPE_CHECKING, Any, cast

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtils

import os
import xml.etree.ElementTree as ET
from BuildingElement import BuildingElement
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from BuildingElementListService import BuildingElementListService
from NemAll_Python_AllplanSettings import AllplanPaths
from datetime import datetime
from NemAll_Python_BaseElements import ProjectAttributeService
from BaseInteractor import BaseInteractor, BaseInteractorData
if TYPE_CHECKING:
    from __BuildingElementStubFiles.EventsBuildingElement import EventsBuildingElement
else:
    EventsBuildingElement = BuildingElement

print('Load ExportDWG.py')


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    """
    Creation of element (only necessary for the library preview)

    Args:
        build_ele: the building element.
        doc:       input document
    """

    del build_ele
    del doc

    com_prop = AllplanBaseElements.CommonProperties()

    com_prop.GetGlobalProperties()

    text_prop = AllplanBasisElements.TextProperties()

    model_ele_list = [AllplanBasisElements.TextElement(com_prop, text_prop, "DWG Export", AllplanGeo.Point2D(0, 100))]

    return (model_ele_list, None, None)


def create_interactor(interactor_data: BaseInteractorData) -> "ExportDWG":
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return ExportDWG(interactor_data)


class ExportDWG(BaseInteractor):
    """
    Definition of class ExportImportInteractor
    """

    def __init__(self, interactor_data: BaseInteractorData):
        """
        Initialization of class ExportImportInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """
        self.coord_input = interactor_data.coord_input
        self.build_ele_list = interactor_data.build_ele_list
        
        self.build_ele = cast(EventsBuildingElement, interactor_data.build_ele_list[0])
        self.esc_pressed = False

        # initialize the point input
        input_control_data = AllplanIFW.ValueInputControlData(AllplanIFW.eValueInputControlType.eTEXT_EDIT, False)
        user_prompt = AllplanIFW.InputStringConvert("See infos printed in trace")
        interactor_data.coord_input.InitFirstPointValueInput(user_prompt, input_control_data)
        
        # initialize the palette
        self.palette_service = BuildingElementPaletteService(interactor_data.build_ele_list,
                                                             interactor_data.build_ele_composite,
                                                             self.build_ele.script_name,
                                                             interactor_data.control_props_list,
                                                             self.build_ele.pyp_file_name)

        self.palette_service.show_palette(self.build_ele.pyp_file_name)


    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """

        # build_ele = build_ele_list[0]

        doc = self.coord_input.GetInputViewDocument()

        def parse_xml(filename):
            tree = ET.parse(filename)
            root = tree.getroot()

            id_list = []
            state_list = []
            activated_list = []

            for entry in root.findall('.//File'):
                id_value = entry.get('ID')
                state_value = entry.get('State')
                activated_value = entry.get('Activated')

                id_list.append(id_value)
                state_list.append(state_value)
                activated_list.append(activated_value)

            return id_list, state_list , activated_list

        #----------------- export the drawing file
        now = datetime.now()
        actual_date = now.strftime('%Y-%m-%d %H%M%S')

        project_path=AllplanPaths.GetCurPrjPath()

        project_name_list = ProjectAttributeService.GetAttributesFromCurrentProject()
        project_name_list = dict(project_name_list)
        project_name = project_name_list [405]
        # print(project_name)

        # directory_path = build_ele.directory_input.value
        directory_path = project_path+"BIM\\"+self.build_ele.directory_input.value

        if event_id == 1001:
            files = os.listdir(directory_path)

            x=0
            while x < len(files):
                drawing_file_serv = AllplanBaseElements.DrawingFileService()
                drawing_file_serv.UnloadAll(doc)


                file_name=files[x]
                if file_name.endswith(".xml"):  # Filter for .xml files
                    file_path = os.path.join(directory_path, file_name)
                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, 'r') as file:
                                content = file.read()
                                print(f"Contents of {file_name}:")
                                print(content)

                                # Parse XML content
                                ids, states , actives = parse_xml(file_path)

                                file_index = ids
                                file_status = states
                                file_active = actives

                                print(f"Fólie: {file_index}")
                                print(f"Statusy: {file_status}")
                                print(f"Aktivovány: {file_active}")

                                i=0
                                while i < len(file_index):
                                    if int(file_status [i])> 0 and int(file_active [i])> 0 :
                                        drawing_file_serv.LoadFile(doc, int (file_index [i]), AllplanBaseElements.DrawingFileLoadState.ActiveForeground)
                                        print(f"open file {file_index [i]}")

                                    i+=1


                                file_name_no_extension = file_name.split('.xml')[0]
                                exported_dwg_name=self.build_ele.DwgDrawingFilePath.value+project_name+"\\"+actual_date+"\\"+file_name_no_extension+".dwg"
                                theme_file = self.build_ele.ConfigFile.value
                                print (theme_file)
                                drawing_file_serv.ExportDWGByTheme(doc, exported_dwg_name, theme_file, version=2018)



                        except Exception as e:
                            print(f"Error opening {file_name}: {e}")
                    else:
                        print(f"{file_name} is not a file.")
                else:
                    print(f"{file_name} is not an XML file.")
                x+=1


            AllplanUtils.ShowMessageBox("Export všech DWG ze seznamu \n"+directory_path+"\ndo složky \n"+self.build_ele.DwgDrawingFilePath.value+project_name+"\\"+actual_date+"\nbyl úspěšný",0)

    def process_mouse_msg(self,
                            mouse_msg: int,
                            pnt      : AllplanGeo.Point2D,
                            msg_info : AllplanIFW.AddMsgInfo) -> bool:
            """ Handle the event of mouse sending a message (being moves, clicked, etc...)

            Args:
                mouse_msg:  The mouse message.
                pnt:        The input point in view coordinates. The origin is the mid point of the viewport
                msg_info:   additional message info.

            Returns:
                True/False for success.
            """

            return True
        
    def modify_element_property(self,
                                page : int,
                                name : str,
                                value: Any):
        """Handle the event of changing an element property in the property palette

        Args:
            page:   Page of the modified property
            name:   Name of the modified property.
            value:  New value of the modified property.
        """
        self.palette_service.modify_element_property(page,name,value)
        self.palette_service.update_palette(-1,False)


    def set_active_palette_page_index(self, active_page_index: int) -> None:
        """Handle the event of changing the tab of the property palette

        Args:
            active_page_index: index of the switched page, starting from 0
        """


    def on_mouse_leave(self):
        """ Handle the event of mouse leaving the viewport."""


    def on_preview_draw(self):
        """ Handles the preview draw event.

        This event is triggered e.g., when an input in the dialog line is done (e.g. input of a coordinate).
        """


    def on_value_input_control_enter(self) -> bool:
        """ Handle the event of hitting the enter key during the input in the dialog line.

        Returns:
            True/False for success.
        """

        return True

    def on_shortcut_control_input(self,
                                  value: int) -> bool:

        return True

    def execute_save_favorite(self,
                              file_name: str) -> None:
        BuildingElementListService.write_to_file(file_name, self.build_ele_list)


    def execute_load_favorite(self,
                              file_name: str) -> None:
        BuildingElementListService.read_from_file(file_name, self.build_ele_list)

        self.palette_service.update_palette(-1, True) 

    def reset_param_values(self,
                           build_ele_list: list[BuildingElement]) -> None:
        BuildingElementListService.reset_param_values(self.build_ele_list) 

        self.palette_service.update_palette(-1, True) 

    def update_after_favorite_read(self) -> None:

        self.palette_service.update_palette(-1, True)
    
    def on_cancel_function(self) -> bool:
        
        self.palette_service.close_palette()

        return True
    
    def __del__(self):
        BuildingElementListService.write_to_default_favorite_file(self.build_ele_list)