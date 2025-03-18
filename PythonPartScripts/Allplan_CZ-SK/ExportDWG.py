"""
Script for ExportImportInteractor
"""

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtils

import os
import xml.etree.ElementTree as ET

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService
from NemAll_Python_AllplanSettings import AllplanPaths
from datetime import datetime
from NemAll_Python_BaseElements import ProjectAttributeService

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


def create_interactor(coord_input, pyp_path, str_table_service):
    """
    Create the interactor

    Args:
        coord_input:        coordinate input
        pyp_path:           path of the pyp file
        str_table_service:  string table service
    """

    return ExportImportInteractor(coord_input, pyp_path, str_table_service)


class ExportImportInteractor():
    """
    Definition of class ExportImportInteractor
    """

    def __init__(self, coord_input, pyp_path, str_table_service):
        """
        Initialization of class ExportImportInteractor

        Args:
            coord_input:        coordinate input
            pyp_path:           path of the pyp file
            str_table_service:  string table service
        """

        self.coord_input       = coord_input
        self.pyp_path          = pyp_path
        self.str_table_service = str_table_service
        self.model_ele_list    = None
        self.build_ele_service = BuildingElementService()


        #----------------- read the data and show the palette

        result, self.build_ele_script, self.build_ele_list, self.control_props_list,    \
            self.build_ele_composite, part_name, self.file_name = \
            self.build_ele_service.read_data_from_pyp(pyp_path + "\\ExportDWG.pal", self.str_table_service.str_table, False,
                                                      self.str_table_service.material_str_table)




        if not result:
            return

        self.palette_service = BuildingElementPaletteService(self.build_ele_list, self.build_ele_composite,
                                                             self.build_ele_script,
                                                             self.control_props_list, self.file_name)

        self.palette_service.show_palette(part_name)



        #----------------- get the properties and start the input

        self.com_prop = AllplanBaseElements.CommonProperties()

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Execute by button click"))


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        if update_palette:
            self.palette_service.update_palette(-1, False)


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """

        build_ele = self.build_ele_list[0]

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
        directory_path = project_path+"BIM\\"+build_ele.directory_input.value

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
                                exported_dwg_name=build_ele.DwgDrawingFilePath.value+project_name+"\\"+actual_date+"\\"+file_name_no_extension+".dwg"
                                theme_file = build_ele.ConfigFile.value
                                print (theme_file)
                                drawing_file_serv.ExportDWGByTheme(doc, exported_dwg_name, theme_file, version=2018)



                        except Exception as e:
                            print(f"Error opening {file_name}: {e}")
                    else:
                        print(f"{file_name} is not a file.")
                else:
                    print(f"{file_name} is not an XML file.")
                x+=1


            AllplanUtils.ShowMessageBox("Export všech DWG ze seznamu \n"+directory_path+"\ndo složky \n"+build_ele.DwgDrawingFilePath.value+project_name+"\\"+actual_date+"\nbyl úspěšný",0)







    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        return True
