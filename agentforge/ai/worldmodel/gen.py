import numpy as np

def create_star_tensor(star_probabilities):
    """Create and return a tensor representing star probabilities for the Milky Way galaxy."""
    star_tensor = np.array(list(star_probabilities.values()))
    return star_tensor / np.sum(star_tensor) if np.sum(star_tensor) != 1 else star_tensor

def create_planet_probability_matrix(planet_types, star_planet_categories):
    """Create and return a probability matrix for planets based on star type and planet position."""
    # Initialize the probability matrix with zeros
    planet_probabilities = np.zeros((4, 3, len(planet_types)))

    for star_category_index, (star_category, possible_planets) in enumerate(star_planet_categories.items()):
        # Assign probabilities for each planet type in a given category
        for position_index, position in enumerate(['inner', 'mid-range', 'outer']):
            position_planet_types = {
                'inner': ['terrestrial', 'superEarth', 'venusLike', 'oceanPlanet'],
                'mid-range': ['gasGiant', 'hotJupiter', 'neptunian', 'miniNeptune', 'ringedPlanet'],
                'outer': ['plutoLike', 'ceresLike', 'icy']
            }
            relevant_planet_types = [pt for pt in possible_planets if pt in position_planet_types[position]]
            for planet_type in relevant_planet_types:
                planet_probabilities[star_category_index, position_index, planet_types.index(planet_type)] = 1 / len(relevant_planet_types)

    return planet_probabilities

def create_refined_biomes_probability_matrix(planet_types, biomes):
    """Create and return a refined probability matrix for biomes based on planet type."""
    # Initialize the probability matrix with zeros
    biomes_probabilities = np.zeros((len(planet_types), len(biomes)))

    # Refined assignment of probabilities based on planet type
    for planet_index, planet_type in enumerate(planet_types):
        if planet_type in ['terrestrial', 'superEarth']:
            biomes_probabilities[planet_index, :] = [0.2, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0, 0.1]
        elif planet_type in ['gasGiant', 'neptunian']:
            biomes_probabilities[planet_index, :] = [0, 0, 0, 0, 0, 0.3, 0.3, 0, 0.4]
        elif planet_type == 'hotJupiter':
            biomes_probabilities[planet_index, :] = [0, 0, 0, 0, 0, 0.1, 0.1, 0.8, 0]
        elif planet_type in ['icy', 'plutoLike']:
            # Higher probability for ice biomes
            biomes_probabilities[planet_index, :] = [0, 0, 0, 0.1, 0, 0, 0, 0, 0.9]
        else:
            # Other planet types - assign a more diverse speculative distribution
            biomes_probabilities[planet_index, :] = [0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11]

    return biomes_probabilities

def create_lifeform_probability_matrix(biomes, life_forms):
    """Create and return a probability matrix for life forms based on biomes."""

    # Initialize the probability matrix with zeros
    num_biomes = len(biomes)
    num_life_form_categories = len(life_forms)
    max_subcategories = max(len(subcats) for subcats in life_forms.values())
    lifeform_probabilities = np.zeros((num_biomes, num_life_form_categories, max_subcategories))

    # Assigning equal probabilities within each life form category for simplicity
    for biome_index, biome in enumerate(biomes):
        for life_form_index, (life_form, subcategories) in enumerate(life_forms.items()):
            num_subcategories = len(subcategories)
            for subcategory_index in range(num_subcategories):
                # Simple equal distribution for this speculative model
                lifeform_probabilities[biome_index, life_form_index, subcategory_index] = 1 / num_subcategories

    return lifeform_probabilities


def create_detailed_characteristics_matrix():
    """Create and return a detailed matrix for individual characteristics of sapient beings."""
    # Define subcategories for each main category
    categories = {
        'Personal Attributes': ['Human', 'Alien', 'Hybrid', 'Other'],
        'Physical Characteristics': ['Small', 'Medium', 'Large', 'Strong', 'Agile', 'Other'],
        'Age and Life Stage': ['Youth', 'Adult', 'Elder'],
        'Health and Physical Abilities': ['Healthy', 'Impaired', 'Enhanced'],
        'Mental Capabilities': ['Intelligent', 'Emotionally Intelligent', 'Creative', 'Other'],
        'Psychological Traits': ['Introvert', 'Extrovert', 'Analytical', 'Other'],
        'Mental Health': ['Stable', 'Stressed', 'Disordered'],
        'Ambitions and Goals': ['Personal', 'Professional', 'Altruistic'],
        'Risk Tolerance': ['Risk-Averse', 'Risk-Neutral', 'Risk-Seeking'],
        'Adaptability': ['Rigid', 'Flexible', 'Highly Adaptive'],
        # ... (Continue with other categories)
    }

    # Initialize the matrix with zeros
    max_subcategories = max(len(subcats) for subcats in categories.values())
    characteristics_matrix = np.zeros((len(categories), max_subcategories))

    # Assigning probabilities to each subcategory
    # Note: These probabilities are speculative and for illustration purposes
    probabilities = {
        'Personal Attributes': [0.7, 0.2, 0.1, 0.05],
        'Physical Characteristics': [0.2, 0.4, 0.2, 0.1, 0.1, 0.05],
        'Age and Life Stage': [0.3, 0.5, 0.2],
        'Health and Physical Abilities': [0.6, 0.2, 0.2],
        'Mental Capabilities': [0.3, 0.3, 0.3, 0.1],
        'Psychological Traits': [0.25, 0.25, 0.25, 0.25],
        'Mental Health': [0.6, 0.3, 0.1],
        'Ambitions and Goals': [0.3, 0.3, 0.4],
        'Risk Tolerance': [0.3, 0.4, 0.3],
        'Adaptability': [0.2, 0.4, 0.4],
        # ... (Assign probabilities for other categories)
    }

    # Populate the matrix
    for category_index, (category, subcategories) in enumerate(categories.items()):
        for subcategory_index, subcategory in enumerate(subcategories):
            characteristics_matrix[category_index, subcategory_index] = probabilities[category][subcategory_index]

    return characteristics_matrix

def create_skills_probability_matrix():
    """Create and return a realistic probability matrix for future skills of sapient beings."""

    # Initialize the matrix with zeros
    max_subcategories = max(len(subcats) for subcats in skills.values())
    skills_matrix = np.zeros((len(skills), max_subcategories))

    # Assigning probabilities to each skill
    # Note: These probabilities are speculative and illustrative
    for category_index, (category, subcategories) in enumerate(skills.items()):
        for subcategory_index, subcategory in enumerate(subcategories):
            # Example probabilities (these can be adjusted based on specific assumptions)
            if category in ['Basic Survival Skills', 'Social and Community Skills']:
                probability = 0.25  # More common skills
            elif category in ['Mystical and Exotic Skills']:
                probability = 0.05  # Rare skills
            else:
                probability = 0.1  # Average prevalence
            skills_matrix[category_index, subcategory_index] = probability

    return skills_matrix

def create_realistic_skills_matrix(life_forms, skills):
    """Create and return a more realistic skills matrix based on life form categories."""
    # Flatten the list of skills into individual skill items
    all_skills = [skill for category in skills.values() for skill in category]

    # Flatten the life form subcategories
    all_life_forms = [subcategory for category in life_forms.values() for subcategory in category]

    # Initialize the matrix with zeros
    num_life_form_subcategories = len(all_life_forms)
    num_skills = len(all_skills)
    realistic_skills_matrix = np.zeros((num_life_form_subcategories, num_skills))

    # Assigning more realistic probabilities
    for life_form_index, life_form in enumerate(all_life_forms):
        for skill_index, skill in enumerate(all_skills):
            # Assign probabilities based on life form traits and skill requirements
            if 'Intelligent' in life_form or 'Artificial' in life_form:
                # Higher probability for technical, scientific, and medical skills
                if skill in ['Engineering', 'Computer Science', 'AI Development', 'Research Scientist']:
                    probability = 0.6
                else:
                    probability = 0.2
            elif 'Physical' in life_form:
                # Higher probability for physical skills
                if skill in ['Soldier', 'Martial Arts', 'Athleticism']:
                    probability = 0.5
                else:
                    probability = 0.1
            elif 'Social' in life_form:
                # Higher probability for social and leadership skills
                if skill in ['Teaching', 'Social Work', 'Community Organizing', 'Command']:
                    probability = 0.4
                else:
                    probability = 0.1
            else:
                # Default moderate probability for other combinations
                probability = 0.3

            realistic_skills_matrix[life_form_index, skill_index] = probability

    return realistic_skills_matrix

star_probabilities = {
    'Class O': 0.03,  # Blue Giants
    'Class B': 0.06,  # Blue-White Stars
    'Class A': 0.10,  # White Stars
    'Class F': 0.10,  # Yellow-White Stars
    'Class G': 0.15,  # Yellow Stars (like our Sun)
    'Class K': 0.10,  # Orange Stars
    'Class M': 0.15,  # Red Dwarfs
    'Red Giant': 0.10,  # Red Giants
    'White Dwarf': 0.05,  # White Dwarfs
    'Neutron Star': 0.05,  # Neutron Stars
    'Wolf-Rayet Star': 0.04,  # Wolf-Rayet Stars
    'Class L': 0.04,  # Brown Dwarfs (Class L)
    'Class T': 0.01,  # Methane Dwarfs
    'Class Y': 0.01  # Cool Brown Dwarfs
}

# Define the planet types and star-planet categories
planet_types = ['terrestrial', 'superEarth', 'mercuryLike', 'marsLike', 'gasGiant', 'hotJupiter', 
                'neptunian', 'ringedPlanet', 'miniNeptune', 'plutoLike', 'ceresLike', 'oceanPlanet', 'venusLike', 'icy']

star_planet_categories = {
    'hot_massive_stars': ['gasGiant', 'hotJupiter', 'neptunian'],
    'sun_like_stars': ['terrestrial', 'superEarth', 'mercuryLike', 'marsLike', 'gasGiant', 'hotJupiter', 
                       'neptunian', 'ringedPlanet', 'miniNeptune'],
    'cool_small_stars': ['terrestrial', 'superEarth', 'mercuryLike', 'marsLike', 'plutoLike', 'ceresLike', 'oceanPlanet'],
    'evolved_compact_stars': ['gasGiant', 'neptunian', 'ringedPlanet', 'miniNeptune']
}

biomes = [  "Forest", 
    "Desert", 
    "Ocean", 
    "Tundra", 
    "Grassland", 
    "Wetlands", 
    "Savanna", 
    "Taiga", 
    "Chaparral", 
    "Temperate Deciduous Forest", 
    "Temperate Rainforest", 
    "Mediterranean", 
    "Montane (Alpine)", 
    "Coral Reefs", 
    "Mangroves",
    "Silicon-based", 
    "Ammonia-based", 
    "Lava", 
    "Ice", 
    "Super-Earth Oceanic", 
    "Carbon-rich", 
    "Iron-rich", 
    "Helium-rich", 
    "Sulfuric Acid Cloud", 
    "Chlorine-based Atmosphere", 
    "Hydrocarbon Lakes", 
    "Supercritical Fluid", 
    "Subsurface Ocean"
]

# Define life form categories and their subcategories
life_forms = {
    'Carbon-Based': ['Aquatic', 'Terrestrial', 'Flora'],
    'Silicon-Based': ['Crystalline', 'Amorphous'],
    'Ammonia-Based': ['Cold-Tolerant Fauna', 'Cold-Tolerant Flora'],
    'Non-Solvent-Based': ['Gaseous', 'Plasma'],
    'Energy Beings': ['Electromagnetic', 'Quantum'],
    'Extremophiles': ['Radiation-Resistant', 'Pressure-Resistant', 'Temperature-Resistant'],
}

skills = {
    'Basic Survival Skills': ['Agriculture', 'Hunting', 'Foraging'],
    'Technical Skills': ['Engineering', 'Computer Science', 'Robotics', 'AI Development'],
    'Medical Skills': ['Doctor', 'Nurse', 'Medical Research', 'Alternative Medicine'],
    'Scientific Skills': ['Research Scientist', 'Astrobiology', 'Astrophysics', 'Quantum Mechanics'],
    'Social and Community Skills': ['Child-Rearing', 'Teaching', 'Social Work', 'Community Organizing'],
    'Arts and Culture': ['Music', 'Visual Arts', 'Literature', 'Performing Arts'],
    'Leadership and Strategy': ['Command', 'Administration', 'Diplomacy', 'Strategic Planning'],
    'Physical and Combat Skills': ['Soldier', 'Security', 'Martial Arts', 'Athleticism'],
    'Exploration and Discovery': ['Space Exploration', 'Deep Sea Diving', 'Wilderness Survival'],
    'Trade and Craftsmanship': ['Construction', 'Manufacturing', 'Handicraft', 'Culinary Arts'],
    'Technology and Computing': ['Software Development', 'Cybersecurity', 'Data Analysis', 'Virtual Reality'],
    'Environmental Skills': ['Ecology', 'Conservation', 'Environmental Science', 'Terraforming'],
    'Mystical and Exotic Skills': ['Psionics', 'Energy Manipulation', 'Dimensional Navigation']
}


# Create the star tensor and planet probability matrix
star_tensor = create_star_tensor(star_probabilities)
planet_probabilities = create_planet_probability_matrix(planet_types, star_planet_categories)
biomes_probabilities = create_refined_biomes_probability_matrix(planet_types, biomes)
lifeform_probabilities = create_lifeform_probability_matrix(biomes, life_forms)\

# star_tensor, np.sum(star_tensor), planet_probabilities.shape, planet_probabilities
print(planet_probabilities)

