import numpy as np

class Genus:
    
    def __init__(self):
        pass

    def get_genus(self, biological_type, evolutionary_stage):
        if biological_type not in self.lifeform_genus_data:
            return "Exotic"
        probabilities = list(self.lifeform_genus_data[biological_type][evolutionary_stage].values())
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        names = list(self.lifeform_genus_data[biological_type][evolutionary_stage].keys())
        return np.random.choice(names, p=probabilities)

    flora_genus = {
        "Single-celled organisms": {
                "Chlorella": 1.0,
                "Volvox": 1.0,
                "Diatoms": 1.0,
                "Cyanobacteria": 1.0,
                "Spirulina": 1.0,
        },
        "Multi-celled organisms": {
            "Mosses": 1.0,
            "Liverworts": 1.0,
            "Hornworts": 1.0,
            "Ferns": 1.0,
            "Horsetails": 1.0,
            "Bryophytes" : 1.0,
            "Conifers": 1.0,
            "Cycads": 1.0,
            "Gymnosperms": 1.0,
        },
        "Complex lifeforms": {
            "Monocots (e.g., Grasses, Orchids)": 1.0,
            "Dicots (e.g., Roses, Sunflowers)": 1.0,
            "Woody Plants (Trees, Shrubs)": 1.0,
            "Herbaceous Plants (Non-woody Plants)": 1.0,
        }
    }

    # More speciiic life form concepts -- to supply LLM prompts
    lifeform_genus_data = {
        "Terrestrial": {
            "Single-celled organisms": {
                "Bacteria": 1.0, 
                "Archaea": 1.0,
                "Protozoa": 1.0,
                "Unicellular Fungi (e.g., Yeasts)": 1.0,
                "Protists (e.g., Amoebas, Slime Molds)": 1.0,
                "Choanoflagellates": 1.0,
                "Ciliates (such as Paramecium)": 1.0,
                "Flagellates (e.g., Euglena)": 1.0,
            },
            "Multi-celled organisms": {
                "Fungi": 1.0,
                "Molds": 1.0,
                "Mildews": 1.0,
                "Yeast": 1.0,
                "Simple Annelids": 1.0,  
            },
            "Complex lifeforms": {
                "Mammals": 1.0,
                "Birds": 1.0,
                "Reptiles": 1.0,
                "Amphibians": 1.0,
                "Fish": 1.0,
                "Coleoptera (Beetles)": 1.0,
                "Lepidoptera (Butterflies and Moths)": 1.0,
                "Hymenoptera (Bees, Wasps, Ants)": 1.0,
                "Diptera (Flies)": 1.0,
                "Hemiptera (True Bugs)": 1.0,
                "Odonata (Dragonflies)": 1.0,
                "Orthoptera (Grasshoppers)": 1.0,
                "Araneae (Spiders)": 1.0,
                "Gastropoda (Snails)": 1.0,
                "Isoptera (Termites)": 1.0,
                "Lagomorpha (Rabbits)": 1.0,
                "Mantodea (Praying Mantises)": 1.0,
                "Blattodea (Cockroaches)": 1.0,
                "Myriapods": 1.0,
                "Arachnids": 1.0,
                "Arachnids": 1.0,
                "Felines": 1.0,
                "Canines": 1.0,
                "Primates": 1.0,
                "Rodents": 1.0,
                "Bovines": 1.0,
                "Equines": 1.0,
                "Porcines": 1.0,
                "Avians": 1.0,
                "Annelids": 1.0,
                "Mollusks": 1.0,
            }
        },
        "Aquatic": {
            "Single-celled organisms": {
                "Phytoplankton (e.g., Diatoms, Dinoflagellates)": 1.0,
                "Green Algae (e.g., Chlamydomonas)": 1.0,
                "Foraminifera": 1.0,
            },
            "Multi-celled organisms": {
                "Sponges (Porifera)": 1.0,
                "Coenocytic Organisms": 1.0,
                "Cnidarians": 1.0,
                "Flatworms": 1.0,
                "Roundworms": 1.0,
                "Mollusks": 1.0,
                "Annelids": 1.0,
                "Arthropods": 1.0,
                "Echinoderms": 1.0,
                "Chordates": 1.0,
            },
            "Complex lifeforms": {
                "Corals": 1.0,
                "Sponges": 1.0,
                "Algae": 1.0,
                "Anemones": 1.0,
                "Polychaetes": 1.0,
                "Parrotfish": 1.0,
                "Butterflyfish": 1.0,
                "Octopuses": 1.0,
                "Urchins": 1.0,
                "Turtles": 1.0,
                "Sharks": 1.0,
                "Groupers": 1.0,
                "Eels": 1.0,
                "Barracudas": 1.0,
                "Lionfish": 1.0,
            }
        },
        "Flora": flora_genus,
        "Cold-Tolerant Flora": flora_genus,
    }

