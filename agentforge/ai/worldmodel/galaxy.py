import time, math
import numpy as np
import pandas as pd
from agentforge.ai.worldmodel.star import Star
from agentforge.ai.worldmodel.planet import Planet
from agentforge.ai.worldmodel.lifeform import Lifeform
from agentforge.ai.worldmodel.concept import Concept
from agentforge.ai.worldmodel.biome import Biome
from agentforge.ai.worldmodel.moon import Moon
from scipy.spatial import KDTree
from agentforge.ai.worldmodel.designation import CelestialNamingSystem, star_designations
from tqdm import tqdm
from uuid import uuid4
from agentforge.ai.worldmodel.simulation import StarSimulation
from agentforge.ai.worldmodel.probability import UniverseProbability
from collections import defaultdict

class Galaxy:
    def __init__(self, metadata=None, config={}):
        self.metadata = metadata if metadata is not None else {}

        # Setup the univseral sim
        self.galaxy_concepts = {"Milky Way": Concept("Milky Way", "Galaxy")}
        self.up = UniverseProbability()
        self.up.setup() # setup the universe probability matricies
        self.star = Star()
        self.planet = Planet()
        self.lifeform = Lifeform()
        self.biome = Biome()
        self.moon = Moon()
        self.star_designations = star_designations
        self.designation_counters = {key: np.random.randint(0, 999) for key in self.star_designations}

        # Setp config for sim
        self.MIN_STAR_SPEED = 0.0005 if "MIN_STAR_SPEED" not in config else config["MIN_STAR_SPEED"]
        self.MAX_STAR_SPEED = 0.0015 if "MAX_STAR_SPEED" not in config else config["MAX_STAR_SPEED"]
        self.REPULSION_DISTANCE = 10 if "REPULSION_DISTANCE" not in config else config["REPULSION_DISTANCE"]
        self.NUM_SAMPLES = 100 if "NUM_SAMPLES" not in config else config["NUM_SAMPLES"]
        self.GALACTIC_SCALE_FACTOR = 5.0 if "GALACTIC_SCALE_FACTOR" not in config else config["GALACTIC_SCALE_FACTOR"]
        self.ALIEN_LIFE_PROBABILITY = 0.0001 if "ALIEN_LIFE_PROBABILITY" not in config else config["ALIEN_LIFE_PROBABILITY"]
        self.LIFE_PROBABILITY = 0.1 if "LIFE_PROBABILITY" not in config else config["LIFE_PROBABILITY"]
        self.STARFIELD_NUM = 2200 if "STARFIELD_NUM" not in config else config["STARFIELD_NUM"]
        self.NUM_ARMS = 4 if "NUM_ARMS" not in config else config["NUM_ARMS"]
        self.R_SPREAD = 9500 if "R_SPREAD" not in config else config["R_SPREAD"]
        self.CORE_RADIUS = 300 if "CORE_RADIUS" not in config else config["CORE_RADIUS"]
        self.ANIM_STEPS = 2500 if "ANIM_STEPS" not in config else config["ANIM_STEPS"]
        self.NOISE_SCALE = 100 if "NOISE_SCALE" not in config else config["NOISE_SCALE"]
        self.TIGHTNESS = 3 if "TIGHTNESS" not in config else config["TIGHTNESS"]
        self.NUM_SYSTEMS = 200 if "NUM_SYSTEMS" not in config else config["NUM_SYSTEMS"]

        self.star_simulation = StarSimulation(self.REPULSION_DISTANCE)

    async def generate_with_life(self):
        simulated_systems = int(math.ceil(self.LIFE_PROBABILITY * self.NUM_SYSTEMS) * (10000/28))
        print("Generating {} systems to sample life...".format(simulated_systems))
        return self.generate(simulated_systems)

    # generate a galaxy with solar systems and life preseance esrtimates
    # num_systems: int, simulated number of solar systems to generate to ensure life probability is met
    def generate(self, num_systems):
        system_names = self.get_system_name(num_systems)
        # From the macro to the micro, we build the world model
        self.systems = []
        self.has_life = []
        self.life_data = defaultdict(int)

        print("Generating star positions...")
        
        star_positions, starfield_positions = self.generate_spiral_positions(
            self.NUM_SYSTEMS,
            starfieldSystems=self.STARFIELD_NUM,
            core_systems_ratio=0.1,
            num_arms=self.NUM_ARMS,
            checkDistance=True,
            r_spread=self.R_SPREAD,
            core_radius=self.CORE_RADIUS,
            anim_steps=self.ANIM_STEPS,
            noise_scale=self.NOISE_SCALE,
            tightness=self.TIGHTNESS,
        )
    
        kd_tree = KDTree(np.array(star_positions))  # Rebuild KDTree with new star positions

        # Ensure that nearest_neighbors is a 2D array with correct dimensions
        nearest_neighbors = [kd_tree.query(position, k=6)[1][1:] for position in star_positions]

        neighbors_positions = star_positions[np.array(nearest_neighbors)]

        # Reshape star_positions for broadcasting
        star_positions_reshaped = star_positions[:, np.newaxis, :]

        # Calculate distances
        distances_matrix = np.linalg.norm(neighbors_positions - star_positions_reshaped, axis=2)

        print("Generating starfield positions...")
        star_names = list(self.star.star_concepts.keys())
        planet_names = list(self.planet.planet_concepts.keys())
        self.biome_names = list(self.biome.biome_concepts.keys())

        start_time = time.time()
        print("Generating systems...")
        self.up.setup() # setup the universe probability matricies
        star_probabilities = self.up.normalized_gx_s_df.iloc[0]
        for i in tqdm(range(num_systems), desc="Sampling solar systems..."):
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
            star_id = str(uuid4())
            solar_system_info = {
                "Name": name,
                "Star": star_type,
                # "Star Position": star_position.tolist(),
                "Star Information": self.star.star_concepts[star_type].metadata,
                "Star Mass (kg)": star_mass_kg,
                "Star Age (Gyr)": star_age_Gyr,
                "Number of Planets": num_planets,
                "Disk Mass": disk_mass,
                "Planets": [],
                "id": star_id
            }

            # Sample a planet type based on star type
            planet_probabilities = self.up.normalized_sx_p_df.iloc[star_index]
            for _ in range(num_planets):
                planet_type = np.random.choice(planet_names, p=planet_probabilities)
                planet_name = name_generator.get_next_name("planet")
                # Find the index of the sampled planet type
                planet_index = planet_names.index(planet_type)
                planet_info, estimated_biomes, life_presence = self.planet.generate(planet_type, star_mass_kg, star_type)
                planet_info["system_id"] = star_id

                # Small chance of alien lifeforms on strange new worlds
                if not life_presence and np.random.rand() < self.ALIEN_LIFE_PROBABILITY and planet_type not in ['oceanPlanet', 'terrestrial', 'superEarth']:
                    life_presence = True

                # Create and set names for satellites
                planet_info["Name"] = planet_name
                for moon in planet_info["Moons"]:
                    moon_name = name_generator.get_next_name("moon")
                    moon["Name"] = moon_name

                for _ in range(estimated_biomes):
                    biome_type = np.random.choice(self.biome_names, p=self.up.normalized_px_b_df.iloc[planet_index])

                    biome_info = {
                        "Biome Type": biome_type,
                        "Life Presence": life_presence,
                    }
                    if life_presence:
                        biome_info['evolved'] = False

                    if biome_type not in planet_info["Biomes"]:
                        planet_info["Biomes"][biome_type] = {}

                    planet_info["Biomes"][biome_type].update(biome_info)

                solar_system_info["Planets"].append(planet_info)

            self.systems.append(solar_system_info)

            if life_presence:
                self.has_life.append(solar_system_info)
                self.life_data[planet_type] += 1
                solar_system_info["Life"] = True

        end_time = time.time()
        print(f"System Generation Time elapsed: {end_time - start_time}")
        dead_systems = np.random.choice(self.systems, self.NUM_SYSTEMS - len(self.has_life), replace=False).tolist()
        self.systems = dead_systems + self.has_life

        # Setup neighbors
        for i, system in enumerate(self.systems):
            self.systems[i]['Star Position'] = star_positions[i].tolist()
            system['Neighbors'] = []
            dist_idx = 0
            for neighbor_index in nearest_neighbors[i]:
                neighbor = {
                    "id": self.systems[neighbor_index]['id'],
                    "Distance": str(distances_matrix[i, dist_idx]),
                    "Name": self.systems[neighbor_index]['Name'],
                }
                system['Neighbors'].append(neighbor)
                dist_idx += 1

        print(f"Systems With Life: {len(self.has_life)}")
        print(f"Planetary Life Report: {self.life_data}")

        return {
            "systems": self.systems,
            "starfield_positions": starfield_positions.tolist(),
        }

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
    
    def evolve_galaxy(self, star_positions, star_speeds, anim_steps):
        print("evolving galaxy...")
        start_time = time.time()

        # MANY ATTEMPTS HERE TO OPTIMIZE THE SIMULATION, Matricies, probability distributions, etc.
        # star_positions = self.monte_carlo_simulation(star_positions, star_speeds, 0.1, anim_steps)
        # star_positions = self.update_positions_with_random_speeds(star_positions, star_speeds, 0.1, anim_steps)

        # Slow but accurate
        for i in tqdm(range(anim_steps), desc="Aging Galaxy"):
            star_positions = self.update_positions_with_random_speeds_og(star_positions, star_speeds, i)
        
        end_time = time.time()
        print(f"evolved galaxy in {end_time - start_time} seconds")
        return star_positions

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

        star_positions = self.evolve_galaxy(star_positions, star_speeds, anim_steps)

        # Scale galaxy up to 10000 light years
        star_positions = star_positions * self.GALACTIC_SCALE_FACTOR
        starfield_indices = np.random.choice(len(star_positions), starfieldSystems, replace=False)
        starfields = star_positions[starfield_indices]

         # Create a mask to remove selected indices
        mask = np.ones(len(star_positions), dtype=bool)
        mask[starfield_indices] = False
        star_positions = star_positions[mask]

        return star_positions, starfields