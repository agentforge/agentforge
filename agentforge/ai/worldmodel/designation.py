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

### List of star designations
star_designations = [
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