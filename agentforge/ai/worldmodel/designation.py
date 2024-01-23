# Naming system for celestial bodies.

class CelestialNamingSystem:
    def __init__(self, system_name):
        self.system_name = system_name
        self.discovery_counts = {
            'planet': 0,
            'asteroid': 0,
            'moon': 0,
        }

    def get_next_name(self, body_type):
        self.discovery_counts[body_type] += 1
        return self._generate_name(body_type, self.discovery_counts[body_type])

    def _generate_name(self, body_type, order):
        if body_type == 'planet':
            planet_letter = chr(96 + order)
            return f'{self.system_name} {planet_letter}'
        elif body_type == 'asteroid':
            return f'{self.system_name} Asteroid {order}'
        elif body_type == 'moon':
            return f'{self.system_name} Moon {self._int_to_roman(order)}'

    def _int_to_roman(self, num):
        roman_map = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
            6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
            # Extend this map for larger numbers
        }
        return roman_map.get(num, '')
