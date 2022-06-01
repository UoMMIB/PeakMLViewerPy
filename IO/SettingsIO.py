from lxml import etree as ET
import Logger as lg
import Utilities as u
import os

from Data.Settings import Settings

from typing import Tuple, List

def load_preference_decdp() -> int:

    settings_tree_data = None
    try:
            # If errors while attempt to read, requires conversion.
        with open(os.path.join(lg.current_directory,"settings.xml"), 'r', encoding='utf-8') as f:
            settings_tree_data = f.read()

    except Exception as err:
        lg.log_error(f'Unable to read preference "decdp" from settings xml: {err}')

    if settings_tree_data:
        settings_root = ET.fromstring(settings_tree_data)
        decdp = settings_root.find("./settings/decdp")
        if decdp is not None:
            return int(decdp.text)
        else:
            return 3
    else:
        return 3

def load_preference_defplot() -> str:

    settings_tree_data = None
    try:
            # If errors while attempt to read, requires conversion.
        with open(os.path.join(lg.current_directory,"settings.xml"), 'r', encoding='utf-8') as f:
            settings_tree_data = f.read()

    except Exception as err:
        lg.log_error(f'Unable to read preference "defplot" from settings xml: {err}')

    if settings_tree_data:
        settings_root = ET.fromstring(settings_tree_data)
        decdp = settings_root.find("./settings/defplot")
        if decdp is not None:
            return decdp.text
        else:
            return "Peak"
    else:
        return "Peak"

def load_preferences() -> List[Tuple[str, str]]:

    preferences = []
    settings_tree_data = None

    try:
            # If errors while attempt to read, requires conversion.
        with open(os.path.join(lg.current_directory,"settings.xml"), 'r', encoding='utf-8') as f:
            settings_tree_data = f.read()

    except Exception as err:
        lg.log_error(f'Unable to read preferences from settings xml: {err}')

    if settings_tree_data:
        settings_root = ET.fromstring(settings_tree_data)

        smooth = settings_root.find("./settings/smooth")
        if smooth is not None:
            preferences.append(("smooth", smooth.text))

        decdp = settings_root.find("./settings/decdp")
        if decdp is not None:
            preferences.append(("decdp", decdp.text))

        defplot = settings_root.find("./settings/defplot")
        if defplot is not None:
            preferences.append(("defplot", defplot.text))


    return preferences

def load_database_paths():

    database_paths = []
    frag_databases_type_1_paths = []
    frag_databases_type_2_paths = []
    settings_tree_data = None
    try:
            # If errors while attempt to read, requires conversion.
        with open(os.path.join(lg.current_directory,"settings.xml"), 'r', encoding='utf-8') as f:
            settings_tree_data = f.read()

    except Exception as err:
        lg.log_error(f'Unable to read database path preferences from settings xml: {err}')

    if settings_tree_data:
        settings_root = ET.fromstring(settings_tree_data)

        for database in settings_root.findall("./settings/databases/database"):
            database_paths.append(database.text)

        for database in settings_root.findall("./settings/fragDatabasesType1/fragDatabase"):
            frag_databases_type_1_paths.append(database.text)

        for database in settings_root.findall("./settings/fragDatabasesType2/fragDatabase"):
            frag_databases_type_2_paths.append(database.text)


    return [database_paths,frag_databases_type_1_paths,frag_databases_type_2_paths]

def write_settings(settings: Settings):

    try:

        peakmlviewer_node = ET.Element("peakmlviewer")
        settings_node = ET.SubElement(peakmlviewer_node,"settings")
        ET.SubElement(settings_node,"smooth").text = settings.get_preference_by_name("smooth")
        ET.SubElement(settings_node,"decdp").text = settings.get_preference_by_name("decdp")
        ET.SubElement(settings_node,"defplot").text = settings.get_preference_by_name("defplot")

        databases_node = ET.SubElement(settings_node,"databases")
        for database_path in settings.get_database_paths():
            ET.SubElement(databases_node,"database").text = database_path

        frag_databases_type_1_node = ET.SubElement(settings_node,"fragDatabasesType1")
        for database_path in settings.get_frag_databases_1_paths():
            ET.SubElement(frag_databases_type_1_node,"fragDatabase").text = database_path

        frag_databases_type_2_node = ET.SubElement(settings_node,"fragDatabasesType2")
        for database_path in settings.get_frag_databases_2_paths():
            ET.SubElement(frag_databases_type_2_node,"fragDatabase").text = database_path

        settings_str = u.prettify_xml(peakmlviewer_node)


        r = open(os.path.join(lg.current_directory,"settings.xml"), "w", encoding='utf-8')
        r.write(settings_str)
        r.close()

    except Exception as err:
        lg.log_error(f'Unable to write settings xml: {err}')
