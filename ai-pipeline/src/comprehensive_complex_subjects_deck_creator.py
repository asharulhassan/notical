import json
import os
from datetime import datetime

class ComprehensiveComplexSubjectsDeckCreator:
    def __init__(self):
        self.output_dir = "comprehensive_complex_subjects_deck"
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_physics_section(self):
        """Create comprehensive physics section"""
        print("🔬 Creating Physics section...")
        
        physics_concepts = {
            # Mechanics
            "Force": "A push or pull that can change an object's motion. Measured in Newtons (N). Example: Gravity pulling objects toward Earth.",
            "Mass": "The amount of matter in an object. Measured in kilograms (kg). Mass is constant regardless of location.",
            "Weight": "The force of gravity acting on an object's mass. Weight = mass × gravitational acceleration (W = mg).",
            "Acceleration": "The rate of change of velocity with time. Measured in meters per second squared (m/s²).",
            "Momentum": "The product of an object's mass and velocity (p = mv). Momentum is conserved in closed systems.",
            "Energy": "The ability to do work. Types include kinetic (motion), potential (position), and thermal (heat) energy.",
            "Power": "The rate at which work is done or energy is transferred. Measured in Watts (W). Power = Work/Time.",
            "Work": "Force applied over a distance. Work = Force × Distance × cos(θ). Measured in Joules (J).",
            "Efficiency": "The ratio of useful work output to total energy input. Efficiency = (Useful Output/Total Input) × 100%.",
            "Conservation of Energy": "Energy cannot be created or destroyed, only transformed from one form to another.",
            
            # Thermodynamics
            "Temperature": "A measure of the average kinetic energy of particles in a substance. Measured in Kelvin (K) or Celsius (°C).",
            "Heat": "Energy transferred between objects due to temperature difference. Heat flows from hot to cold objects.",
            "Internal Energy": "The total energy of all particles in a system, including kinetic and potential energy.",
            "Entropy": "A measure of disorder or randomness in a system. Entropy always increases in isolated systems.",
            "First Law of Thermodynamics": "Energy cannot be created or destroyed. The change in internal energy equals heat added minus work done.",
            "Second Law of Thermodynamics": "Heat cannot spontaneously flow from a colder body to a hotter body. Entropy increases over time.",
            
            # Waves
            "Wave": "A disturbance that transfers energy through a medium or space without transferring matter.",
            "Amplitude": "The maximum displacement of a wave from its equilibrium position. Determines wave intensity.",
            "Wavelength": "The distance between two consecutive points in phase on a wave (e.g., crest to crest).",
            "Frequency": "The number of complete wave cycles per second. Measured in Hertz (Hz).",
            "Wave Speed": "The speed at which a wave travels through a medium. Wave Speed = Frequency × Wavelength.",
            "Interference": "The interaction of two or more waves. Constructive interference increases amplitude; destructive decreases it.",
            
            # Electricity
            "Electric Charge": "A fundamental property of matter. Like charges repel; opposite charges attract. Measured in Coulombs (C).",
            "Electric Field": "A region around a charged object where other charges experience electric force. Field lines show direction.",
            "Current": "The rate of flow of electric charge. Current = Charge/Time. Measured in Amperes (A).",
            "Voltage": "The difference in electric potential between two points. Voltage = Work/Charge. Measured in Volts (V).",
            "Resistance": "The opposition to electric current flow. Resistance = Voltage/Current. Measured in Ohms (Ω).",
            "Ohm's Law": "The relationship between voltage, current, and resistance: V = IR (Voltage = Current × Resistance).",
            
            # Modern Physics
            "Photoelectric Effect": "The emission of electrons from a metal surface when light shines on it. Supports particle nature of light.",
            "Wave-Particle Duality": "The concept that light and matter exhibit both wave-like and particle-like properties.",
            "Quantum Mechanics": "The branch of physics that describes the behavior of matter and energy at atomic and subatomic scales.",
            "Relativity": "Einstein's theory that space and time are interconnected, and that the speed of light is constant for all observers.",
            "Nuclear Fission": "The splitting of a heavy nucleus into smaller nuclei, releasing energy. Used in nuclear power plants.",
            "Nuclear Fusion": "The combining of light nuclei to form heavier nuclei, releasing energy. Powers the Sun and stars."
        }
        
        cards = []
        for concept, explanation in physics_concepts.items():
            card = {
                "front": f"Define and explain: {concept}",
                "back": explanation,
                "type": "physics",
                "category": "physics",
                "difficulty": "advanced",
                "tags": ["physics", "science", "complex"]
            }
            cards.append(card)
        
        return cards
    
    def create_chemistry_section(self):
        """Create comprehensive chemistry section"""
        print("🧪 Creating Chemistry section...")
        
        chemistry_concepts = {
            # Atomic Structure
            "Atom": "The smallest unit of an element that retains the properties of that element. Consists of protons, neutrons, and electrons.",
            "Proton": "Positively charged subatomic particle found in the nucleus. Determines the element's identity.",
            "Neutron": "Neutrally charged subatomic particle found in the nucleus. Contributes to atomic mass.",
            "Electron": "Negatively charged subatomic particle that orbits the nucleus. Participates in chemical bonding.",
            "Atomic Number": "The number of protons in an atom's nucleus. Determines the element's identity.",
            "Atomic Mass": "The total mass of an atom, including protons, neutrons, and electrons.",
            "Isotope": "Atoms of the same element with different numbers of neutrons, resulting in different atomic masses.",
            
            # Chemical Bonding
            "Ionic Bond": "Chemical bond formed by the transfer of electrons from one atom to another, creating oppositely charged ions.",
            "Covalent Bond": "Chemical bond formed by the sharing of electrons between atoms.",
            "Metallic Bond": "Chemical bond formed by the attraction between metal cations and delocalized electrons.",
            "Polar Bond": "Covalent bond where electrons are shared unequally, creating partial positive and negative charges.",
            "Nonpolar Bond": "Covalent bond where electrons are shared equally between atoms.",
            "Hydrogen Bond": "Weak attraction between a hydrogen atom and an electronegative atom (usually oxygen, nitrogen, or fluorine).",
            
            # Chemical Reactions
            "Chemical Reaction": "Process where substances are transformed into new substances with different properties.",
            "Reactant": "Substance that participates in a chemical reaction and is consumed.",
            "Product": "Substance that is formed as a result of a chemical reaction.",
            "Catalyst": "Substance that increases the rate of a chemical reaction without being consumed.",
            "Enzyme": "Biological catalyst that speeds up biochemical reactions in living organisms.",
            "Activation Energy": "Minimum energy required for a chemical reaction to occur.",
            
            # States of Matter
            "Solid": "State of matter with definite shape and volume. Particles are closely packed and vibrate in fixed positions.",
            "Liquid": "State of matter with definite volume but no definite shape. Particles are close but can move past each other.",
            "Gas": "State of matter with no definite shape or volume. Particles are far apart and move freely.",
            "Plasma": "State of matter where atoms are ionized and electrons are free. Found in stars and lightning.",
            "Phase Change": "Transition between different states of matter (solid, liquid, gas) due to temperature or pressure changes.",
            "Melting Point": "Temperature at which a solid changes to a liquid.",
            "Boiling Point": "Temperature at which a liquid changes to a gas."
        }
        
        cards = []
        for concept, explanation in chemistry_concepts.items():
            card = {
                "front": f"Explain the chemical concept: {concept}",
                "back": explanation,
                "type": "chemistry",
                "category": "chemistry",
                "difficulty": "advanced",
                "tags": ["chemistry", "science", "complex"]
            }
            cards.append(card)
        
        return cards
    
    def create_mathematics_section(self):
        """Create comprehensive mathematics section"""
        print("📐 Creating Mathematics section...")
        
        mathematics_concepts = {
            # Algebra
            "Variable": "A symbol (usually a letter) that represents an unknown value or a value that can change.",
            "Equation": "A mathematical statement that two expressions are equal, containing an equals sign (=).",
            "Inequality": "A mathematical statement that two expressions are not equal, using symbols like <, >, ≤, ≥, ≠.",
            "Function": "A relationship between two sets where each input has exactly one output. Often written as f(x).",
            "Polynomial": "An expression with multiple terms, each containing variables raised to whole number powers.",
            "Quadratic Equation": "A polynomial equation of degree 2, in the form ax² + bx + c = 0.",
            "Factoring": "The process of breaking down a polynomial into a product of simpler polynomials.",
            
            # Geometry
            "Point": "A location in space with no size or dimension. Represented by a dot.",
            "Line": "A straight path that extends infinitely in both directions. Has length but no width.",
            "Plane": "A flat surface that extends infinitely in all directions. Has length and width but no height.",
            "Angle": "The figure formed by two rays sharing a common endpoint. Measured in degrees or radians.",
            "Triangle": "A polygon with three sides and three angles. Sum of angles equals 180°.",
            "Circle": "A set of points equidistant from a center point. Defined by radius and circumference.",
            "Pythagorean Theorem": "In a right triangle, a² + b² = c², where c is the hypotenuse.",
            
            # Calculus
            "Derivative": "The rate of change of a function with respect to its variable. Represents slope of tangent line.",
            "Integral": "The area under a curve or the accumulation of a quantity over an interval.",
            "Limit": "The value that a function approaches as the input approaches a certain value.",
            "Continuity": "A function is continuous if there are no breaks, jumps, or holes in its graph.",
            "Differentiation": "The process of finding the derivative of a function.",
            "Integration": "The process of finding the integral of a function.",
            
            # Statistics
            "Mean": "The average of a set of numbers, calculated by summing all values and dividing by the count.",
            "Median": "The middle value in a set of numbers when arranged in order.",
            "Mode": "The value that appears most frequently in a set of numbers.",
            "Standard Deviation": "A measure of how spread out numbers are from the mean.",
            "Probability": "The likelihood of an event occurring, expressed as a number between 0 and 1.",
            "Correlation": "A measure of the strength and direction of the relationship between two variables."
        }
        
        cards = []
        for concept, explanation in mathematics_concepts.items():
            card = {
                "front": f"Define the mathematical concept: {concept}",
                "back": explanation,
                "type": "mathematics",
                "category": "mathematics",
                "difficulty": "advanced",
                "tags": ["mathematics", "math", "complex"]
            }
            cards.append(card)
        
        return cards
    
    def create_biology_section(self):
        """Create comprehensive biology section"""
        print("🧬 Creating Biology section...")
        
        biology_concepts = {
            # Cell Biology
            "Cell": "The basic unit of life. All living organisms are composed of one or more cells.",
            "Nucleus": "The control center of the cell, containing DNA and regulating cell activities.",
            "Mitochondria": "Organelles that produce energy through cellular respiration. Known as the 'powerhouse of the cell.'",
            "Chloroplast": "Organelles in plant cells that carry out photosynthesis, converting sunlight into chemical energy.",
            "Cell Membrane": "The outer boundary of the cell that controls what enters and exits.",
            "Cytoplasm": "The gel-like substance inside the cell where organelles are suspended.",
            
            # Genetics
            "DNA": "Deoxyribonucleic acid, the molecule that carries genetic information in all living organisms.",
            "Gene": "A segment of DNA that codes for a specific protein or trait.",
            "Chromosome": "A structure made of DNA and proteins that carries genetic information.",
            "Mutation": "A change in the DNA sequence that can result in different traits or genetic disorders.",
            "Heredity": "The passing of traits from parents to offspring through genes.",
            "Natural Selection": "The process where organisms with favorable traits are more likely to survive and reproduce.",
            
            # Evolution
            "Evolution": "The process of change in living organisms over time, resulting in new species.",
            "Adaptation": "A trait that helps an organism survive and reproduce in its environment.",
            "Speciation": "The formation of new species from existing ones through evolutionary processes.",
            "Fossil": "The preserved remains or traces of ancient organisms, providing evidence of evolution.",
            "Common Ancestor": "An organism from which two or more species evolved.",
            "Extinction": "The complete disappearance of a species from Earth.",
            
            # Ecology
            "Ecosystem": "A community of living organisms interacting with their physical environment.",
            "Food Chain": "A linear sequence showing how energy and nutrients flow from one organism to another.",
            "Food Web": "A complex network of interconnected food chains in an ecosystem.",
            "Biodiversity": "The variety of life in an ecosystem, including different species and genetic diversity.",
            "Habitat": "The natural environment where an organism lives and grows.",
            "Niche": "The role and position of an organism in its ecosystem, including its habitat and behavior."
        }
        
        cards = []
        for concept, explanation in biology_concepts.items():
            card = {
                "front": f"Explain the biological concept: {concept}",
                "back": explanation,
                "type": "biology",
                "category": "biology",
                "difficulty": "advanced",
                "tags": ["biology", "science", "complex"]
            }
            cards.append(card)
        
        return cards
    
    def create_computer_science_section(self):
        """Create comprehensive computer science section"""
        print("💻 Creating Computer Science section...")
        
        cs_concepts = {
            # Programming
            "Algorithm": "A step-by-step procedure for solving a problem or accomplishing a task.",
            "Variable": "A named storage location in computer memory that can hold data.",
            "Function": "A reusable block of code that performs a specific task.",
            "Loop": "A control structure that repeats a block of code multiple times.",
            "Conditional": "A control structure that executes different code based on whether a condition is true or false.",
            "Recursion": "A programming technique where a function calls itself to solve a problem.",
            
            # Data Structures
            "Array": "A collection of elements stored at contiguous memory locations, accessible by index.",
            "Linked List": "A data structure where elements are stored in nodes, each pointing to the next node.",
            "Stack": "A data structure that follows Last-In-First-Out (LIFO) principle.",
            "Queue": "A data structure that follows First-In-First-Out (FIFO) principle.",
            "Tree": "A hierarchical data structure with nodes connected by edges, having one root node.",
            "Graph": "A data structure consisting of vertices (nodes) connected by edges.",
            
            # Computer Architecture
            "CPU": "Central Processing Unit, the brain of the computer that executes instructions.",
            "RAM": "Random Access Memory, temporary storage that the CPU uses for active programs and data.",
            "Hard Drive": "Permanent storage device that stores the operating system, programs, and files.",
            "Binary": "A number system using only 0 and 1, the foundation of all computer operations.",
            "Operating System": "Software that manages computer hardware and provides services for computer programs.",
            "Compiler": "A program that translates source code written in a programming language into machine code."
        }
        
        cards = []
        for concept, explanation in cs_concepts.items():
            card = {
                "front": f"Define the computer science concept: {concept}",
                "back": explanation,
                "type": "computer_science",
                "category": "computer_science",
                "difficulty": "advanced",
                "tags": ["computer_science", "programming", "complex"]
            }
            cards.append(card)
        
        return cards
    
    def create_comprehensive_complex_subjects_deck(self):
        """Create one massive comprehensive complex subjects deck"""
        print("🚀 Creating ONE comprehensive complex subjects deck with ALL content...")
        
        # Generate all sections
        physics_cards = self.create_physics_section()
        chemistry_cards = self.create_chemistry_section()
        mathematics_cards = self.create_mathematics_section()
        biology_cards = self.create_biology_section()
        cs_cards = self.create_computer_science_section()
        
        # Combine all cards
        all_cards = physics_cards + chemistry_cards + mathematics_cards + biology_cards + cs_cards
        
        # Create comprehensive deck
        comprehensive_deck = {
            "deck_info": {
                "name": "Comprehensive Complex Subjects Master Deck",
                "description": "Complete complex subjects deck covering Physics, Chemistry, Mathematics, Biology, and Computer Science",
                "total_cards": len(all_cards),
                "created_date": datetime.now().isoformat(),
                "version": "1.0"
            },
            "sections": {
                "physics": {
                    "name": "Physics",
                    "cards": physics_cards,
                    "total_cards": len(physics_cards),
                    "description": "Physical laws, mechanics, thermodynamics, waves, electricity, and modern physics"
                },
                "chemistry": {
                    "name": "Chemistry",
                    "cards": chemistry_cards,
                    "total_cards": len(chemistry_cards),
                    "description": "Atomic structure, chemical bonding, reactions, and states of matter"
                },
                "mathematics": {
                    "name": "Mathematics",
                    "cards": mathematics_cards,
                    "total_cards": len(mathematics_cards),
                    "description": "Algebra, geometry, calculus, and statistics"
                },
                "biology": {
                    "name": "Biology",
                    "cards": biology_cards,
                    "total_cards": len(biology_cards),
                    "description": "Cell biology, genetics, evolution, and ecology"
                },
                "computer_science": {
                    "name": "Computer Science",
                    "cards": cs_cards,
                    "total_cards": len(cs_cards),
                    "description": "Programming, data structures, and computer architecture"
                }
            },
            "all_cards": all_cards,
            "statistics": {
                "total_cards": len(all_cards),
                "physics_cards": len(physics_cards),
                "chemistry_cards": len(chemistry_cards),
                "mathematics_cards": len(mathematics_cards),
                "biology_cards": len(biology_cards),
                "computer_science_cards": len(cs_cards)
            }
        }
        
        # Save comprehensive deck
        filename = "comprehensive_complex_subjects_master_deck.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_deck, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Comprehensive complex subjects deck created!")
        print(f"📊 Total cards: {len(all_cards)}")
        print(f"📁 Saved to: {filepath}")
        print(f"🎯 All three comprehensive decks are now complete!")
        
        return comprehensive_deck

def main():
    creator = ComprehensiveComplexSubjectsDeckCreator()
    comprehensive_deck = creator.create_comprehensive_complex_subjects_deck()
    
    print(f"\n🎉 COMPREHENSIVE COMPLEX SUBJECTS DECK COMPLETE!")
    print("🚀 We now have ALL THREE massive comprehensive decks!")
    print("🎯 Mission accomplished: English → Humanities → Complex Subjects!")

if __name__ == "__main__":
    main()
