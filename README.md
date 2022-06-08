# aas_transform
utility functions for transforming AAS serializations

# currently supported
* transform AAS XML files to JSON
* check AAS XML files to wrong/missing concept descriptions (wrong as in wrong ECLASS ID)

## setup (bash)
* create venv: ```python -m venv .venv```
* activate venv: ```source .venv/bin/activate```
* install dependencies: ```pip install -r requirements.txt```
* run: ```python transform.py```

## testing
* run on example.xml

properties:     
		
		line 57: ManufacturerName	with present semanticID: ConceptDescription with local IRDI (l.65)

		l. 75:   YearOfConstruction	with present semanticID: Property with non-local IRDI (l.80)
		
		l. 125:  Location 		with no semanticID

after check_conceptdesc:

		line 55: ManufacturerName	with present semanticID: ConceptDescription with global IRDI (l.63)

		l. 72:   YearOfConstruction	with present semanticID: ConceptDescription with global IRDI (l.77)
		
		l. 118:  Location 		with present semanticID: ConceptDescription with global IRDI (l.123)
