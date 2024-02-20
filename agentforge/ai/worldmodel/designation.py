import random
import time
# Simple Naming system for celestial bodies.
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

class SocietyNamingSystem:
    def __init__(self) -> None:
        # Load society names from a file
        societies = []
        with open("agentforge/ai/worldmodel/societies.txt", "r") as f:
            raw = f.read()

        societies = raw.split("\n")
        total_syllables = 0

        self.syllables = []

        # Analyze syllables in society names
        for s in societies:
            lex = s.split("-")
            total_syllables += len(lex)
            for l in lex:
                if l not in self.syllables:
                    self.syllables.append(l)
        # print("Syllables : " + str(len(self.syllables)))

        # Calculate diversity index
        div_index = len(self.syllables) / total_syllables
        div_index_str = str(div_index)[:4]
        # print("Diversity index : " + div_index_str)

        # Prepare for frequency analysis
        self.size = len(self.syllables) + 1
        self.freq = [[0] * self.size for i in range(self.size)]

        # Frequency analysis
        for s in societies:
            lex = s.split("-")
            i = 0
            while i < len(lex) - 1:
                self.freq[self.syllables.index(lex[i])][self.syllables.index(lex[i+1])] += 1
                i += 1
            self.freq[self.syllables.index(lex[len(lex) - 1])][self.size-1] += 1
        print('Frequency analysis : done!\n')

    def generate_name(self):
        # Generate society names
        num_names = 0
        society_name = ""
        names = []
        while num_names < 20:
            length = random.randint(2, 3)
            initial = random.randint(0, self.size - 2)
            while length > 0:
                while 1 not in self.freq[initial]:
                    initial = random.randint(0, self.size - 2)
                society_name += self.syllables[initial]
                initial = self.freq[initial].index(1)
                length -= 1
            names.append(society_name.capitalize())
            society_name = ""
            num_names += 1

        return random.choice(names)
