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

    # TODO: Convert to new method of determining governance
    sociological_values_to_governance_adjustments = {
        'Stature Valorization': {
            'Feudal System': {'adjustment': 0.1, 'operator': '+'},
            'Tribalism': {'adjustment': 0.05, 'operator': '+'}
        },
        'Intellect Valorization': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.15, 'operator': '+'},
            'Democracy': {'adjustment': 0.05, 'operator': '+'}
        },
        'Physical Valor': {
            'Oligarchy': {'adjustment': 0.1, 'operator': '+'},
            'Dictatorship': {'adjustment': 0.1, 'operator': '+'},
            'Empire': {'adjustment': 0.05, 'operator': '+'}
        },
        'Evolutionary Dynamism': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'},
            'Federation': {'adjustment': 0.15, 'operator': '+'}
        },
        'Eco-Integration': {
            'Eco-Governance': {'adjustment': 0.3, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Resource Efficiency': {
            'Corporate State': {'adjustment': 0.2, 'operator': '+'},
            'Technocracy': {'adjustment': 0.15, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Tall Architectural Adaptation': {
            'Feudal System': {'adjustment': 0.05, 'operator': '+'},
            'Empire': {'adjustment': 0.05, 'operator': '+'}
        },
        'Physical Presence': {
            'Monarchy': {'adjustment': 0.1, 'operator': '+'},
            'Empire': {'adjustment': 0.05, 'operator': '+'}
        },
        'Huge Structural Design': {
            'Technocracy': {'adjustment': 0.1, 'operator': '+'},
            'Corporate State': {'adjustment': 0.05, 'operator': '+'}
        },
        'Educational Priority': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Innovation Emphasis': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Warrior Culture': {
            'Oligarchy': {'adjustment': 0.1, 'operator': '+'},
            'Dictatorship': {'adjustment': 0.1, 'operator': '+'}
        },
        'Skillfulness': {
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Ranged Combat': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Federation': {'adjustment': 0.05, 'operator': '+'}
        },
        'Resilience': {
            'Feudal System': {'adjustment': 0.1, 'operator': '+'},
            'Tribalism': {'adjustment': 0.1, 'operator': '+'}
        },
        'Perseverance': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Endurance Cultivation': {
            'Technocracy': {'adjustment': 0.1, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Hierarchical Leadership': {
            'Oligarchy': {'adjustment': 0.2, 'operator': '+'},
            'Monarchy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Charismatic Dominance': {
            'Dictatorship': {'adjustment': 0.2, 'operator': '+'},
            'Monarchy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Cunning': {
            'Theocracy': {'adjustment': 0.1, 'operator': '+'},
            'Corporate State': {'adjustment': 0.1, 'operator': '+'}
        },
        'Strategic Councils': {
            'Republic': {'adjustment': 0.2, 'operator': '+'},
            'Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Insight Cultivation': {
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'},
            'Technocracy': {'adjustment': 0.2, 'operator': '+'}
        },
        'Sensory Acuity': {
            'Technocracy': {'adjustment': 0.1, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'High-Frequency Language': {
            'Federation': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Rapid Response': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Flexibility': {
            'Egalitarian': {'adjustment': 0.2, 'operator': '+'},
            'Anarchy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Evolutionary Dynamism': {
            'Technocracy': {'adjustment': 0.15, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Embedded Architecture': {
            'Tribalism': {'adjustment': 0.1, 'operator': '+'},
            'Eco-Governance': {'adjustment': 0.1, 'operator': '+'}
        },
        'Social Concealment': {
            'Anarchy': {'adjustment': 0.1, 'operator': '+'},
            'Corporate State': {'adjustment': 0.05, 'operator': '+'}
        },
        'Privacy Emphasis': {
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Covert Operations': {
            'Corporate State': {'adjustment': 0.2, 'operator': '+'},
            'Dictatorship': {'adjustment': 0.15, 'operator': '+'}
        },
        'Aquatic Lifestyle': {
            'Tribalism': {'adjustment': 0.2, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'}
        },
        'Water Affinity': {
            'Eco-Governance': {'adjustment': 0.2, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'}
        },
        'Deep-Sea Adaptation': {
            'Tribalism': {'adjustment': 0.2, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'}
        },
        'Pressure Tolerance': {
            'Technocracy': {'adjustment': 0.15, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Heat Adaptation': {
            'Feudal System': {'adjustment': 0.1, 'operator': '+'},
            'Empire': {'adjustment': 0.05, 'operator': '+'}
        },
        'Cold Endurance': {
            'Feudal System': {'adjustment': 0.1, 'operator': '+'},
            'Empire': {'adjustment': 0.05, 'operator': '+'}
        },
        'Radiation Baths': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Mutagenic Forms': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Autotrophic Lifestyle': {
            'Eco-Governance': {'adjustment': 0.3, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'}
        },
        'Photosynthetic Architectural Integration': {
            'Eco-Governance': {'adjustment': 0.3, 'operator': '+'},
            'Technocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Regenerative Healing': {
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Rapid Recovery': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Fertility Norms': {
            'Tribalism': {'adjustment': 0.3, 'operator': '+'},
            'Feudal System': {'adjustment': 0.1, 'operator': '+'}
        },
        'Birthrate Control': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Perceptual Roles': {
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'},
            'Technocracy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Sensory Enrichment': {
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Industrial Might': {
            'Corporate State': {'adjustment': 0.2, 'operator': '+'},
            'Oligarchy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Waste Managers': {
            'Eco-Governance': {'adjustment': 0.2, 'operator': '+'},
            'Corporate State': {'adjustment': 0.1, 'operator': '+'}
        },
        'Ecological Defenders': {
            'Eco-Governance': {'adjustment': 0.3, 'operator': '+'},
            'Federation': {'adjustment': 0.15, 'operator': '+'}
        },
        'Stoicism': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Democracy': {'adjustment': 0.05, 'operator': '+'}
        },
        'Aerial Mobility': {
            'Federation': {'adjustment': 0.15, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Vertical Architecture': {
            'Corporate State': {'adjustment': 0.2, 'operator': '+'},
            'Technocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Disease Resistance': {
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'},
            'Technocracy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Pathogen Management': {
            'Technocracy': {'adjustment': 0.2, 'operator': '+'},
            'Republic': {'adjustment': 0.1, 'operator': '+'}
        },
        'Dietary Diversity': {
            'Eco-Governance': {'adjustment': 0.2, 'operator': '+'},
            'Federation': {'adjustment': 0.1, 'operator': '+'}
        },
        'Food Cultivation': {
            'Tribalism': {'adjustment': 0.2, 'operator': '+'},
            'Eco-Governance': {'adjustment': 0.15, 'operator': '+'}
        },
        'Breathing Adaptation': {
            'Technocracy': {'adjustment': 0.15, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Oxygen Management': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Visual Culture': {
            'Democracy': {'adjustment': 0.1, 'operator': '+'},
            'Republic': {'adjustment': 0.05, 'operator': '+'}
        },
        'Colorful Culture': {
            'Direct Democracy': {'adjustment': 0.1, 'operator': '+'},
            'Egalitarian': {'adjustment': 0.15, 'operator': '+'}
        },
        'Predatory Valor': {
            'Empire': {'adjustment': 0.2, 'operator': '+'},
            'Dictatorship': {'adjustment': 0.15, 'operator': '+'}
        },
        'Combat Strategies': {
            'Military Junta': {'adjustment': 0.2, 'operator': '+'},
            'Empire': {'adjustment': 0.1, 'operator': '+'}
        },
        'Poison Immunity': {
            'Technocracy': {'adjustment': 0.15, 'operator': '+'},
            'Meritocracy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Toxicology Knowledge': {
            'Republic': {'adjustment': 0.1, 'operator': '+'},
            'Technocracy': {'adjustment': 0.2, 'operator': '+'}
        },
        'Chemical Warfare': {
            'Dictatorship': {'adjustment': 0.2, 'operator': '+'},
            'Oligarchy': {'adjustment': 0.1, 'operator': '+'}
        },
        'Toxin Utilization': {
            'Corporate State': {'adjustment': 0.2, 'operator': '+'},
            'Technocracy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Wayfinding Traditions': {
            'Federation': {'adjustment': 0.15, 'operator': '+'},
            'Republic': {'adjustment': 0.1, 'operator': '+'}
        },
        'Migration': {
            'Tribalism': {'adjustment': 0.3, 'operator': '+'},
            'Anarchy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Exploration': {
            'Federation': {'adjustment': 0.2, 'operator': '+'},
            'Republic': {'adjustment': 0.1, 'operator': '+'}
        },
        'Collectivism': {
            'Egalitarian': {'adjustment': 0.2, 'operator': '+'},
            'Anarchy': {'adjustment': 0.15, 'operator': '+'}
        },
        'Cooperative Frameworks': {
            'Republic': {'adjustment': 0.2, 'operator': '+'},
            'Democracy': {'adjustment': 0.15, 'operator': '+'}
        }
    }