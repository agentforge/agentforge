from agentforge.ai.worldmodel.socialframework import SocialFramework

# Tech tree for pre-interstellar society
class TechnologicalFramework(SocialFramework):
    def __init__(self):
        super().__init__()

    dimensions = {}

    states = {
        "Warfare": [
            {"name": "Handheld Stone Tools", "point": 0.0, "description": "Prehistoric use of stones as basic weapons."},
            {"name": "Stone Weapons and Tools", "point": 0.11, "description": "Development of more sophisticated stone tools and weapons."},
            {"name": "Bronze Age Fortifications and Weapons", "point": 0.22, "description": "Introduction of bronze weapons and early defensive structures."},
            {"name": "Iron Age Defenses and Weaponry", "point": 0.33, "description": "Advancements in iron weapons and fortifications."},
            {"name": "City Walls and Fortifications", "point": 0.44, "description": "Construction of massive defensive walls around cities."},
            {"name": "Gunpowder and Cannons", "point": 0.56, "description": "Revolutionizing warfare with gunpowder-based weapons."},
            {"name": "Rifling and Breech-loading Weapons", "point": 0.67, "description": "Enhancements in firearm accuracy and reloading speed."},
            {"name": "Machine Guns and Artillery", "point": 0.78, "description": "Introduction of rapid-fire weapons and advanced artillery."},
            {"name": "Tanks and Armored Vehicles", "point": 0.89, "description": "Use of armored vehicles for ground warfare."},
            {"name": "Nuclear Weapons", "point": 1.0, "description": "Development of weapons with unprecedented destructive power."}
        ],
        "Transportation": [
            {"name": "Walking and Animal Riding", "point": 0.0, "description": "Earliest forms of transportation."},
            {"name": "Wheel and Sail", "point": 0.11, "description": "Invention of the wheel and sail for transportation."},
            {"name": "Horse-drawn Chariots and Boats", "point": 0.22, "description": "Use of animals and early boats for travel and trade."},
            {"name": "Roads and Bridges", "point": 0.33, "description": "Development of roads and bridges for easier travel."},
            {"name": "Navigational Advances", "point": 0.44, "description": "Improvements in navigation for sea and land travel."},
            {"name": "Steam Power", "point": 0.56, "description": "Adoption of steam power for trains and ships."},
            {"name": "Internal Combustion and Early Flight", "point": 0.67, "description": "Invention of cars and the first airplanes."},
            {"name": "Commercial Aviation and Highways", "point": 0.78, "description": "Expansion of commercial flights and highway systems."},
            {"name": "Space Travel", "point": 0.89, "description": "Human space exploration and satellite deployment."},
            {"name": "Hyperloop and Commercial Space Travel", "point": 1.0, "description": "Emerging high-speed ground transport and space tourism."}
        ],
        "Information Technology": [
            {"name": "Oral Tradition and Manuscript Culture", "point": 0.0, "description": "Preservation and transmission of knowledge orally and through manuscripts."},
            {"name": "Written Records", "point": 0.11, "description": "Development of writing systems and early record keeping."},
            {"name": "Printed Press", "point": 0.22, "description": "Invention of the printing press, enabling mass production of texts."},
            {"name": "Early Computing Devices", "point": 0.33, "description": "Creation of mechanical and analog computing devices."},
            {"name": "Electronic Computers", "point": 0.44, "description": "Development of electronic computers for various applications."},
            {"name": "Personal Computing and Internet", "point": 0.56, "description": "Widespread use of personal computers and the advent of the internet."},
            {"name": "Mobile Computing and Social Media", "point": 0.67, "description": "Rise of smartphones and social media platforms."},
            {"name": "Cloud Computing", "point": 0.78, "description": "Introduction of cloud services for storage and computing."},
            {"name": "Artificial Intelligence and Machine Learning", "point": 0.89, "description": "Advancements in AI technologies and their applications."},
            {"name": "Quantum Computing and AI", "point": 1.0, "description": "Emergence of quantum computing and advanced AI systems."}
        ],
        "Life Science": [
            {"name": "Herbal Remedies", "point": 0.0, "description": "Use of plants and natural substances to treat illnesses."},
            {"name": "Early Medical Practices", "point": 0.11, "description": "Development of structured medical practices in ancient civilizations."},
            {"name": "Anatomical Study", "point": 0.22, "description": "Early understanding of body structures and functions."},
            {"name": "Biological Discoveries", "point": 0.33, "description": "Significant discoveries in biology during the Renaissance."},
            {"name": "Microbiology", "point": 0.44, "description": "Study of microorganisms and their effects on humans."},
            {"name": "Germ Theory", "point": 0.56, "description": "Recognition of microbes causing diseases, leading to advances in hygiene and medicine."},
            {"name": "Genetic Engineering", "point": 0.67, "description": "Manipulation of genetic material for medical and agricultural purposes."},
            {"name": "Human Genome Project", "point": 0.78, "description": "Mapping and understanding all the genes of the human species."},
            {"name": "Stem Cell Research", "point": 0.89, "description": "Use of stem cells to treat or prevent a disease or condition."},
            {"name": "Personalized Medicine", "point": 1.0, "description": "Tailoring medical treatments to the individual genetic makeup."}
        ],
        "Physical Sciences": [
            {"name": "Observation of Natural Phenomena", "point": 0.0, "description": "Early human observation and interpretation of the natural world."},
            {"name": "Basic Elements", "point": 0.11, "description": "Early classification of matter into earth, water, air, and fire."},
            {"name": "Classical Mechanics", "point": 0.22, "description": "Foundational principles of physics that explain motion and physical laws."},
            {"name": "Scientific Revolution Discoveries", "point": 0.33, "description": "Advancements in understanding the physical universe during the Renaissance."},
            {"name": "Thermodynamics", "point": 0.44, "description": "Study of heat, work, and the energy of systems."},
            {"name": "Electromagnetism", "point": 0.56, "description": "Discovery and understanding of electromagnetic forces."},
            {"name": "Relativity", "point": 0.67, "description": "Theories of special and general relativity revolutionizing physics."},
            {"name": "Nuclear Physics", "point": 0.78, "description": "Study of atomic nuclei and their constituents and interactions."},
            {"name": "Quantum Mechanics", "point": 0.89, "description": "Study of particles at the smallest scales, fundamentally changing our understanding of matter and energy."},
            {"name": "Unified Field Theory", "point": 1.0, "description": "Theoretical framework that attempts to describe all fundamental forces and matter in a single, all-encompassing theory."}
        ],
        "Engineering": [
            {"name": "Stone Tools and Basic Structures", "point": 0.0, "description": "The use of stone tools and construction of simple shelters."},
            {"name": "Simple Machines", "point": 0.11, "description": "Invention of lever, wheel, and pulley to perform tasks more efficiently."},
            {"name": "Water Management Systems", "point": 0.22, "description": "Development of irrigation, aqueducts, and early hydraulic engineering."},
            {"name": "Roman Engineering", "point": 0.33, "description": "Advanced road networks, bridges, and architectural achievements."},
            {"name": "Mechanical Clocks and Windmills", "point": 0.44, "description": "Innovations in timekeeping and harnessing wind power."},
            {"name": "Civil Engineering", "point": 0.56, "description": "Design and construction of public works, such as roads and bridges."},
            {"name": "Steam Engine and Railways", "point": 0.67, "description": "The steam engine's invention leading to the railway system's development."},
            {"name": "Electrification and Telecommunications", "point": 0.78, "description": "Widespread adoption of electrical power and the invention of telecommunication devices."},
            {"name": "Computers and Software Engineering", "point": 0.89, "description": "Development of digital computers and the field of software engineering."},
            {"name": "Artificial Intelligence and Robotics", "point": 1.0, "description": "Advances in AI and robotics transforming engineering practices."}
        ],
        "Applied Sciences": [
            {"name": "Domestication of Plants and Animals", "point": 0.0, "description": "Early agricultural practices and animal domestication."},
            {"name": "Agricultural Innovations", "point": 0.11, "description": "Introduction of plow and crop rotation techniques."},
            {"name": "Alchemy to Chemistry", "point": 0.22, "description": "Transformation from mystical practices to scientific chemistry."},
            {"name": "Medical Practice", "point": 0.33, "description": "Advancements in medical knowledge and practices."},
            {"name": "Industrial Chemistry and Pharmaceuticals", "point": 0.44, "description": "Development of chemical industry and modern pharmaceuticals."},
            {"name": "Public Health and Sanitation", "point": 0.56, "description": "Establishment of public health systems and sanitation."},
            {"name": "Environmental Science", "point": 0.67, "description": "Recognition and study of environmental issues."},
            {"name": "Genetic Engineering", "point": 0.78, "description": "Manipulation of organisms' genetic material."},
            {"name": "Information Technology", "point": 0.89, "description": "Expansion of computing and information technology."},
            {"name": "Synthetic Biology and Nanotechnology", "point": 1.0, "description": "Emerging fields focusing on modifying living organisms and manipulating materials at the nanoscale."}
        ],
        "Agriculture and Pastoralism": [
            {"name": "Foraging to Early Farming", "point": 0.0, "description": "Transition from hunter-gatherer societies to rudimentary farming."},
            {"name": "Nomadic Herding", "point": 0.11, "description": "Pastoral nomadism involving the seasonal movement of livestock."},
            {"name": "Irrigation and Crop Specialization", "point": 0.22, "description": "Introduction of irrigation and specialization in specific crops."},
            {"name": "Three-Field System", "point": 0.33, "description": "Medieval crop rotation system improving land use efficiency."},
            {"name": "Agricultural Revolution", "point": 0.44, "description": "18th-century innovations that increased food production."},
            {"name": "Mechanization of Agriculture", "point": 0.56, "description": "Use of machinery to increase agricultural productivity."},
            {"name": "Green Revolution", "point": 0.67, "description": "Mid-20th century advancements in agricultural technology and practices."},
            {"name": "Genetically Modified Organisms", "point": 0.78, "description": "Introduction of genetically modified crops for agriculture."},
            {"name": "Organic Farming", "point": 0.89, "description": "Adoption of natural farming methods without synthetic inputs."},
            {"name": "Vertical Farming and Lab-grown Meat", "point": 1.0, "description": "Innovative farming techniques including vertical farms and cultured meat production."}
        ],
        "Interdisciplinary Science": [
        {
            "name": "Observational Astronomy and Natural Philosophy",
            "description": "Early human observations of celestial bodies and philosophical inquiries into the natural world.",
            "point": 0.0
        },
        {
            "name": "Ancient Engineering and Mathematics",
            "description": "Integration of engineering principles and mathematical calculations in ancient constructions and tools.",
            "point": 0.11
        },
        {
            "name": "Classical Antiquity's Natural Sciences",
            "description": "Fusion of astronomy, physics, and biology in classical Greek and Roman scholarly works.",
            "point": 0.22
        },
        {
            "name": "Medieval Alchemy and Astrology",
            "description": "Combination of chemical, astronomical, and mystical studies in search of universal truths and materials.",
            "point": 0.33
        },
        {
            "name": "Renaissance Humanism and Naturalism",
            "description": "Interdisciplinary approach to studying the natural world, human anatomy, and artistic expression.",
            "point": 0.44
        },
        {
            "name": "Scientific Revolution and Methodology",
            "description": "Development of the scientific method, integrating experimental physics, chemistry, and astronomy.",
            "point": 0.56
        },
        {
            "name": "Industrial Era Technological Convergence",
            "description": "Fusion of mechanical engineering, physics, and chemistry leading to industrial advancements.",
            "point": 0.67
        },
        {
            "name": "Modern Environmental and Earth Sciences",
            "description": "Integration of biology, chemistry, and geology to address environmental issues and understand Earth systems.",
            "point": 0.78
        },
        {
            "name": "Postmodern Computational and Systems Biology",
            "description": "Use of computational models to understand complex biological systems, integrating biology, computer science, and mathematics.",
            "point": 0.89
        },
        {
            "name": "Future Quantum and Interstellar Sciences",
            "description": "Advanced interdisciplinary fields exploring quantum mechanics, astrophysics, and potential interstellar travel.",
            "point": 1.0
        }
        ]
    }