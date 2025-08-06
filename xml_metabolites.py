import xml.etree.ElementTree as ET

print("Script started...")

file = "/Users/nesarashree/Downloads/hmdb_metabolites.xml"

# Try loading the XML
try:
    context = ET.iterparse(file, events=("end",))
    print("XML file loaded successfully.")
except Exception as e:
    print("Error loading XML:", e)
    exit()

count_metabolites = 0
count_transporters = 0
slc_hits = []

for event, elem in context:
    if elem.tag.endswith("metabolite"):
        count_metabolites += 1

        name_elem = elem.find("{http://www.hmdb.ca}name")
        name = name_elem.text if name_elem is not None else "UNKNOWN"

        smiles_elem = elem.find("{http://www.hmdb.ca}smiles")
        smiles = smiles_elem.text if smiles_elem is not None else None

        bio_props = elem.find("{http://www.hmdb.ca}biological_properties")
        if bio_props is not None:
            for transporter in bio_props.findall("{http://www.hmdb.ca}transporter"):
                t_name_elem = transporter.find("{http://www.hmdb.ca}transporter_name")
                if t_name_elem is not None:
                    count_transporters += 1
                    t_name = t_name_elem.text
                    if any(slc in t_name for slc in ["SLC52A1", "SLC52A2", "SLC52A3"]):
                        slc_hits.append((name, smiles, t_name))

        elem.clear()  # Clear memory

        if count_metabolites % 1000 == 0:
            print(f"Parsed {count_metabolites} metabolites...")

print(f"Total metabolites parsed: {count_metabolites}")
print(f"Total transporters found: {count_transporters}")
print(f"Matches to SLC52: {len(slc_hits)}")
print(f"hello world I'm dying")
# Show first few hits
for hit in slc_hits[:10]:
    print(hit)
