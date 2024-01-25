# Simple Life Form Concepts are simplified
simple_life_form_categories = {
    "Single-celled organisms": {
        "Archaea": "Unicellular organisms, similar to bacteria but with distinct molecular characteristics.",
        "Bacteria": "Unicellular microorganisms with no nucleus.",
        "Protozoa": "Diverse group of unicellular eukaryotic organisms, often motile.",
        "Fungi": "Includes unicellular organisms like yeasts as well as simple multicellular forms like molds.",
        "Algae": "Photosynthetic organisms, can be unicellular or simple multicellular.",
    },
    'Multi-celled organisms': {
        "Sponges (Porifera)": "Simplest multicellular animals, lacking true tissues and organs.",
        "Coenocytic Organisms": "Multinucleate organisms with no cell walls, like slime molds.",
        "Cnidarians": "Simple organisms with stinging cells",
        "Flatworms": "Simple, flat organisms with no organs",
        "Roundworms": "Simple, cylindrical organisms with no organs",
        "Mollusks": "Simple organisms with soft bodies and shells",
        "Annelids": "Simple organisms with segmented bodies",
        "Arthropods": "Simple organisms with jointed legs and exoskeletons",
        "Echinoderms": "Simple organisms with spiny skin",
        "Chordates": "Simple organisms with spinal cords"
    }
}

# Complex Life Form Concepts each include a single LifeForm Concept
complex_life_form_categories = {
    'Complex lifeforms': { # categorized per planet/biome"
        "Flora": {

        },
        "Terrestrial": {
            "Forest": {
                "Early Arboreal Organisms": "Tree-dwelling, primitive organisms developing climbing and gliding adaptations.",
                "Mid-Cycle Forest Dwellers": "Diverse herbivores and carnivores with adaptations for dense forest environments.",
                "Advanced Canopy Species": "Highly specialized arboreal species with complex social structures and behaviors."
            },
            "Desert": {
                "Early Desert Adapters": "Organisms with basic water retention and heat avoidance capabilities.",
                "Desert Specialists": "Species with advanced water conservation, navigation, and temperature regulation.",
                "Desert Apex Predators": "Highly efficient predators adapted for extreme aridity and temperature fluctuations."
            },
            "Tundra": {
                "Initial Tundra Colonizers": "Hardy species with adaptations for cold temperatures and low vegetation.",
                "Tundra Herbivores and Predators": "Species with insulating adaptations and migration/in-hibernation strategies.",
                "Advanced Tundra Specialists": "Highly adapted species for extreme cold and seasonal changes."
            },
            "Grassland": {
                "Early Grazers": "Species adapted to wide, open environments with basic herding or solitary behaviors.",
                "Grassland Predators": "Fast and agile species adapted for hunting in open terrains.",
                "Advanced Grassland Mammals": "Species with complex social structures and varied diets."
            },
            "Wetlands": {
                "Early Amphibious Life": "Organisms with dual aquatic and terrestrial adaptations.",
                "Wetland Avians": "Bird-like species adapted for wading and specialized feeding.",
                "Apex Wetland Predators": "Top predators with amphibious capabilities and diverse diets."
            },
            "Savanna": {
                "Early Savanna Fauna": "Organisms adapted to seasonal water availability and open landscapes.",
                "Savanna Herd Species": "Large herbivores with migration behaviors and social structures.",
                "Savanna Predators": "Stealthy and fast predators adapted for hunting large herbivores."
            },
            "Taiga": {
                "Initial Taiga Adaptations": "Species with insulating features and foraging behaviors for long winters.",
                "Mid-Tier Taiga Fauna": "Predators and herbivores with specialized winter survival strategies.",
                "Apex Taiga Predators": "Top predators with adaptations for hunting in dense, snowy forests."
            },
            "Chaparral": {
                "Early Chaparral Dwellers": "Species adapted to dry summers and wet winters, with fire-resistant traits.",
                "Mid-Cycle Chaparral Fauna": "Herbivores and omnivores with varied diets and drought survival strategies.",
                "Chaparral Predators": "Adaptable predators proficient in camouflage and ambush tactics."
            },
            "Temperate Deciduous Forest": {
                "Early Deciduous Forest Species": "Species adapted to seasonal changes with varied feeding and hibernation strategies.",
                "Mid-Level Forest Dwellers": "Diverse herbivores and carnivores with adaptations for vertical forest layers.",
                "Advanced Deciduous Predators": "Top predators with adaptations for seasonal hunting and territory control."
            },
            "Temperate Rainforest": {
                "Early Rainforest Settlers": "Species with adaptations for high rainfall and dense undergrowth.",
                "Mid-Level Canopy Dwellers": "Arboreal species with climbing and gliding abilities.",
                "Advanced Rainforest Predators": "Stealthy predators adapted for a three-dimensional forest environment."
            },
            "Mediterranean": {
                "Early Mediterranean Adapters": "Species adapted to hot, dry summers and mild, wet winters.",
                "Mediterranean Flora and Fauna": "Diverse plant and animal life adapted to limited water resources.",
                "Mediterranean Predators": "Predators adapted for hunting in open and mixed terrains."
            },
            "Montane (Alpine)": {
                "Initial Alpine Species": "Organisms adapted to high altitude, thin air, and cold temperatures.",
                "Mid-Altitude Dwellers": "Species with enhanced respiratory systems and temperature regulation.",
                "Alpine Apex Predators": "Top predators adapted for hunting in rugged, mountainous terrains."
            },
            "Coral Reefs": {
                "Early Reef Builders": "Simple organisms contributing to reef structures, like corals and sponges.",
                "Reef Community Members": "Diverse fish, mollusks, and crustaceans with symbiotic and predatory relationships.",
                "Advanced Reef Predators": "Top predators in the reef ecosystem with specialized hunting strategies."
            },
            "Mangroves": {
                "Mangrove Foundation Species": "Early colonizers that stabilize and enrich the mangrove ecosystem.",
                "Mangrove Community Dwellers": "Species adapted to brackish water and tidal changes.",
                "Mangrove Apex Predators": "Top predators adapted for an amphibious life in tangled root systems."
            }
        },
        "Aquatic": {
            "Ocean": {
                "Jellyfish": "Simple filter-feeding jellyfish",
                "Plankton": "Planktonic algae",
                "Fish": "Basic fish species with primitive swimming capabilities",
                "Cephalopod": "Primitive cephalopods",
                "Trilobite": "Early crustaceans resembling trilobites",
                "SchoolingFish": "Schooling fish with advanced navigation",
                "Manta": "Graceful manta rays",
                "Shark": "Agile predatory sharks",
                "Giant Tube Worm": "Giant tube worms near hydrothermal vents",
                "Anglerfish": "Deep-sea anglerfish with lure-like appendages",
                "Pressure-Adapted Isopods": "Pressure-adapted isopods",
                "Viperfish": "Viperfish with sharp fangs"
            },
            "Coral Reefs": {
                  "Corals": "Stony corals with symbiotic algae",
                "Sponges": "Reef-building sponges",
                "Algae": "Calcium-depositing algae",
                "Anemones": "Colonial anemones",
                "Polychaetes": "Tube-building polychaetes",
                "Parrotfish": "Parrotfish with coral-grazing habits",
                "Butterflyfish": "Colorful butterflyfish",
                "Octopuses": "Reef octopuses",
                "Urchins": "Long-spined sea urchins",
                "Turtles": "Grazing sea turtles",
                "Sharks": "Reef sharks like the blacktip reef shark",
                "Groupers": "Large groupers",
                "Eels": "Moray eels in reef crevices",
                "Barracudas": "Barracudas with swift attacks",
                "Lionfish": "Predatory lionfish with venomous spines"
            },
            "Mangroves": {
                "Root-Dwelling Early Life": "Mudskippers, juvenile fishes, and root-feeding crustaceans.",
                "Mangrove Community Organisms": "Birds, crabs, shellfish, and young predatory fish.",
                "Mangrove Apex Predators": "Crocodilians, large fish, and predatory birds."
            },
            "Super-Earth Oceanic": {
                "Giant Marine Plankton": "Colossal planktonic organisms and giant floating algae.",
                "Mid-Level Navigators": "Super-sized cephalopods, armored fishes, and swift-moving marine mammals.",
                "Leviathan Predators": "Gigantic predatory creatures, some resembling prehistoric marine reptiles."
            },
            "Subsurface Ocean": {
                "Chemotrophic Base Life": "Diverse chemosynthetic bacteria and tube worms near hydrothermal vents.",
                "Thermal Vent Communities": "Heat-tolerant crustaceans, blind fish, and unique mollusks.",
                "Subsurface Apex Predators": "Sonic-hunting creatures and large, tentacled hunters of the deep."
            },
        }
    }
}
# Life Form CAPSTONE CONCEPTS -- TODO: We need to add more concepts and align this 
life_form_metadata = {
    "Amorphous": {
        "Morphology": "Capable of changing shape in response to environmental stimuli",
        "Sensory Perception": "Likely rudimentary, based on direct environmental interaction",
        "Reproduction": "Could involve splitting or amalgamating with similar life forms",
        "Evolution": "Adaptation through mutation or environmental assimilation",
        "Movement": "Locomotion through flowing, oozing, or other non-standard methods"
    },
    "Aquatic": {
        "Physiological Adaptations": "Gills for underwater breathing, streamlined bodies for efficient swimming",
        "Sensory Perception": "Adapted for underwater environments, like enhanced vision or echolocation",
        "Reproduction": "Variety of reproductive strategies, from spawning to live birth",
        "Social Structure": "Ranges from solitary to complex social groups",
        "Diet": "Diverse, from planktonic organisms to larger marine animals"
    },
    "Cold-Tolerant Fauna": {
        "Physiological Adaptations": "Antifreeze proteins, insulating layers, reduced metabolic rates",
        "Growth Patterns": "Slow growth rates, possibly with dormancy periods",
        "Reproduction": "Adapted to short growing seasons, with rapid lifecycle stages",
        "Survival Strategy": "Adaptations to conserve energy and resources",
        "Ecological Interactions": "Specialized roles in cold ecosystems"
    },
    "Cold-Tolerant Flora": {
        "Physiological Adaptations": "Antifreeze properties, slow metabolic processes",
        "Growth Patterns": "Adapted to harsh, cold conditions with limited growing periods",
        "Reproduction": "Efficient seed dispersal mechanisms for short growing seasons",
        "Survival Strategy": "Energy conservation and resilience in extreme cold",
        "Ecological Role": "Supporting cold ecosystems, often forming the basis of the food web"
    },
    "Crystalline": {
        "Structural Formation": "Growth through mineral deposition, possibly geometric structures",
        "Energy Utilization": "Likely photosynthetic or chemosynthetic",
        "Interaction with Environment": "Absorption and reflection of light, possible piezoelectric properties",
        "Growth": "Could be slow and dependent on environmental mineral availability",
        "Resilience": "High structural strength but potentially brittle"
    },
    "Electromagnetic": {
        "Existence": "Manifestation in electromagnetic fields, possibly invisible to the naked eye",
        "Interaction": "Influence over electronic devices, communication via electromagnetic waves",
        "Energy Utilization": "Absorbing and manipulating ambient electromagnetic energy",
        "Movement": "Unbound by physical barriers, potentially high-speed travel along electromagnetic lines",
        "Perception": "Sensing the world in terms of electromagnetic fields and currents"
    },
    "Flora": {
        "Photosynthesis": "Conversion of sunlight into energy, with oxygen as a byproduct",
        "Growth": "Adapted to specific ecological niches, from deep shade to full sunlight",
        "Reproduction": "From seeds to spores, with various dispersal mechanisms",
        "Interaction with Fauna": "Ranging from mutualistic relationships to defensive strategies against herbivores",
        "Adaptability": "Specialization to local environments, from deserts to rainforests"
    },
    "Gaseous": {
        "Form": "Existing as a cloud or nebulous entity, diffuse and expansive",
        "Sensory Mechanism": "Possibly sensing changes in pressure, temperature, and chemical composition",
        "Interaction": "Difficult to interact with physical objects but may influence gas and airflow dynamics",
        "Movement": "Capable of drifting or flowing with air currents, possibly controlling its own density and distribution",
        "Survival Mechanism": "May rely on atmospheric gases for sustenance, possibly through a form of gas absorption"
    },
    "Plasma": {
        "State of Matter": "Existing in a high-energy state beyond gas, composed of ionized particles",
        "Energy Interaction": "Interaction with magnetic and electric fields, possibly emitting light",
        "Form Stability": "Maintaining coherence in environments with sufficient energy",
        "Energy Requirement": "High energy needed to sustain the plasma state",
        "Environmental Impact": "Potential to influence or be influenced by high-energy phenomena"
        },
    "Pressure-Resistant": {
        "Structural Adaptations": "Robust physical structures to withstand high-pressure environments",
        "Sensory Adaptations": "Sensory organs adapted to function under extreme pressure",
        "Movement": "Mechanisms to navigate effectively in high-pressure conditions",
        "Habitat": "Likely found in deep-sea environments or other high-pressure ecological niches",
        "Interaction with Other Life": "Adapted to interact with similarly pressure-adapted organisms"
        },
    "Quantum": {
        "Existence": "Operating on quantum principles, possibly exhibiting phenomena like superposition or entanglement",
        "Perception": "Potentially perceiving and interacting with the environment at a quantum level",
        "Energy Utilization": "Utilizing quantum states or fluctuations for energy",
        "Communication": "Possibly capable of non-local communication through quantum entanglement",
        "Adaptation": "Thriving in environments where quantum effects are pronounced"
        },
    "Radiation-Resistant": {
        "Cellular Adaptations": "Robust DNA repair mechanisms and radiation shielding",
        "Habitat": "Thriving in radiation-rich environments, such as near radioactive materials or in space",
        "Reproduction": "Mechanisms to protect genetic material from radiation damage",
        "Ecological Role": "Potentially playing a key role in ecosystems with high radiation levels",
        "Survival Strategy": "Utilizing radiation as an energy source or for mutation and adaptation"
    },
    "Temperature-Resistant": {
        "Structural Adaptations": "Robust physical structures to withstand high-pressure environments",
        "Sensory Adaptations": "Sensory organs adapted to function under extreme pressure",
        "Movement": "Mechanisms to navigate effectively in high-pressure conditions",
        "Habitat": "Likely found in deep-sea environments or other high-pressure ecological niches",
        "Interaction with Other Life": "Adapted to interact with similarly pressure-adapted organisms"
    },
    "Terrestrial": {
        "Structural Adaptations": "Limbs for movement on land, organs adapted for air breathing",
        "Sensory Adaptations": "Senses tuned for detecting stimuli in a terrestrial environment",
        "Reproduction": "Diverse methods, from egg-laying to live birth",
        "Social Interaction": "Varied, from solitary to complex social structures",
        "Dietary Needs": "Adapted to consume land-based food sources"
    }
}
