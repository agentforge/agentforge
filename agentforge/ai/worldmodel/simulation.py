# Multiprocessing attempt for galaxy generation

from multiprocessing import Pool
import numpy as np
from scipy.spatial import KDTree

class StarSimulation:

    def __init__(self, REPULSION_DISTANCE):
        self.REPULSION_DISTANCE = REPULSION_DISTANCE

    def update_star_chunk(self, chunk_data):
        star_positions, star_speeds, kd_tree_data, time_steps = chunk_data
        kd_tree = KDTree(kd_tree_data)
        all_positions = []

        for time_step in time_steps:
            new_positions = np.copy(star_positions)
            for i, (pos, speed) in enumerate(zip(star_positions, star_speeds)):
                # Repulsion force logic
                distance, index = kd_tree.query(pos, k=2)
                if distance[1] < self.REPULSION_DISTANCE:
                    direction = pos - kd_tree_data[index[1]]
                    direction /= np.linalg.norm(direction)
                    new_positions[i] += direction * speed * time_step

                # Dark matter effect logic
                distance_from_center = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
                dark_matter_factor = 1 + np.exp(-distance_from_center / 2000)
                angle = np.arctan2(pos[1], pos[0])
                angle += (speed * dark_matter_factor) * time_step / (distance_from_center + 0.1)
                new_x = distance_from_center * np.cos(angle)
                new_y = distance_from_center * np.sin(angle)
                new_positions[i][0] = new_x
                new_positions[i][1] = new_y

            all_positions.append(new_positions)
            star_positions = new_positions

        return all_positions

    def update_positions_with_random_speeds_parallel(self, star_positions, star_speeds, anim_steps, num_processes=4):
        kd_tree_data = np.copy(star_positions)
        pool = Pool(num_processes)
        chunk_size = len(star_positions) // num_processes
        time_step_chunks = np.array_split(range(anim_steps), num_processes)

        chunks = [(star_positions[i:i + chunk_size], star_speeds[i:i + chunk_size], kd_tree_data, time_steps)
                  for i, time_steps in zip(range(0, len(star_positions), chunk_size), time_step_chunks)]

        results = pool.map(self.update_star_chunk, chunks)
        pool.close()
        pool.join()

        # Combining results
        combined_results = []
        for step in range(anim_steps):
            step_positions = np.vstack([result[step] for result in results])
            combined_results.append(step_positions)

        return combined_results