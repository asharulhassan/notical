import json
import time
import os

class ComplexSubjectsDeckCreator:
    def __init__(self):
        self.decks = []
        
    def create_physics_deck(self):
        """Create comprehensive Physics deck"""
        print("Creating Physics deck...")
        
        physics_deck = {
            'name': 'Physics Master',
            'category': 'Physics',
            'cards': []
        }
        
        # Mechanics
        mechanics = [
            ('Newton\'s First Law', 'What is Newton\'s First Law?', 'Object at rest stays at rest, object in motion stays in motion unless acted upon by force'),
            ('Newton\'s Second Law', 'What is Newton\'s Second Law?', 'Force equals mass times acceleration (F=ma)'),
            ('Newton\'s Third Law', 'What is Newton\'s Third Law?', 'For every action there is an equal and opposite reaction'),
            ('Gravity', 'What is the formula for gravitational force?', 'F = G(m1*m2)/r²'),
            ('Kinetic Energy', 'What is the formula for kinetic energy?', 'KE = ½mv²'),
            ('Potential Energy', 'What is the formula for gravitational potential energy?', 'PE = mgh'),
            ('Momentum', 'What is the formula for momentum?', 'p = mv'),
            ('Work', 'What is the formula for work?', 'W = Fd'),
            ('Power', 'What is the formula for power?', 'P = W/t'),
            ('Friction', 'What is the formula for friction?', 'f = μN')
        ]
        
        # Thermodynamics
        thermodynamics = [
            ('First Law', 'What is the First Law of Thermodynamics?', 'Energy cannot be created or destroyed, only transformed'),
            ('Second Law', 'What is the Second Law of Thermodynamics?', 'Entropy always increases in isolated systems'),
            ('Temperature', 'What is temperature?', 'Measure of average kinetic energy of particles'),
            ('Heat', 'What is heat?', 'Transfer of thermal energy'),
            ('Specific Heat', 'What is specific heat?', 'Amount of heat needed to raise 1kg by 1°C'),
            ('Latent Heat', 'What is latent heat?', 'Heat needed for phase change without temperature change'),
            ('Conduction', 'What is conduction?', 'Heat transfer through direct contact'),
            ('Convection', 'What is convection?', 'Heat transfer through fluid movement'),
            ('Radiation', 'What is radiation?', 'Heat transfer through electromagnetic waves'),
            ('Efficiency', 'What is efficiency?', 'Ratio of useful work output to total energy input')
        ]
        
        # Waves
        waves = [
            ('Wave', 'What is a wave?', 'Disturbance that transfers energy through medium'),
            ('Frequency', 'What is frequency?', 'Number of complete cycles per second'),
            ('Wavelength', 'What is wavelength?', 'Distance between consecutive wave peaks'),
            ('Amplitude', 'What is amplitude?', 'Maximum displacement from equilibrium'),
            ('Period', 'What is period?', 'Time for one complete cycle'),
            ('Wave Speed', 'What is the formula for wave speed?', 'v = fλ'),
            ('Reflection', 'What is reflection?', 'Wave bouncing off surface'),
            ('Refraction', 'What is refraction?', 'Wave changing direction at boundary'),
            ('Diffraction', 'What is diffraction?', 'Wave bending around obstacles'),
            ('Interference', 'What is interference?', 'Waves combining to form new pattern')
        ]
        
        # Electricity
        electricity = [
            ('Current', 'What is electric current?', 'Flow of electric charge'),
            ('Voltage', 'What is voltage?', 'Electric potential difference'),
            ('Resistance', 'What is resistance?', 'Opposition to current flow'),
            ('Ohm\'s Law', 'What is Ohm\'s Law?', 'V = IR'),
            ('Power', 'What is the formula for electrical power?', 'P = VI'),
            ('Series Circuit', 'What is a series circuit?', 'Components connected end-to-end'),
            ('Parallel Circuit', 'What is a parallel circuit?', 'Components connected across same voltage'),
            ('Capacitor', 'What is a capacitor?', 'Device that stores electric charge'),
            ('Inductor', 'What is an inductor?', 'Device that stores magnetic energy'),
            ('Magnetic Field', 'What is a magnetic field?', 'Region where magnetic forces act')
        ]
        
        # Add all physics cards
        for category in [mechanics, thermodynamics, waves, electricity]:
            for item in category:
                physics_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'physics',
                    'difficulty': 'medium'
                })
        
        self.decks.append(physics_deck)
        print(f"Created Physics deck with {len(physics_deck['cards'])} cards")
    
    def create_chemistry_deck(self):
        """Create comprehensive Chemistry deck"""
        print("Creating Chemistry deck...")
        
        chemistry_deck = {
            'name': 'Chemistry Master',
            'category': 'Chemistry',
            'cards': []
        }
        
        # Atomic Structure
        atomic_structure = [
            ('Atom', 'What is an atom?', 'Smallest unit of element that retains properties'),
            ('Proton', 'What is a proton?', 'Positively charged subatomic particle'),
            ('Neutron', 'What is a neutron?', 'Neutrally charged subatomic particle'),
            ('Electron', 'What is an electron?', 'Negatively charged subatomic particle'),
            ('Atomic Number', 'What is atomic number?', 'Number of protons in nucleus'),
            ('Mass Number', 'What is mass number?', 'Sum of protons and neutrons'),
            ('Isotope', 'What is an isotope?', 'Atoms with same protons but different neutrons'),
            ('Ion', 'What is an ion?', 'Atom with net electric charge'),
            ('Cation', 'What is a cation?', 'Positively charged ion'),
            ('Anion', 'What is an anion?', 'Negatively charged ion')
        ]
        
        # Chemical Bonding
        chemical_bonding = [
            ('Ionic Bond', 'What is an ionic bond?', 'Bond formed by transfer of electrons'),
            ('Covalent Bond', 'What is a covalent bond?', 'Bond formed by sharing electrons'),
            ('Metallic Bond', 'What is a metallic bond?', 'Bond formed by delocalized electrons'),
            ('Polar Bond', 'What is a polar bond?', 'Covalent bond with unequal electron sharing'),
            ('Nonpolar Bond', 'What is a nonpolar bond?', 'Covalent bond with equal electron sharing'),
            ('Single Bond', 'What is a single bond?', 'Bond sharing one pair of electrons'),
            ('Double Bond', 'What is a double bond?', 'Bond sharing two pairs of electrons'),
            ('Triple Bond', 'What is a triple bond?', 'Bond sharing three pairs of electrons'),
            ('Hydrogen Bond', 'What is a hydrogen bond?', 'Weak bond between hydrogen and electronegative atom'),
            ('Van der Waals', 'What are Van der Waals forces?', 'Weak intermolecular forces')
        ]
        
        # Chemical Reactions
        chemical_reactions = [
            ('Synthesis', 'What is a synthesis reaction?', 'Two or more substances combine to form one'),
            ('Decomposition', 'What is a decomposition reaction?', 'One substance breaks down into two or more'),
            ('Single Replacement', 'What is a single replacement reaction?', 'One element replaces another in compound'),
            ('Double Replacement', 'What is a double replacement reaction?', 'Two compounds exchange ions'),
            ('Combustion', 'What is a combustion reaction?', 'Reaction with oxygen producing heat and light'),
            ('Oxidation', 'What is oxidation?', 'Loss of electrons'),
            ('Reduction', 'What is reduction?', 'Gain of electrons'),
            ('Catalyst', 'What is a catalyst?', 'Substance that speeds up reaction without being consumed'),
            ('Inhibitor', 'What is an inhibitor?', 'Substance that slows down reaction'),
            ('Equilibrium', 'What is chemical equilibrium?', 'Forward and reverse reactions occur at equal rates')
        ]
        
        # Add all chemistry cards
        for category in [atomic_structure, chemical_bonding, chemical_reactions]:
            for item in category:
                chemistry_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'chemistry',
                    'difficulty': 'medium'
                })
        
        self.decks.append(chemistry_deck)
        print(f"Created Chemistry deck with {len(chemistry_deck['cards'])} cards")
    
    def create_mathematics_deck(self):
        """Create comprehensive Mathematics deck"""
        print("Creating Mathematics deck...")
        
        mathematics_deck = {
            'name': 'Mathematics Master',
            'category': 'Mathematics',
            'cards': []
        }
        
        # Algebra
        algebra = [
            ('Variable', 'What is a variable?', 'Symbol representing unknown value'),
            ('Equation', 'What is an equation?', 'Mathematical statement with equals sign'),
            ('Inequality', 'What is an inequality?', 'Mathematical statement with comparison symbols'),
            ('Function', 'What is a function?', 'Relation where each input has one output'),
            ('Linear Function', 'What is a linear function?', 'Function with constant rate of change'),
            ('Quadratic Function', 'What is a quadratic function?', 'Function with x² term'),
            ('Polynomial', 'What is a polynomial?', 'Expression with multiple terms'),
            ('Factoring', 'What is factoring?', 'Breaking expression into product of factors'),
            ('Completing the Square', 'What is completing the square?', 'Method to solve quadratic equations'),
            ('Quadratic Formula', 'What is the quadratic formula?', 'x = (-b ± √(b²-4ac))/2a')
        ]
        
        # Geometry
        geometry = [
            ('Point', 'What is a point?', 'Location in space with no dimensions'),
            ('Line', 'What is a line?', 'Straight path extending infinitely in both directions'),
            ('Plane', 'What is a plane?', 'Flat surface extending infinitely in all directions'),
            ('Angle', 'What is an angle?', 'Figure formed by two rays sharing endpoint'),
            ('Triangle', 'What is a triangle?', 'Polygon with three sides'),
            ('Circle', 'What is a circle?', 'Set of points equidistant from center'),
            ('Area', 'What is area?', 'Measure of surface covered'),
            ('Perimeter', 'What is perimeter?', 'Distance around figure'),
            ('Volume', 'What is volume?', 'Amount of space occupied'),
            ('Pythagorean Theorem', 'What is the Pythagorean theorem?', 'a² + b² = c²')
        ]
        
        # Calculus
        calculus = [
            ('Limit', 'What is a limit?', 'Value function approaches as input approaches specific value'),
            ('Derivative', 'What is a derivative?', 'Rate of change of function'),
            ('Integral', 'What is an integral?', 'Area under curve or antiderivative'),
            ('Chain Rule', 'What is the chain rule?', 'd/dx[f(g(x))] = f\'(g(x))g\'(x)'),
            ('Product Rule', 'What is the product rule?', 'd/dx[uv] = u\'v + uv\''),
            ('Quotient Rule', 'What is the quotient rule?', 'd/dx[u/v] = (u\'v - uv\')/v²'),
            ('Power Rule', 'What is the power rule?', 'd/dx[x^n] = nx^(n-1)'),
            ('Fundamental Theorem', 'What is the fundamental theorem of calculus?', 'Integration and differentiation are inverse operations'),
            ('Critical Point', 'What is a critical point?', 'Point where derivative is zero or undefined'),
            ('Inflection Point', 'What is an inflection point?', 'Point where concavity changes')
        ]
        
        # Add all mathematics cards
        for category in [algebra, geometry, calculus]:
            for item in category:
                mathematics_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'mathematics',
                    'difficulty': 'medium'
                })
        
        self.decks.append(mathematics_deck)
        print(f"Created Mathematics deck with {len(mathematics_deck['cards'])} cards")
    
    def create_biology_deck(self):
        """Create comprehensive Biology deck"""
        print("Creating Biology deck...")
        
        biology_deck = {
            'name': 'Biology Master',
            'category': 'Biology',
            'cards': []
        }
        
        # Cell Biology
        cell_biology = [
            ('Cell', 'What is a cell?', 'Basic unit of life'),
            ('Cell Membrane', 'What is the cell membrane?', 'Outer boundary of cell'),
            ('Nucleus', 'What is the nucleus?', 'Control center of cell'),
            ('Mitochondria', 'What are mitochondria?', 'Powerhouse of cell'),
            ('Ribosomes', 'What are ribosomes?', 'Site of protein synthesis'),
            ('Endoplasmic Reticulum', 'What is the ER?', 'Network of membranes for transport'),
            ('Golgi Apparatus', 'What is the Golgi apparatus?', 'Packaging and shipping center'),
            ('Lysosomes', 'What are lysosomes?', 'Digestive organelles'),
            ('Vacuoles', 'What are vacuoles?', 'Storage organelles'),
            ('Chloroplasts', 'What are chloroplasts?', 'Site of photosynthesis in plants')
        ]
        
        # Genetics
        genetics = [
            ('Gene', 'What is a gene?', 'Unit of heredity'),
            ('DNA', 'What is DNA?', 'Genetic material'),
            ('Chromosome', 'What is a chromosome?', 'Thread-like structure of DNA'),
            ('Allele', 'What is an allele?', 'Alternative form of gene'),
            ('Dominant', 'What is a dominant allele?', 'Allele that masks recessive'),
            ('Recessive', 'What is a recessive allele?', 'Allele masked by dominant'),
            ('Genotype', 'What is genotype?', 'Genetic makeup of organism'),
            ('Phenotype', 'What is phenotype?', 'Physical appearance'),
            ('Homozygous', 'What is homozygous?', 'Having identical alleles'),
            ('Heterozygous', 'What is heterozygous?', 'Having different alleles')
        ]
        
        # Evolution
        evolution = [
            ('Natural Selection', 'What is natural selection?', 'Survival of fittest'),
            ('Adaptation', 'What is adaptation?', 'Trait that increases survival'),
            ('Mutation', 'What is mutation?', 'Change in DNA sequence'),
            ('Speciation', 'What is speciation?', 'Formation of new species'),
            ('Fossil', 'What is a fossil?', 'Preserved remains of organism'),
            ('Extinction', 'What is extinction?', 'Complete disappearance of species'),
            ('Common Ancestor', 'What is a common ancestor?', 'Species from which others evolved'),
            ('Convergent Evolution', 'What is convergent evolution?', 'Similar traits in unrelated species'),
            ('Divergent Evolution', 'What is divergent evolution?', 'Different traits in related species'),
            ('Coevolution', 'What is coevolution?', 'Two species evolving together')
        ]
        
        # Add all biology cards
        for category in [cell_biology, genetics, evolution]:
            for item in category:
                biology_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'biology',
                    'difficulty': 'medium'
                })
        
        self.decks.append(biology_deck)
        print(f"Created Biology deck with {len(biology_deck['cards'])} cards")
    
    def create_computer_science_deck(self):
        """Create comprehensive Computer Science deck"""
        print("Creating Computer Science deck...")
        
        cs_deck = {
            'name': 'Computer Science Master',
            'category': 'Computer Science',
            'cards': []
        }
        
        # Programming
        programming = [
            ('Algorithm', 'What is an algorithm?', 'Step-by-step problem-solving procedure'),
            ('Variable', 'What is a variable?', 'Container for storing data'),
            ('Function', 'What is a function?', 'Reusable block of code'),
            ('Loop', 'What is a loop?', 'Code that repeats until condition is met'),
            ('Conditional', 'What is a conditional?', 'Code that executes based on condition'),
            ('Array', 'What is an array?', 'Ordered collection of elements'),
            ('Object', 'What is an object?', 'Instance of class with properties and methods'),
            ('Class', 'What is a class?', 'Blueprint for creating objects'),
            ('Inheritance', 'What is inheritance?', 'Class inheriting properties from another'),
            ('Polymorphism', 'What is polymorphism?', 'Same interface, different implementations')
        ]
        
        # Data Structures
        data_structures = [
            ('Stack', 'What is a stack?', 'Last-in-first-out data structure'),
            ('Queue', 'What is a queue?', 'First-in-first-out data structure'),
            ('Linked List', 'What is a linked list?', 'Data structure with nodes pointing to next'),
            ('Tree', 'What is a tree?', 'Hierarchical data structure'),
            ('Graph', 'What is a graph?', 'Data structure with nodes and edges'),
            ('Hash Table', 'What is a hash table?', 'Data structure for key-value pairs'),
            ('Binary Search Tree', 'What is a BST?', 'Tree where left child < parent < right child'),
            ('Heap', 'What is a heap?', 'Tree-based data structure with heap property'),
            ('Set', 'What is a set?', 'Collection of unique elements'),
            ('Map', 'What is a map?', 'Collection of key-value pairs')
        ]
        
        # Computer Systems
        computer_systems = [
            ('CPU', 'What is a CPU?', 'Central processing unit'),
            ('RAM', 'What is RAM?', 'Random access memory'),
            ('Operating System', 'What is an OS?', 'Software managing hardware and software'),
            ('Compiler', 'What is a compiler?', 'Program that translates source code to machine code'),
            ('Interpreter', 'What is an interpreter?', 'Program that executes source code directly'),
            ('Database', 'What is a database?', 'Organized collection of data'),
            ('Network', 'What is a network?', 'Connected computers sharing resources'),
            ('Protocol', 'What is a protocol?', 'Set of rules for communication'),
            ('Encryption', 'What is encryption?', 'Converting data to unreadable format'),
            ('Firewall', 'What is a firewall?', 'Security system controlling network traffic')
        ]
        
        # Add all computer science cards
        for category in [programming, data_structures, computer_systems]:
            for item in category:
                cs_deck['cards'].append({
                    'front': item[0],
                    'question': item[1],
                    'back': item[2],
                    'type': 'computer_science',
                    'difficulty': 'medium'
                })
        
        self.decks.append(cs_deck)
        print(f"Created Computer Science deck with {len(cs_deck['cards'])} cards")
    
    def consolidate_decks(self):
        """Consolidate all complex subject decks"""
        print("Consolidating all Complex Subject decks...")
        
        all_cards = []
        total_cards = 0
        
        for deck in self.decks:
            all_cards.extend(deck['cards'])
            total_cards += len(deck['cards'])
            print(f"Added {len(deck['cards'])} cards from {deck['name']}")
        
        consolidated_deck = {
            'name': 'Comprehensive Complex Subjects Master Deck',
            'total_cards': total_cards,
            'categories': [deck['category'] for deck in self.decks],
            'cards': all_cards,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return consolidated_deck
    
    def create_training_test_split(self, consolidated_deck):
        """Create 80/20 training/testing split"""
        print("Creating 80/20 training/testing split...")
        
        total_cards = len(consolidated_deck['cards'])
        training_size = int(total_cards * 0.8)
        testing_size = total_cards - training_size
        
        # Shuffle cards
        import random
        random.shuffle(consolidated_deck['cards'])
        
        training_deck = {
            'name': 'Complex Subjects Training Deck (80%)',
            'total_cards': training_size,
            'cards': consolidated_deck['cards'][:training_size],
            'split': 'training'
        }
        
        testing_deck = {
            'name': 'Complex Subjects Testing Deck (20%)',
            'total_cards': testing_size,
            'cards': consolidated_deck['cards'][training_size:],
            'split': 'testing'
        }
        
        return training_deck, testing_deck
    
    def save_decks(self, consolidated_deck, training_deck, testing_deck):
        """Save all decks to JSON files"""
        print("Saving Complex Subjects decks to JSON files...")
        
        # Create output directory
        os.makedirs('generated_flashcards', exist_ok=True)
        
        # Save consolidated deck
        with open('generated_flashcards/comprehensive_complex_subjects_deck.json', 'w', encoding='utf-8') as f:
            json.dump(consolidated_deck, f, indent=2, ensure_ascii=False)
        
        # Save training deck
        with open('generated_flashcards/complex_subjects_training_deck.json', 'w', encoding='utf-8') as f:
            json.dump(training_deck, f, indent=2, ensure_ascii=False)
        
        # Save testing deck
        with open('generated_flashcards/complex_subjects_testing_deck.json', 'w', encoding='utf-8') as f:
            json.dump(testing_deck, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {consolidated_deck['total_cards']} total Complex Subjects cards")
        print(f"✅ Training deck: {training_deck['total_cards']} cards")
        print(f"✅ Testing deck: {testing_deck['total_cards']} cards")
    
    def run(self):
        """Main execution method"""
        print("🚀 Starting Complex Subjects Deck Creation Process...")
        
        # Create all complex subject decks
        self.create_physics_deck()
        self.create_chemistry_deck()
        self.create_mathematics_deck()
        self.create_biology_deck()
        self.create_computer_science_deck()
        
        print(f"Created {len(self.decks)} Complex Subject decks")
        
        # Consolidate all decks
        consolidated_deck = self.consolidate_decks()
        
        # Create training/testing split
        training_deck, testing_deck = self.create_training_test_split(consolidated_deck)
        
        # Save all decks
        self.save_decks(consolidated_deck, training_deck, testing_deck)
        
        print("🎉 Complex Subjects Deck Creation Complete!")
        print(f"📊 Total Cards: {consolidated_deck['total_cards']}")
        print(f"📚 Training Set: {training_deck['total_cards']} cards (80%)")
        print(f"🧪 Testing Set: {testing_deck['total_cards']} cards (20%)")
        
        return consolidated_deck, training_deck, testing_deck

if __name__ == "__main__":
    creator = ComplexSubjectsDeckCreator()
    creator.run()
