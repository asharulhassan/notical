import json
import os
from datetime import datetime

class ComprehensiveHumanitiesDeckCreator:
    def __init__(self):
        self.output_dir = "comprehensive_humanities_deck"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_history_section(self):
        """Create comprehensive history section"""
        print("📚 Creating History section...")
        
        history_concepts = {
            # Ancient Civilizations
            "Ancient Egypt": "Civilization along the Nile River (3100-30 BCE) known for pyramids, pharaohs, hieroglyphics, and mummification.",
            "Ancient Greece": "Civilization (800-146 BCE) that developed democracy, philosophy, theater, and Olympic Games.",
            "Ancient Rome": "Empire (753 BCE-476 CE) that built roads, aqueducts, and created a legal system that influenced modern law.",
            "Mesopotamia": "Region between Tigris and Euphrates rivers where the first cities, writing (cuneiform), and agriculture developed.",
            "Indus Valley": "Ancient civilization (3300-1300 BCE) in South Asia known for advanced urban planning and drainage systems.",
            "Ancient China": "Civilization along the Yellow River that developed paper, gunpowder, compass, and printing.",
            "Maya Civilization": "Mesoamerican civilization (2000 BCE-1500 CE) known for pyramids, calendar system, and hieroglyphic writing.",
            "Aztec Empire": "Mesoamerican empire (1345-1521) centered in Tenochtitlan, known for human sacrifice and advanced architecture.",
            "Inca Empire": "South American empire (1438-1533) known for Machu Picchu, road systems, and terrace farming.",
            "Persian Empire": "Ancient empire (550-330 BCE) that ruled from Egypt to India, known for tolerance and administrative efficiency.",
            
            # Medieval Period
            "Feudalism": "Social system where land was exchanged for military service and loyalty to lords.",
            "Crusades": "Series of religious wars (1095-1291) between Christians and Muslims for control of the Holy Land.",
            "Black Death": "Plague pandemic (1347-1351) that killed 30-60% of Europe's population.",
            "Magna Carta": "Document signed in 1215 that limited the power of English kings and established basic rights.",
            "Hundred Years' War": "Conflict (1337-1453) between England and France over French territory.",
            "Renaissance": "Period of cultural rebirth (14th-17th centuries) marked by renewed interest in classical learning and art.",
            "Reformation": "Religious movement (16th century) that led to the creation of Protestant churches.",
            "Age of Exploration": "Period (15th-17th centuries) when European nations explored and colonized other parts of the world.",
            "Enlightenment": "Intellectual movement (17th-18th centuries) emphasizing reason, individualism, and skepticism.",
            "Industrial Revolution": "Period (1760-1840) when manufacturing shifted from hand production to machines.",
            
            # Modern Era
            "French Revolution": "Period of radical social and political upheaval in France (1789-1799) that overthrew the monarchy.",
            "American Revolution": "Colonial revolt (1765-1783) that resulted in United States independence from Great Britain.",
            "Napoleonic Wars": "Series of conflicts (1803-1815) involving Napoleon Bonaparte's French Empire against various European coalitions.",
            "American Civil War": "Conflict (1861-1865) between Northern and Southern states over slavery and states' rights.",
            "World War I": "Global conflict (1914-1918) involving most European nations, resulting in millions of casualties.",
            "Russian Revolution": "Revolution (1917) that overthrew the Russian monarchy and established the Soviet Union.",
            "Great Depression": "Severe worldwide economic downturn (1929-1939) marked by high unemployment and poverty.",
            "World War II": "Global conflict (1939-1945) involving most nations, ending with the use of atomic bombs.",
            "Cold War": "Period of geopolitical tension (1947-1991) between the United States and Soviet Union.",
            "Civil Rights Movement": "Social movement (1954-1968) in the United States to end racial segregation and discrimination.",
            "Vietnam War": "Conflict (1955-1975) between North and South Vietnam, with US involvement.",
            "Fall of Berlin Wall": "Event (1989) symbolizing the end of the Cold War and division of Germany.",
            "9/11 Attacks": "Terrorist attacks (2001) on the World Trade Center and Pentagon that changed US foreign policy.",
            "Arab Spring": "Series of anti-government protests and uprisings across the Arab world (2010-2012).",
            "COVID-19 Pandemic": "Global pandemic (2019-present) caused by coronavirus that affected economies and societies worldwide."
        }
        
        cards = []
        for concept, explanation in history_concepts.items():
            card = {
                "front": f"Explain the historical event/period: {concept}",
                "back": explanation,
                "type": "history",
                "category": "history",
                "difficulty": "intermediate",
                "tags": ["history", "humanities", "events"]
            }
            cards.append(card)
        
        return cards
    
    def create_geography_section(self):
        """Create comprehensive geography section"""
        print("📚 Creating Geography section...")
        
        geography_concepts = {
            # Physical Geography
            "Plate Tectonics": "Theory that Earth's outer shell is divided into plates that move over the mantle, causing earthquakes and volcanoes.",
            "Weathering": "Process of breaking down rocks and minerals on Earth's surface through physical, chemical, or biological means.",
            "Erosion": "Process of wearing away Earth's surface by water, wind, or ice, creating landforms like valleys and canyons.",
            "Deposition": "Process of dropping sediments in new locations, building up landforms like deltas and beaches.",
            "Climate Zones": "Large areas of Earth with similar weather patterns: tropical, temperate, and polar zones.",
            "Biomes": "Large ecological areas with similar climate, plants, and animals: desert, forest, grassland, tundra, aquatic.",
            "Ecosystems": "Communities of living organisms interacting with their physical environment.",
            "Water Cycle": "Continuous movement of water on, above, and below Earth's surface through evaporation, condensation, and precipitation.",
            "Carbon Cycle": "Movement of carbon between the atmosphere, oceans, soil, and living organisms.",
            "Rock Cycle": "Process by which rocks change from one type to another through weathering, erosion, and heat/pressure.",
            
            # Human Geography
            "Population Density": "Number of people living in a given area, usually measured as people per square kilometer.",
            "Urbanization": "Process of population concentration in cities and towns, leading to urban growth and development.",
            "Migration": "Movement of people from one place to another, either within a country (internal) or between countries (international).",
            "Cultural Diffusion": "Spread of cultural beliefs, practices, and ideas from one society to another.",
            "Globalization": "Process of increasing interconnectedness and interdependence among countries through trade, technology, and culture.",
            "Demographics": "Statistical characteristics of human populations, including age, gender, income, education, and ethnicity.",
            "Economic Development": "Process of improving economic well-being and quality of life for a country's population.",
            "Sustainable Development": "Development that meets present needs without compromising future generations' ability to meet their own needs.",
            "Cultural Landscape": "Visible features of an area shaped by human activity and culture.",
            "Environmental Impact": "Effect of human activities on the natural environment, including pollution and habitat destruction.",
            
            # Regional Geography
            "Continents": "Seven large landmasses: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.",
            "Oceans": "Five major bodies of saltwater: Pacific, Atlantic, Indian, Southern, and Arctic.",
            "Mountain Ranges": "Chains of mountains formed by tectonic activity, including Himalayas, Andes, Rockies, and Alps.",
            "Rivers": "Natural flowing watercourses that drain into oceans, lakes, or other rivers.",
            "Deserts": "Arid regions with little precipitation, including Sahara, Arabian, Gobi, and Mojave.",
            "Rainforests": "Dense forests with high rainfall, including Amazon, Congo, and Southeast Asian rainforests.",
            "Tundra": "Treeless Arctic regions with permanently frozen subsoil and low-growing vegetation.",
            "Savanna": "Grassland ecosystems with scattered trees, found in tropical and subtropical regions.",
            "Mediterranean Climate": "Climate characterized by hot, dry summers and mild, wet winters.",
            "Monsoon": "Seasonal wind pattern that brings heavy rainfall to certain regions, especially South Asia."
        }
        
        cards = []
        for concept, explanation in geography_concepts.items():
            card = {
                "front": f"Define the geographical concept: {concept}",
                "back": explanation,
                "type": "geography",
                "category": "geography",
                "difficulty": "intermediate",
                "tags": ["geography", "humanities", "earth"]
            }
            cards.append(card)
        
        return cards
    
    def create_philosophy_section(self):
        """Create comprehensive philosophy section"""
        print("📚 Creating Philosophy section...")
        
        philosophy_concepts = {
            # Branches of Philosophy
            "Metaphysics": "Branch of philosophy concerned with the fundamental nature of reality and existence.",
            "Epistemology": "Branch of philosophy concerned with the nature and scope of knowledge.",
            "Ethics": "Branch of philosophy concerned with moral principles and values.",
            "Logic": "Branch of philosophy concerned with valid reasoning and argumentation.",
            "Aesthetics": "Branch of philosophy concerned with beauty, art, and taste.",
            "Political Philosophy": "Branch of philosophy concerned with government, justice, and social organization.",
            
            # Major Philosophical Concepts
            "Dualism": "Belief that mind and body are fundamentally different substances.",
            "Materialism": "Belief that only matter exists and everything can be explained in material terms.",
            "Idealism": "Belief that reality is fundamentally mental or spiritual rather than physical.",
            "Empiricism": "Belief that knowledge comes primarily from sensory experience and observation.",
            "Rationalism": "Belief that knowledge comes primarily from reason and logical thinking.",
            "Skepticism": "Philosophical position that questions the possibility of certain knowledge.",
            "Relativism": "Belief that truth and morality are relative to culture, society, or individual perspective.",
            "Absolutism": "Belief that certain principles are universally true regardless of context.",
            "Utilitarianism": "Ethical theory that actions are right if they promote the greatest happiness for the greatest number.",
            "Deontology": "Ethical theory that actions are right or wrong based on their adherence to moral rules or duties.",
            
            # Famous Philosophers
            "Socrates": "Ancient Greek philosopher (470-399 BCE) known for the Socratic method and questioning approach.",
            "Plato": "Ancient Greek philosopher (428-348 BCE) who founded the Academy and wrote philosophical dialogues.",
            "Aristotle": "Ancient Greek philosopher (384-322 BCE) who studied logic, ethics, politics, and natural sciences.",
            "Confucius": "Chinese philosopher (551-479 BCE) whose teachings emphasized moral behavior and social harmony.",
            "Descartes": "French philosopher (1596-1650) known for 'Cogito, ergo sum' and mind-body dualism.",
            "Kant": "German philosopher (1724-1804) who developed deontological ethics and transcendental idealism.",
            "Nietzsche": "German philosopher (1844-1900) known for critiques of morality and the concept of the Übermensch.",
            "Sartre": "French philosopher (1905-1980) associated with existentialism and human freedom.",
            "Foucault": "French philosopher (1926-1984) who studied power, knowledge, and social institutions.",
            "Chomsky": "American philosopher (1928-present) known for work on language, politics, and media."
        }
        
        cards = []
        for concept, explanation in philosophy_concepts.items():
            card = {
                "front": f"Explain the philosophical concept: {concept}",
                "back": explanation,
                "type": "philosophy",
                "category": "philosophy",
                "difficulty": "advanced",
                "tags": ["philosophy", "humanities", "thinking"]
            }
            cards.append(card)
        
        return cards
    
    def create_sociology_section(self):
        """Create comprehensive sociology section"""
        print("📚 Creating Sociology section...")
        
        sociology_concepts = {
            # Social Theories
            "Functionalism": "Theory that society is a system of interconnected parts that work together to maintain stability.",
            "Conflict Theory": "Theory that society is characterized by inequality and conflict between different groups.",
            "Symbolic Interactionism": "Theory that society is created through everyday interactions and shared meanings.",
            "Social Constructionism": "Theory that reality is socially constructed through human interaction and language.",
            "Feminist Theory": "Theory that examines gender inequality and advocates for women's rights and equality.",
            "Critical Race Theory": "Theory that examines how race and racism are embedded in social structures and institutions.",
            
            # Social Institutions
            "Family": "Social institution that provides emotional support, socialization, and economic cooperation.",
            "Education": "Social institution that transmits knowledge, skills, and cultural values to new generations.",
            "Religion": "Social institution that provides meaning, purpose, and moral guidance to individuals and communities.",
            "Government": "Social institution that exercises authority and control over a society.",
            "Economy": "Social institution that organizes the production, distribution, and consumption of goods and services.",
            "Media": "Social institution that communicates information, entertainment, and cultural content to the public.",
            
            # Social Processes
            "Socialization": "Process by which individuals learn the norms, values, and behaviors of their society.",
            "Social Stratification": "System of ranking individuals and groups in a hierarchy based on wealth, power, and prestige.",
            "Social Mobility": "Movement of individuals or groups between different social positions.",
            "Deviance": "Behavior that violates social norms and expectations.",
            "Social Control": "Mechanisms used by society to ensure conformity to social norms.",
            "Social Change": "Transformation of social institutions, behaviors, and relationships over time.",
            
            # Social Issues
            "Poverty": "Condition of lacking basic material needs and resources for a decent standard of living.",
            "Inequality": "Unequal distribution of resources, opportunities, and power among different groups.",
            "Discrimination": "Unfair treatment of individuals or groups based on characteristics like race, gender, or religion.",
            "Social Movements": "Organized efforts by groups to bring about social or political change.",
            "Globalization": "Process of increasing interconnectedness and interdependence among societies worldwide.",
            "Environmental Sociology": "Study of the relationship between society and the natural environment."
        }
        
        cards = []
        for concept, explanation in sociology_concepts.items():
            card = {
                "front": f"Define the sociological concept: {concept}",
                "back": explanation,
                "type": "sociology",
                "category": "sociology",
                "difficulty": "intermediate",
                "tags": ["sociology", "humanities", "society"]
            }
            cards.append(card)
        
        return cards
    
    def create_psychology_section(self):
        """Create comprehensive psychology section"""
        print("📚 Creating Psychology section...")
        
        psychology_concepts = {
            # Branches of Psychology
            "Clinical Psychology": "Branch that studies, assesses, and treats people with psychological disorders.",
            "Cognitive Psychology": "Branch that studies mental processes like thinking, memory, and problem-solving.",
            "Developmental Psychology": "Branch that studies how people change and grow throughout their lives.",
            "Social Psychology": "Branch that studies how people's thoughts, feelings, and behaviors are influenced by others.",
            "Behavioral Psychology": "Branch that studies observable behavior and learning processes.",
            "Biological Psychology": "Branch that studies the biological basis of behavior and mental processes.",
            
            # Psychological Concepts
            "Consciousness": "Awareness of one's thoughts, feelings, and surroundings.",
            "Memory": "Process of encoding, storing, and retrieving information.",
            "Learning": "Process of acquiring new knowledge, skills, or behaviors.",
            "Motivation": "Internal and external factors that drive behavior toward goals.",
            "Emotion": "Complex psychological and physiological state that influences thoughts and behavior.",
            "Personality": "Enduring patterns of thoughts, feelings, and behaviors that characterize an individual.",
            "Intelligence": "Ability to learn, reason, problem-solve, and adapt to new situations.",
            "Stress": "Body's response to demands or threats, both real and perceived.",
            "Mental Health": "State of psychological well-being and ability to function effectively in daily life.",
            "Psychological Disorders": "Patterns of thoughts, feelings, or behaviors that cause distress or impairment.",
            
            # Famous Psychologists
            "Sigmund Freud": "Austrian neurologist (1856-1939) who founded psychoanalysis and studied the unconscious mind.",
            "B.F. Skinner": "American psychologist (1904-1990) who studied operant conditioning and behaviorism.",
            "Jean Piaget": "Swiss psychologist (1896-1980) who studied cognitive development in children.",
            "Carl Jung": "Swiss psychiatrist (1875-1961) who developed analytical psychology and studied the collective unconscious.",
            "Abraham Maslow": "American psychologist (1908-1970) who developed the hierarchy of needs.",
            "Ivan Pavlov": "Russian physiologist (1849-1936) who studied classical conditioning with dogs.",
            "Erik Erikson": "German-American psychologist (1902-1994) who developed the theory of psychosocial development.",
            "Albert Bandura": "Canadian-American psychologist (1925-2021) who studied social learning and self-efficacy.",
            "Lev Vygotsky": "Russian psychologist (1896-1934) who studied social and cultural influences on development.",
            "William James": "American psychologist (1842-1910) who founded functionalism and wrote 'Principles of Psychology.'"
        }
        
        cards = []
        for concept, explanation in psychology_concepts.items():
            card = {
                "front": f"Explain the psychological concept: {concept}",
                "back": explanation,
                "type": "psychology",
                "category": "psychology",
                "difficulty": "intermediate",
                "tags": ["psychology", "humanities", "mind"]
            }
            cards.append(card)
        
        return cards
    
    def create_comprehensive_humanities_deck(self):
        """Create one massive comprehensive Humanities deck"""
        print("🚀 Creating ONE comprehensive Humanities deck with ALL content...")
        
        # Generate all sections
        history_cards = self.create_history_section()
        geography_cards = self.create_geography_section()
        philosophy_cards = self.create_philosophy_section()
        sociology_cards = self.create_sociology_section()
        psychology_cards = self.create_psychology_section()
        
        # Combine all cards
        all_cards = history_cards + geography_cards + philosophy_cards + sociology_cards + psychology_cards
        
        # Create comprehensive deck
        comprehensive_deck = {
            "deck_info": {
                "name": "Comprehensive Humanities Master Deck",
                "description": "Complete Humanities deck covering History, Geography, Philosophy, Sociology, and Psychology",
                "total_cards": len(all_cards),
                "created_date": datetime.now().isoformat(),
                "version": "1.0"
            },
            "sections": {
                "history": {
                    "name": "History",
                    "cards": history_cards,
                    "total_cards": len(history_cards),
                    "description": "Major historical events, periods, and civilizations"
                },
                "geography": {
                    "name": "Geography",
                    "cards": geography_cards,
                    "total_cards": len(geography_cards),
                    "description": "Physical and human geography concepts"
                },
                "philosophy": {
                    "name": "Philosophy",
                    "cards": philosophy_cards,
                    "total_cards": len(philosophy_cards),
                    "description": "Philosophical concepts, theories, and thinkers"
                },
                "sociology": {
                    "name": "Sociology",
                    "cards": sociology_cards,
                    "total_cards": len(sociology_cards),
                    "description": "Social theories, institutions, and processes"
                },
                "psychology": {
                    "name": "Psychology",
                    "cards": psychology_cards,
                    "total_cards": len(psychology_cards),
                    "description": "Psychological concepts, theories, and research"
                }
            },
            "all_cards": all_cards,
            "statistics": {
                "total_cards": len(all_cards),
                "history_cards": len(history_cards),
                "geography_cards": len(geography_cards),
                "philosophy_cards": len(philosophy_cards),
                "sociology_cards": len(sociology_cards),
                "psychology_cards": len(psychology_cards)
            }
        }
        
        # Save comprehensive deck
        filename = "comprehensive_humanities_master_deck.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_deck, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Comprehensive Humanities deck created!")
        print(f"📊 Total cards: {len(all_cards)}")
        print(f"📁 Saved to: {filepath}")
        print(f"🎯 Ready for complex subjects next!")
        
        return comprehensive_deck

def main():
    creator = ComprehensiveHumanitiesDeckCreator()
    comprehensive_deck = creator.create_comprehensive_humanities_deck()
    
    print(f"\n🎉 COMPREHENSIVE HUMANITIES DECK COMPLETE!")
    print("🚀 We now have ONE massive Humanities deck with everything!")
    print("🎯 Next: Create comprehensive complex subjects deck!")

if __name__ == "__main__":
    main()
