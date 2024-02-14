class ValueFramework:
    def __init__(self, genetics):
      self.values = self.get_values(genetics)

    def has(self, value):
        return value in self.values

    def get_values(self, genetics):
        # Compile the list of sociological norms associated with the expressed genetic features
        sociological_values = []
        for feature in genetics:
            if feature in self.values_based_on_genetics:
                sociological_values.extend(self.values_based_on_genetics[feature])
                
        # Remove duplicates from the sociological values list
        return list(set(sociological_values))

    values_based_on_genetics = {
        'Height': ['Stature Valorization', 'Tall Architectural Adaptation'],
        'Mass': ['Physical Presence', 'Huge Structural Design'],
        'Intelligence': ['Intellect Valorization', 'Educational Priority', 'Innovation Emphasis'],
        'Strength': ['Physical Valor', 'Warrior Culture'],
        'Dexterity': ['Skillfulness', 'Ranged Combat'],
        'Constitution': ['Resilience'],
        'Endurance': ['Perseverance', 'Endurance Cultivation'],
        'Charisma': ['Hierarchical Leadership', 'Charismatic Dominance'],
        'Wisdom': ['Cunning', 'Strategic Councils'],
        'Perception': ['Insight Cultivation', 'Sensory Acuity'],
        'Speed': ['High-Frequency Language', 'Rapid Response'],
        'Adaptability': ['Flexibility', 'Evolutionary Dynamism'],
        'Camouflage': ['Embedded Architecture', 'Social Concealment'],
        'Stealth': ['Privacy Emphasis', 'Covert Operations'],
        'Aquatic Adaptation': ['Aquatic Lifestyle', 'Water Affinity'],
        'Pressure Resistance': ['Deep-Sea Adaptation', 'Pressure Tolerance'],
        'Thermal Resistance': ['Heat Adaptation', 'Cold Endurance'],
        'Radiation Resistance': ['Radiation Baths', 'Mutagenic Forms'],
        'Photosynthetic Ability': ['Autotrophic Lifestyle', 'Photosynthetic Architectural Integration'],
        'Regeneration': ['Regenerative Healing', 'Rapid Recovery'],
        'Longevity': ['Lifespan Extension', 'Aging Attitudes'],
        'Reproductive Rate': ['Fertility Norms', 'Birthrate Control'],
        'Sensory Range': ['Perceptual Roles', 'Sensory Enrichment'],
        'Ecosystem Impact': ['Industrial Might', 'Waste Managers'],
        'Eco-Sensitivity': ['Ecological Defenders', 'Eco-Integration'],
        'Resource Utilization': ['Resource Efficiency', 'Stoicism'],
        'Flight Capability': ['Aerial Mobility', 'Vertical Architecture'],
        'Immune System Strength': ['Disease Resistance', 'Pathogen Management'],
        'Nutritional Requirements': ['Dietary Diversity', 'Food Cultivation'],
        'Oxygen Utilization Efficiency': ['Breathing Adaptation', 'Oxygen Management'],
        'Vision Adaptation': ['Visual Culture', 'Colorful Culture'],
        'Predation Instincts': ['Predatory Valor', 'Combat Strategies'],
        'Toxin Resistance': ['Poison Immunity', 'Toxicology Knowledge'],
        'Toxin Production': ['Chemical Warfare', 'Toxin Utilization'],
        'Navigation Skills': ['Wayfinding Traditions', 'Migration', 'Exploration'],
        'Social Cooperation': ['Collectivism', 'Cooperative Frameworks']
    }

    sociopolitical_mods = {
        "Stature Valorization": [
            ["Social Mobility", -0.1],
            ["Militaristic", 0.1]
        ],
        "Tall Architectural Adaptation": [
            ["Environmental Sustainability", 0.1],
            ["Technological Integration", 0.1]
        ],
        "Physical Presence": [
            ["Militaristic", 0.2],
            ["Nationalism", 0.1]
        ],
        "Huge Structural Design": [
            ["Environmental Sustainability", 0.1],
            ["Technological Integration", 0.2]
        ],
        "Intellect Valorization": [
            ["Innovation and Research", 0.3],
            ["Social Mobility", 0.2]
        ],
        "Educational Priority": [
            ["Social Welfare", 0.2],
            ["Information Freedom", 0.2]
        ],
        "Innovation Emphasis": [
            ["Innovation and Research", 0.3]
        ],
        "Physical Valor": [
            ["Militaristic", 0.2],
            ["Egalitarianism", -0.3]
        ],
        "Warrior Culture": [
            ["Militaristic", 0.3],
            ["Nationalism", 0.2],
        ],
        "Skillfulness": [
            ["Worker Self-Management", 0.1],
            ["Merit-based Advancement", 0.2]
        ],
        "Ranged Combat": [
            ["Militaristic", 0.2]
        ],
        "Resilience": [
            ["Social Welfare", 0.1],
            ["Environmental Sustainability", 0.1]
        ],
        "Perseverance": [
            ["Social Welfare", 0.1]
        ],
        "Endurance Cultivation": [
            ["Health", 0.2],
            ["Environmental Sustainability", 0.1]
        ],
        "Hierarchical Leadership": [
            ["Centralization", 0.4],
            ["Class Stratification", 0.3]
        ],
        "Charismatic Dominance": [
            ["Centralization", 0.1],
            ["Class Stratification", 0.1]
        ],
        "Cunning": [
            ["Diplomatic", 0.1],
            ["Covert Operations", 0.2]
        ],
        "Strategic Councils": [
            ["Diplomatic", 0.2],
            ["Centralization", -0.4]
        ],
        "Insight Cultivation": [
            ["Innovation and Research", 0.2],
            ["Educational Priority", 0.1]
        ],
        "Sensory Acuity": [
            ["Environmental Sustainability", 0.1]
        ],
        "High-Frequency Language": [
            ["Information Freedom", 0.1]
        ],
        "Rapid Response": [
            ["Security", 0.2],
            ["Civic Participation", 0.4]
        ],
        "Flexibility": [
            ["Social Mobility", 0.1],
            ["Open Borders", 0.4]
        ],
        "Evolutionary Dynamism": [
            ["Environmental Sustainability", 0.2],
            ["Technological Integration", 0.1]
        ],
        "Embedded Architecture": [
            ["Environmental Sustainability", 0.2]
        ],
        "Social Concealment": [
            ["Privacy", 0.2],
            ["Covert Operations", 0.1]
        ],
        "Privacy Emphasis": [
            ["Privacy", 0.3]
        ],
        "Covert Operations": [
            ["Security", 0.2],
            ["Diplomatic", -0.1]
        ],
        "Aquatic Lifestyle": [
            ["Environmental Sustainability", 0.2]
        ],
        "Water Affinity": [
            ["Environmental Sustainability", 0.2]
        ],
        "Deep-Sea Adaptation": [
            ["Environmental Sustainability", 0.2]
        ],
        "Pressure Tolerance": [
            ["Technological Integration", 0.1]
        ],
        "Heat Adaptation": [
            ["Environmental Sustainability", 0.1]
        ],
        "Cold Endurance": [
            ["Environmental Sustainability", 0.1]
        ],
        "Radiation Baths": [
            ["Technological Integration", 0.2]
        ],
        "Mutagenic Forms": [
            ["Ideological Enforcement", -0.4],
        ],
        "Autotrophic Lifestyle": [
            ["Ideological Enforcement", 0.3]
        ],
        "Photosynthetic Architectural Integration": [
            ["Public Commons", 0.3]
        ],
        "Regenerative Healing": [
            ["Social Welfare", 0.3]
        ],
        "Rapid Recovery": [
            ["Security", 0.2]
        ],
        "Lifespan Extension": [
            ["Class Stratification", 0.3]
        ],
        "Aging Attitudes": [],
        "Fertility Norms": [],
        "Birthrate Control": [],
        "Perceptual Roles": [],
        "Sensory Enrichment": [],
        "Industrial Might": [("Environmental Sustainability", -0.2), ("Innovation and Research", 0.2)],
        "Waste Managers": [("Environmental Sustainability", 0.2)],
        "Ecological Defenders": [("Environmental Sustainability", 0.3)],
        "Eco-Integration": [("Environmental Sustainability", 0.4)],
        "Resource Efficiency": [("Environmental Sustainability", 0.2)],
        "Stoicism": [],
        "Aerial Mobility": [("Technological Integration", 0.1)],
        "Vertical Architecture": [("Environmental Sustainability", 0.1)],
        "Disease Resistance": [("Social Welfare", 0.1)],
        "Pathogen Management": [("Social Welfare", 0.1)],
        "Dietary Diversity": [],
        "Food Cultivation": [("Environmental Sustainability", 0.2)],
        "Breathing Adaptation": [],
        "Oxygen Management": [],
        "Visual Culture": [],
        "Colorful Culture": [],
        "Predatory Valor": [("Militaristic", 0.2)],
        "Combat Strategies": [("Militaristic", 0.3)],
        "Poison Immunity": [("Social Welfare", 0.1)],
        "Toxicology Knowledge": [("Innovation and Research", 0.1)],
        "Chemical Warfare": [("Militaristic", 0.2)],
        "Toxin Utilization": [("Innovation and Research", 0.1)],
        "Wayfinding Traditions": [],
        "Migration": [],
        "Exploration": [("Innovation and Research", 0.2)],
        "Collectivism": [("Social Welfare", 0.1), ("Egalitarianism", 0.2)],
        "Cooperative Frameworks": [("Social Welfare", 0.2), ("Participatory Governance", 0.2)]
    }
