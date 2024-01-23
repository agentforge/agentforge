import time
import numpy as np
import pandas as pd
from agentforge.ai.worldmodel.star import Star
from agentforge.ai.worldmodel.planet import Planet
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.concept import Concept, normalize_rows, ensure_non_negative_and_normalize_row
from agentforge.ai.worldmodel.biome import Biome
from agentforge.ai.worldmodel.moon import Moon
from scipy.spatial import KDTree
from agentforge.ai.worldmodel.designation import CelestialNamingSystem
from uuid import uuid4
from agentforge.ai.worldmodel.simulation import StarSimulation

class Galaxy:
    def __init__(self, metadata=None):
        self.metadata = metadata if metadata is not None else {}
        self.star = Star()
        self.planet = Planet()
        self.lifeform = Lifeform()
        self.biome = Biome()
        self.moon = Moon()
        self.MIN_STAR_SPEED = 0.0005
        self.MAX_STAR_SPEED = 0.0015
        self.REPULSION_DISTANCE = 10
        self.NUM_SAMPLES = 100
        self.star_simulation = StarSimulation(self.REPULSION_DISTANCE)
        self.star_designations = [
            'Kepler', 'Hubble', 'Galileo', 'Hawking', 'Sagan', 'Curie',
            'Newton', 'Einstein', 'Copernicus', 'Herschel', 'Voyager', 'Cassini',
            'Webb', 'Chandra', 'Spitzer', 'Planck', 'Fermi', 'Swift', 'Rosetta', 'Juno',
            'Pioneer', 'Viking', 'Magellan', 'Tycho', 'Halley', 'Huygens', 'Ptolemy', 
            'Brahe', 'Hipparchus', 'Messier', 'Leavitt', 'Tombaugh', 'Lowell', 'Hoyle',
            'Shapley', 'Bell', 'Rubin', 'Mariner', 'Ulysses', 'Spirit', 'Opportunity',
            'Curiosity', 'Perseverance', 'Ingenuity', 'Apollo', 'Gemini', 'Mercury',
            'Soyuz', 'Vostok', 'New Horizons', 'Parker', 'Europa Clipper', 'Luna', 
            'Zond', 'Venera', 'Nikola Tesla', 'da Vinci',
            'Archimedes', 'Aristotle', 'Al-Biruni', 'Alhazen', 'Anaximander', 'Bacon',
            'Braun', 'Bruno', 'Carson', 'Dawkins', 'Descartes', 'Drake', 'Edison', 
            'Faraday', 'Feynman', 'Franklin', 'Galilei', 'Goodall', 'Heisenberg', 
            'Hippocrates', 'Hopper', 'Jung', 'Kaku', 'Lamarck', 'Lavoisier', 'Lovelace',
            'Mendel', 'Mendeleev', 'Michelson', 'Morley', 'Newton', 'Nightingale', 
            'Noether', 'Oppenheimer', 'Pascal', 'Pasteur', 'Pauling', 'Pavlov', 'Payne',
            'Penrose', 'Planck', 'Poincaré', 'Raman', 'Ramanujan', 'Rutherford', 
            'Salk', 'Schrödinger', 'Skłodowska', 'Sommerfeld', 'Thomson', 
            'Tyson', 'Venter', 'Watson', 'Watt', 'Wiener', 'Wolfram', 'Wright', 
            'Yalow', 'Yeager', 'Zwicky', 'Arecibo', 'FAST', 'Green Bank', 'Lovelock', 
            'SETI', 'TESS', 'VLA', 'VLBI', 'WISE', 'XMM-Newton', 'HD', 'PSR', 'WASP', 'KIC',
            'LHS', 'TOI', 'GJ', 'TRAPPIST', 'OGLE', 'K2'
        ]
        self.designation_counters = {key: np.random.randint(0, 999) for key in self.star_designations}

    async def generate_with_life(self, num_systems):
        systems_dict = self.generate(100000)
        num_dead_systems = num_systems - len(self.has_life)
        dead_systems = np.random.choice(self.systems, num_dead_systems, replace=False).tolist()
        systems_to_return = dead_systems + systems_dict["has_life"]
        print(len(systems_to_return))
        print(len(systems_dict["has_life"]))
        print(len(dead_systems))
        return {"systems": dead_systems + systems_dict["has_life"], "starfield_positions": systems_dict["starfield_positions"]}

    def generate(self, num_systems):
        system_names = self.get_system_name(num_systems)
        # From the macro to the micro, we build the world model
        self.systems = []
        self.has_life = []
        print("generating star positions...")
        
        star_positions, starfield_positions = self.generate_spiral_positions(num_systems, starfieldSystems=2200, core_systems_ratio=0.1, num_arms=6, checkDistance=True, r_spread=9500, core_radius=300, anim_steps=2500, noise_scale=100, tightness=3)
    
        kd_tree = KDTree(np.array(star_positions))  # Rebuild KDTree with new star positions

        # Ensure that nearest_neighbors is a 2D array with correct dimensions
        nearest_neighbors = [kd_tree.query(position, k=6)[1][1:] for position in star_positions]

        neighbors_positions = star_positions[np.array(nearest_neighbors)]

        # Reshape star_positions for broadcasting
        star_positions_reshaped = star_positions[:, np.newaxis, :]

        # Calculate distances
        distances_matrix = np.linalg.norm(neighbors_positions - star_positions_reshaped, axis=2)

        print("generating starfield positions...")
        self.galaxy_concepts = {"Milky Way": Concept("Milky Way", "Galaxy")}
        galaxy_names = list(self.galaxy_concepts.keys())
        star_names = list(self.star.star_concepts.keys())
        planet_names = list(self.planet.planet_concepts.keys())
        biome_names = list(set(b for biomes in self.planet.planet_biome_connections.values() for b in biomes))

        for star_type, probability in self.star.star_probabilities.items():
            self.galaxy_concepts["Milky Way"].add_connection(self.star.star_concepts[star_type], probability)

        self.star.create_connections_for_star(self.planet)

        # Initialize DataFrames with float dtype
        gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
        sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
        px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
        bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=self.lifeform.life_form_categories)

        # Step 1: Create GxS DataFrame
        gx_s_df = pd.DataFrame(0.0, index=galaxy_names, columns=star_names)
        for galaxy in galaxy_names:
            for connection in self.galaxy_concepts[galaxy].get_connections():
                gx_s_df.at[galaxy, connection['concept'].name] = connection['probability']

        # Step 2: Create SxP DataFrame
        sx_p_df = pd.DataFrame(0.0, index=star_names, columns=planet_names)
        for star in star_names:
            for connection in self.star.star_concepts[star].get_connections():
                sx_p_df.at[star, connection['concept'].name] = connection['probability']

        # Create the PxB DataFrame
        px_b_df = pd.DataFrame(0.0, index=planet_names, columns=biome_names)
        for planet in planet_names:
            for biome, probability in self.planet.planet_biome_connections.get(planet, {}).items():
                if biome in biome_names:
                    px_b_df.at[planet, biome] = probability

        # Initialize the Biome x Biology DataFrame
        bx_b_df = pd.DataFrame(0.0, index=biome_names, columns=self.lifeform.life_form_categories)

        # Populate the DataFrame with probabilities
        for biome in biome_names:
            for subcategory, probability in self.biome.biome_biology_probabilities.get(biome, {}).items():
                if subcategory in self.lifeform.life_form_categories:
                    bx_b_df.at[biome, subcategory] = probability

        # Create the biological matrix with row normalization
        biological_matrix_row_norm = self.lifeform.create_biological_matrix_row_normalization()

        # Initialize the Biology x Individual Characteristics DataFrame
        biology_x_individual_df = pd.DataFrame(0.0, index=biological_matrix_row_norm.index, columns=self.lifeform.life_form_characteristic_names)

        # Populate the DataFrame with normalized values
        for biology_type in biological_matrix_row_norm.index:
            for characteristic in self.lifeform.life_form_characteristic_names:
                biology_x_individual_df.at[biology_type, characteristic] = biological_matrix_row_norm.at[biology_type, characteristic]

        # Normalize rows of GxS, SxP, PxB, and BxBio DataFrames
        normalized_gx_s_df = normalize_rows(gx_s_df)
        normalized_sx_p_df = normalize_rows(sx_p_df)
        normalized_px_b_df = normalize_rows(px_b_df)
        normalized_bx_b_df = normalize_rows(bx_b_df)
        normalized_bx_lf_df = normalize_rows(biology_x_individual_df)

        # Multiply normalized GxS, SxP, PxB, and BxBio DataFrames to get GxBio DataFrame
        gx_p_df = normalized_gx_s_df.dot(normalized_sx_p_df)
        gx_b_df = gx_p_df.dot(normalized_px_b_df)
        gx_bb_df = gx_b_df.dot(normalized_bx_b_df)
        gx_bl_df = gx_bb_df.dot(normalized_bx_lf_df)

        # print(gx_bb_df)
        # print(gx_b_df)
        # print(gx_p_df)
        # print(gx_bl_df)
        start_time = time.time()
        print("generating systems...")
        star_probabilities = normalized_gx_s_df.iloc[0]
        for star_position in star_positions:

            star_type = np.random.choice(star_names, p=star_probabilities)

            # Find the index of the sampled star type
            star_index = star_names.index(star_type)

            # Create star specific information
            star_mass_range = self.star.star_concepts[star_type].metadata['mass_range_kg']
            star_mass_kg = np.random.uniform(star_mass_range[0], star_mass_range[1])

            star_age_range = self.star.star_concepts[star_type].metadata['age_range_Gyr']
            star_age_Gyr = np.random.uniform(star_age_range[0], star_age_range[1])

            disk_mass_range = self.star.star_concepts[star_type].metadata['disk_mass_percentage_of_solar_mass']
            disk_mass = np.random.uniform(disk_mass_range[0], disk_mass_range[1])

            # Estimate number of planets
            num_planets = self.planet.estimate_planet_count(star_mass_kg, disk_mass, star_age_Gyr, 1.0)
            name = system_names.pop()
            name_generator = CelestialNamingSystem(name)
            solar_system_info = {
                "Name": name,
                "Star": star_type,
                "Star Position": star_position.tolist(),
                "Star Information": self.star.star_concepts[star_type].metadata,
                "Star Mass (kg)": star_mass_kg,
                "Star Age (Gyr)": star_age_Gyr,
                "Number of Planets": num_planets,
                "Disk Mass": disk_mass,
                "Planets": [],
                "uuid": str(uuid4())
            }

            # Sample a planet type based on star type
            planet_probabilities = normalized_sx_p_df.iloc[star_index]
            for _ in range(num_planets):

                planet_type = np.random.choice(planet_names, p=planet_probabilities)
                planet_name = name_generator.get_next_name("planet")
                # Find the index of the sampled planet type
                planet_index = planet_names.index(planet_type)
                planet_info, estimated_biomes, life_presence = self.planet.generate(planet_type, star_mass_kg, star_type)

                # Create and set names for satellites
                planet_info["Name"] = planet_name
                for moon in planet_info["Moons"]:
                    moon_name = name_generator.get_next_name("moon")
                    moon["Name"] = moon_name

                for _ in range(estimated_biomes):
                    biome_type = np.random.choice(biome_names, p=normalized_px_b_df.iloc[planet_index])

                    biome_index = biome_names.index(biome_type)
                    
                    lifeforms = []
                    
                    if life_presence:
                        biological_probabilities = normalized_bx_b_df.iloc[biome_index]
                        biological_type = np.random.choice(self.lifeform.life_form_categories, p=biological_probabilities)

                        biological_index = self.lifeform.life_form_categories.index(biological_type)

                        life_form_characteristic_probabilities = normalized_bx_lf_df.iloc[biological_index]
                        adjusted_probabilities = ensure_non_negative_and_normalize_row(life_form_characteristic_probabilities)
                        life_form_characteristic_list = list(set(np.random.choice(self.lifeform.life_form_characteristic_names, p=adjusted_probabilities, size=5)))

                        bio_info = {
                            "Biological": biological_type,
                            "Biological Characteristics": self.lifeform.biologic_concepts[biological_type].metadata,
                            "Life Form Characteristics": life_form_characteristic_list
                        }

                        lifeforms.append(bio_info)

                    biome_info = {
                        "Biome Type": biome_type,
                        "Lifeforms": lifeforms,
                    }

                    if biome_type not in planet_info["Biomes"]:
                        planet_info["Biomes"][biome_type] = {}

                    planet_info["Biomes"][biome_type].update(biome_info)

                solar_system_info["Planets"].append(planet_info)

            self.systems.append(solar_system_info)

            if life_presence:
                self.has_life.append(solar_system_info)

        # Setup neighbors
        end_time = time.time()
        print(f"System Generation Time elapsed: {end_time - start_time}")

        for i, system in enumerate(self.systems):
            system['Neighbors'] = []
            dist_idx = 0
            for neighbor_index in nearest_neighbors[i]:
                neighbor = {
                    "uuid": self.systems[neighbor_index]['uuid'],
                    "Distance": str(distances_matrix[i, dist_idx]),
                    "Name": self.systems[neighbor_index]['Name'],
                }
                system['Neighbors'].append(neighbor)
                dist_idx += 1

        return {"systems": self.systems, "has_life": self.has_life, "starfield_positions": starfield_positions.tolist()}

    # Perlin noise implementation
    def perlin_noise(self, size, scale=100, seed=None):
        if seed:
            np.random.seed(seed)
        grid_x, grid_y = np.mgrid[0:scale:complex(0, size), 0:scale:complex(0, size)]
        gradients = np.random.rand(scale, scale, 2) * 2 - 1
        gradients /= np.linalg.norm(gradients, axis=2, keepdims=True)

        dot_product = lambda x, y, gx, gy: gx * x + gy * y
        dprod = np.vectorize(dot_product)

        def lerp(a, b, t):
            return a + t * (b - a)

        def fade(t):
            return 6 * t**5 - 15 * t**4 + 10 * t**3

        distances_x = grid_x - grid_x.astype(int)
        distances_y = grid_y - grid_y.astype(int)

        fade_x = fade(distances_x)
        fade_y = fade(distances_y)

        top_right = dprod(distances_x-1, distances_y-1, gradients[grid_x.astype(int)+1, grid_y.astype(int)+1, 0], gradients[grid_x.astype(int)+1, grid_y.astype(int)+1, 1])
        top_left = dprod(distances_x, distances_y-1, gradients[grid_x.astype(int), grid_y.astype(int)+1, 0], gradients[grid_x.astype(int), grid_y.astype(int)+1, 1])
        bottom_right = dprod(distances_x-1, distances_y, gradients[grid_x.astype(int)+1, grid_y.astype(int), 0], gradients[grid_x.astype(int)+1, grid_y.astype(int), 1])
        bottom_left = dprod(distances_x, distances_y, gradients[grid_x.astype(int), grid_y.astype(int), 0], gradients[grid_x.astype(int), grid_y.astype(int), 1])

        lerp_top = lerp(top_left, top_right, fade_x)
        lerp_bottom = lerp(bottom_left, bottom_right, fade_x)
        return lerp(lerp_bottom, lerp_top, fade_y)

    def update_positions_with_random_speeds_og(self, star_positions, star_speeds, time_step):
        kd_tree = KDTree(star_positions)
        new_positions = np.copy(star_positions)

        for i, (pos, speed) in enumerate(zip(star_positions, star_speeds)):
            # Repulsion force logic
            distance, index = kd_tree.query(pos, k=2) 
            if distance[1] < self.REPULSION_DISTANCE: 
                direction = pos - star_positions[index[1]]
                direction /= np.linalg.norm(direction)
                new_positions[i] += direction * speed * time_step

            # Adjust angular speed based on dark matter effect
            distance_from_center = np.sqrt(pos[0]**2 + pos[1]**2)
            dark_matter_factor = 1 + np.exp(-distance_from_center / 2000)
            angle = np.arctan2(pos[1], pos[0])
            angle += (speed * dark_matter_factor) * time_step / (distance_from_center + 0.1)
            new_x = distance_from_center * np.cos(angle)
            new_y = distance_from_center * np.sin(angle)
            new_positions[i][0] = new_x
            new_positions[i][1] = new_y

        return new_positions
    
    def monte_carlo_simulation(self, positions, speeds, time_step, anim_steps):
        num_stars = len(positions)
        final_positions = np.zeros_like(positions)

        for _ in range(self.NUM_SAMPLES):
            sample_positions = np.copy(positions)
            sample_speeds = np.copy(speeds) + np.random.randn(num_stars) * 0.1  # Randomize speeds

            for _ in range(anim_steps):
                # Randomize dark matter effect
                angles = np.arctan2(sample_positions[:, 1], sample_positions[:, 0])
                distances = np.sqrt(np.sum(sample_positions ** 2, axis=1))
                dark_matter_factor = 1 + np.exp(-distances / 2000) + np.random.randn(num_stars) * 0.1
                angle_change = (sample_speeds * dark_matter_factor) * time_step / (distances + 0.1)
                angles += angle_change
                sample_positions[:, 0] = distances * np.cos(angles)
                sample_positions[:, 1] = distances * np.sin(angles)

                # Randomize repulsion forces
                kd_tree = KDTree(sample_positions)
                for i, pos in enumerate(sample_positions):
                    distance, index = kd_tree.query(pos, k=2)
                    if distance[1] < self.REPULSION_DISTANCE:
                        direction = np.random.randn(2)  # Random direction
                        magnitude = np.random.rand() * 2  # Random magnitude
                        direction /= np.linalg.norm(direction)
                        sample_positions[i] += direction * magnitude * time_step

            final_positions += sample_positions

        # Average the results of all samples
        final_positions /= self.NUM_SAMPLES
        return final_positions

    
    def compute_dark_matter_effect(self, positions, speeds, time_step, anim_steps):
        # Initial angles and distances
        angles = np.arctan2(positions[:, 1], positions[:, 0])
        distances_from_center = np.sqrt(np.sum(positions ** 2, axis=1))
        dark_matter_factors = 1 + np.exp(-distances_from_center / 2000)

        # Approximating the total angle change over all steps
        total_angle_change = (speeds * dark_matter_factors) * time_step * anim_steps / (distances_from_center + 0.1)
        final_angles = angles + total_angle_change

        # Updating positions based on the final angles
        positions[:, 0] = distances_from_center * np.cos(final_angles)
        positions[:, 1] = distances_from_center * np.sin(final_angles)

        return positions

    def apply_repulsion_forces(self, positions, speeds, time_step):
        # Applying repulsion forces at the end
        kd_tree = KDTree(positions)
        for i, pos in enumerate(positions):
            distance, index = kd_tree.query(pos, k=2)
            if distance[1] < self.REPULSION_DISTANCE:
                direction = pos - positions[index[1]]
                norm = np.linalg.norm(direction)
                if norm != 0:
                    direction /= norm
                    positions[i] += direction * speeds[i] * time_step

        return positions

    def update_positions_with_random_speeds(self, star_positions, star_speeds, time_step, anim_steps):
        new_positions = np.copy(star_positions)
        new_positions = self.compute_dark_matter_effect(new_positions, star_speeds, time_step, anim_steps)
        new_positions = self.apply_repulsion_forces(new_positions, star_speeds, time_step)
        return new_positions

    def get_system_name(self, num_names=1):
        # Random choice array to determine naming method
        choice_array = np.random.choice(self.star_designations, num_names)

        names = []
        for random_name in choice_array:
            count = self.designation_counters[random_name]
            self.designation_counters[random_name] += 1
            name = f"{random_name}-{count + 1}"
            names.append(name)

        return names

    def generate_spiral_positions(self, num_systems, starfieldSystems=100, core_systems_ratio=0.2, min_distance=5, checkDistance=True, num_arms = 4, r_spread = 5000, anim_steps = 1500, tightness = 2, noise_scale = 60, core_radius = 300):
        num_systems += starfieldSystems
        # Determine the number of systems in the core and in the spiral arms
        num_core_systems = int(num_systems * core_systems_ratio)
        num_spiral_systems = num_systems - num_core_systems

        # Generate star positions
        np.random.seed(0)
        star_positions = []

        # Function to generate a single star position using perlin noise and trigonometry
        # to mimic a spiral arms pattern
        def generate_star_position(is_core=False):
            if is_core:
                angle = np.random.uniform(0, 2 * np.pi)
                radius = np.random.uniform(0, core_radius)
            else:
                arm_offset = 2 * np.pi * np.random.randint(num_arms) / num_arms
                angle = tightness * np.sqrt(len(star_positions) / num_spiral_systems) + arm_offset
                base_radius = (r_spread / num_arms) * np.sqrt(len(star_positions) / num_spiral_systems)
                noise = self.perlin_noise(1, scale=noise_scale)[0, 0]
                noisy_radius = base_radius * (1 + noise * 0.4)
                radius = noisy_radius
            
            scaleFactor = 5
            radius = radius * scaleFactor

            # Adding gravitational pull towards the center
            # gravity_factor = 1 - np.exp(-radius / 3000)  # Adjust the denominator for effect strength
            # radius *= (1 - gravity_factor)

            z = np.random.uniform(-50, 50) * np.sqrt(len(star_positions) / num_spiral_systems)
            
            return radius * np.cos(angle), radius * np.sin(angle), z

        # Initialize KDTree for efficient distance checking
        kd_tree = KDTree(np.zeros((0, 3)))

        # Generate positions for the spiral arms and the central cluster
        for _ in range(num_systems):
            num_attempts = 0
            is_core = len(star_positions) >= num_spiral_systems
            new_pos = generate_star_position(is_core)
            if checkDistance and not num_systems > starfieldSystems:
                while kd_tree.query([new_pos], k=1, distance_upper_bound=min_distance)[0][0] < min_distance and num_attempts < 100:
                    new_pos = generate_star_position(is_core)
            star_positions.append(new_pos)
            if checkDistance and not num_systems > starfieldSystems:
                kd_tree = KDTree(np.array(star_positions))  # Rebuild KDTree with new star position

        # Convert star_positions to a numpy array for easier handling
        star_positions = np.array(star_positions)

        # Initialize star speeds
        star_speeds = np.random.uniform(self.MIN_STAR_SPEED, self.MAX_STAR_SPEED, num_systems)
        print("evolving galaxy...")
        start_time = time.time()

        # MANY ATTEMPTS HERE TO OPTIMIZE THE SIMULATION, Matricies, probability distributions, etc.
        # star_positions = self.monte_carlo_simulation(star_positions, star_speeds, 0.1, anim_steps)
        # star_positions = self.update_positions_with_random_speeds(star_positions, star_speeds, 0.1, anim_steps)

        # Slow but accurate
        for i in range(anim_steps):
            if(i % 10 == 0):
                print(f"step {i} of {anim_steps}")
            star_positions = self.update_positions_with_random_speeds_og(star_positions, star_speeds, i)
        
        end_time = time.time()
        print(f"evolved galaxy in {end_time - start_time} seconds")

        # Scale galaxy up to 10000 light years
        star_positions = star_positions * 5.0
        starfield_indices = np.random.choice(len(star_positions), starfieldSystems, replace=False)
        starfields = star_positions[starfield_indices]

         # Create a mask to remove selected indices
        mask = np.ones(len(star_positions), dtype=bool)
        mask[starfield_indices] = False
        star_positions = star_positions[mask]

        return star_positions, starfields