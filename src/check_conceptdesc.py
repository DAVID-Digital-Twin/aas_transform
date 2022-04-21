import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

CD_ID_DICT ={"Identification":"0173-1#01-AGZ247#010","ManufacturerName":"0173-1#02-AAO677#002","SerialNumber":"0173-1#02-AAO607#001",
"ProductCountryOfOrigin":"0173-1#02-AAE665#003","YearOfConstruction":"0173-1#02-AAP906#001","EvolutionStep":"0173-1#02-AAR710#001",
"Location":"0173-1#02-ABA686#001","PickUpSpot":"0173-1#02-BAF163#002","Price":"0173-1#02-AAO739#001","MinPressure":"0173-1#02-AAV623#002",
"MaxPressure":"0173-1#02-AAJ549#002","MinHeight":"0173-1#02-AAH915#004","MaxHeight":"0173-1#02-AAH914#003","MinWidth":"0173-1#02-AAH913#004",
"MaxWidth":"0173-1#02-AAH912#003","PositionAccuracy":"0173-1#02-AAM405#004","StampingTime":"0173-1#02-AAQ203#001","CycleTime":"0173-1#02-AAF891#003",
"StoragePositions":"0173-1#02-AAR531#001","StoredWPs":"0173-1#02-BAF551#003","MinRange":"0173-1#02-AAV547#002","MaxRange":"0173-1#02-AAV540#002",
"LiftTime":"0173-1#02-AAJ500#003","SkidSpeed":"0173-1#02-AAG967#004","StartPoint":"0173-1#02-ABA686#001","EndPoint":"0173-1#02-ABA686#001",
"ConveyorSpeed":"0173-1#02-AAI045#003","TwoWay":"0173-1#02-AAZ920#001","Schedule":"0173-1#02-AAE840#006","YearOfProduction":"0173-1#02-AAR972#002","Priority":""}

ns = {'aas': 'http://www.admin-shell.io/aas/2/0'} #namespaces dictionary 

def check_conceptdesc (aas_dir: str) -> None: 
    """modifies wrong and adds missing concept descriptions to property submodels in an AAS
    Args:
        aas_dir (str): The directory which contains the aas files which are to be checked. Files need to be in XML format

    Returns:
        None
    """

    files = [os.path.join(aas_dir, f) for f in os.listdir(aas_dir) if os.path.isfile(os.path.join(aas_dir, f)) and f.split('.')[-1] == "xml"]
    ET.register_namespace('aas','http://www.admin-shell.io/aas/2/0')
    for f in files:
        xml_tree = ET.parse(f)
        root = xml_tree.getroot()
        submodels = root.findall('./aas:submodels/aas:submodel', ns)   # list of all submodels, list contains Elements
        for submodel in submodels:
            properties = submodel.findall('./aas:submodelElements/aas:submodelElement/aas:property', ns)
            for property_sm in properties:
                property_name = property_sm.find('aas:idShort', ns).text 
                semantic_id_sm = None
                semantic_id_sm = property_sm.find('aas:semanticId', ns)
                if semantic_id_sm == None:
                    semantic_id_sm =  ET.SubElement(property_sm, "aas:semanticId")
                    keys_sm = ET.SubElement(semantic_id_sm, "aas:keys")
                    key_sm = ET.SubElement(keys_sm, "aas:key", {"type":"ConceptDescription", "local":"false", "idType":"IRDI"})
                    key_sm.text = CD_ID_DICT[property_name]
                else:
                    keys_sm = None
                    keys_sm = semantic_id_sm.find('aas:keys', ns)
                    if keys_sm == None:
                        keys_sm = ET.SubElement(semantic_id_sm, "aas:keys")
                        key_sm = ET.SubElement(keys_sm, "aas:key", {"type":"ConceptDescription", "local":"false", "idType":"IRDI"})
                        key_sm.text = CD_ID_DICT[property_name]
                    else:
                        key_sm = None
                        key_sm = keys_sm.find('aas:key', ns)
                        if key_sm == None:
                            key_sm = ET.SubElement(keys_sm, "aas:key", {"type":"ConceptDescription", "local":"false", "idType":"IRDI"})
                            key_sm.text = CD_ID_DICT[property_name]
                        else:
                            key_type = key_sm.get("type")
                            if key_type != "ConceptDescription":
                                key_sm.set("type", "ConceptDescription")
                            key_local = key_sm.get("local")
                            if key_local != "false":
                                key_sm.set("local", "false")
                            key_idtype = key_sm.get("idType")
                            if key_idtype != "IRDI":
                                key_sm.set("idType", "IRDI")
                            key_idtype_text = None
                            key_idtype_text = key_sm.text
                            if key_idtype_text == None:
                                key_sm.text = CD_ID_DICT[property_name]
                            if " " in key_idtype_text or key_idtype_text != CD_ID_DICT[property_name]:
                                key_sm.text = CD_ID_DICT[property_name]
        new_file_name = "res_new/" + f.split("/")[-1]
        xml_tree.write(new_file_name)
        #xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        #with open(f, "w") as new_file:
        #    new_file.write(xmlstr)
        print(f"Successfully checked/modified/added concept descriptions for {f}")

if __name__ == "__main__":
    in_path = "../res/"
    check_conceptdesc(in_path)
