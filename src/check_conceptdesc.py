"""modifies wrong and adds missing concept descriptions to property submodels"""


import os
from aas import model
import aas.adapter.xml


CD_ID_DICT = {
	"Identification":"0173-1#01-AGZ247#010",
	"ManufacturerName" :"0173-1#02-AAO677#002",
	"SerialNumber": "0173-1#02-AAO607#001",
	"ProductCountryOfOrigin": "0173-1#02-AAE665#003",
	"YearOfConstruction": "0173-1#02-AAP906#001",
	"EvolutionStep": "0173-1#02-AAR710#001",
	"Location": "0173-1#02-ABA686#001",
	"PickUpSpot": "0173-1#02-BAF163#002",
	"Price": "0173-1#02-AAO739#001",
	"MinPressure": "0173-1#02-AAV623#002",
	"MaxPressure": "0173-1#02-AAJ549#002",
	"MinHeight": "0173-1#02-AAH915#004",
	"MaxHeight": "0173-1#02-AAH914#003",
	"MinWidth": "0173-1#02-AAH913#004",
	"MaxWidth": "0173-1#02-AAH912#003",
	"PositionAccuracy": "0173-1#02-AAM405#004",
	"StampingTime": "0173-1#02-AAQ203#001",
	"CycleTime": "0173-1#02-AAF891#003",
	"StoragePositions": "0173-1#02-AAR531#001",
	"StoredWPs": "0173-1#02-BAF551#003",
	"MinRange": "0173-1#02-AAV547#002",
	"MaxRange": "0173-1#02-AAV540#002",
	"LiftTime": "0173-1#02-AAJ500#003",
	"SkidSpeed": "0173-1#02-AAG967#004",
	"StartPoint": "0173-1#02-ABA686#001",
	"EndPoint": "0173-1#02-ABA686#001",
	"ConveyorSpeed": "0173-1#02-AAI045#003",
	"TwoWay": "0173-1#02-AAZ920#001",
	"Schedule": "0173-1#02-AAE840#006",
	"YearOfProduction": "0173-1#02-AAR972#002",
	"Priority": "",
}


def check_conceptdesc(aas_dir: str) -> None:
	""" modifies wrong and adds missing concept descriptions to property submodels

	:param aas_dir:	directory containing the aas files which are to be checked
		files need to be in XML format
	:return: None
	"""
	files = [os.path.join(aas_dir, f) for f in os.listdir(aas_dir) if os.path.isfile(os.path.join(aas_dir, f)) and f.split('.')[-1] == "xml"]
	for f in files:
		preprocess(f)
		with open(f, 'rb') as xml_file:
			data: model.AbstractObjectStore = aas.adapter.xml.read_aas_xml_file(xml_file)
			for obj in data:
				if isinstance(obj, model.Submodel):
					for element in obj.submodel_element:
						if isinstance(element, model.Property):
							new_semantic_id = model.Reference(
								(model.Key(
									type_ = model.KeyElements.CONCEPT_DESCRIPTION,
									local = False,
									value = CD_ID_DICT[element.id_short],
									id_type = model.KeyType.IRDI
								),)
							)
							element.semantic_id = new_semantic_id
		new_file_name = "../res_new/" + f.split("/")[-1]
		with open(new_file_name, 'wb') as xml_file:
			aas.adapter.xml.write_aas_xml_file(xml_file, data)
		print(f"Successfully checked/modified/added concept descriptions for {f}")


def preprocess(in_path: str) -> None:
	with open(in_path, 'r') as file :
		filedata = file.read()
	filedata = filedata.replace('REAL_MEASURE', 'decimal')
	filedata = filedata.replace('True', 'true')
	with open(in_path, 'w') as f:
		f.write(filedata)



if __name__ == "__main__":
	in_path = "../res/"
	check_conceptdesc(in_path)
