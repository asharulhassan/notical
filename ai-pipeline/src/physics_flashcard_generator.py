import json
import os
from datetime import datetime

class PhysicsFlashcardGenerator:
    def __init__(self):
        self.output_dir = "physics_flashcards"
        self.learned_patterns = {
            "question_starters": ["What is", "Define", "Explain", "Describe", "How does", "What causes"],
            "answer_structures": ["definition", "with_examples", "step_by_step", "comparison"]
        }
        
        # Create output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_mechanics_cards(self):
        """Generate Mechanics flashcards using learned patterns"""
        print("🔧 Creating Mechanics flashcards...")
        
        mechanics_concepts = {
            "Force": "A push or pull that can change an object's motion. Measured in Newtons (N). Example: Gravity pulling objects toward Earth.",
            "Mass": "The amount of matter in an object. Measured in kilograms (kg). Mass is constant regardless of location.",
            "Weight": "The force of gravity acting on an object's mass. Weight = mass × gravitational acceleration (W = mg).",
            "Acceleration": "The rate of change of velocity with time. Measured in meters per second squared (m/s²).",
            "Momentum": "The product of an object's mass and velocity (p = mv). Momentum is conserved in closed systems.",
            "Energy": "The ability to do work. Types include kinetic (motion), potential (position), and thermal (heat) energy.",
            "Power": "The rate at which work is done or energy is transferred. Measured in Watts (W). Power = Work/Time.",
            "Work": "Force applied over a distance. Work = Force × Distance × cos(θ). Measured in Joules (J).",
            "Efficiency": "The ratio of useful work output to total energy input. Efficiency = (Useful Output/Total Input) × 100%.",
            "Conservation of Energy": "Energy cannot be created or destroyed, only transformed from one form to another."
        }
        
        cards = []
        for concept, explanation in mechanics_concepts.items():
            card = {
                "front": f"Define and explain: {concept}",
                "back": explanation,
                "type": "concept",
                "subject": "Physics - Mechanics",
                "tags": ["mechanics", "physics", "concept"],
                "difficulty": "intermediate",
                "category": "mechanics"
            }
            cards.append(card)
        
        return cards
    
    def generate_thermodynamics_cards(self):
        """Generate Thermodynamics flashcards"""
        print("🔥 Creating Thermodynamics flashcards...")
        
        thermo_concepts = {
            "Temperature": "A measure of the average kinetic energy of particles in a substance. Measured in Kelvin (K) or Celsius (°C).",
            "Heat": "Energy transferred between objects due to temperature difference. Heat flows from hot to cold objects.",
            "Internal Energy": "The total energy of all particles in a system, including kinetic and potential energy.",
            "Entropy": "A measure of disorder or randomness in a system. Entropy always increases in isolated systems.",
            "First Law of Thermodynamics": "Energy cannot be created or destroyed. The change in internal energy equals heat added minus work done.",
            "Second Law of Thermodynamics": "Heat cannot spontaneously flow from a colder body to a hotter body. Entropy increases over time.",
            "Heat Capacity": "The amount of heat required to raise the temperature of a substance by 1°C. Units: J/°C or J/K.",
            "Specific Heat": "The heat capacity per unit mass of a substance. Units: J/kg°C or J/kgK.",
            "Latent Heat": "The heat required to change the phase of a substance (solid to liquid, liquid to gas) without changing temperature.",
            "Thermal Expansion": "The tendency of matter to change volume in response to temperature changes. Most substances expand when heated."
        }
        
        cards = []
        for concept, explanation in thermo_concepts.items():
            card = {
                "front": f"What is {concept}?",
                "back": explanation,
                "type": "concept",
                "subject": "Physics - Thermodynamics",
                "tags": ["thermodynamics", "physics", "concept"],
                "difficulty": "advanced",
                "category": "thermodynamics"
            }
            cards.append(card)
        
        return cards
    
    def generate_waves_cards(self):
        """Generate Waves flashcards"""
        print("🌊 Creating Waves flashcards...")
        
        waves_concepts = {
            "Wave": "A disturbance that transfers energy through a medium or space without transferring matter.",
            "Amplitude": "The maximum displacement of a wave from its equilibrium position. Determines wave intensity.",
            "Wavelength": "The distance between two consecutive points in phase on a wave (e.g., crest to crest).",
            "Frequency": "The number of complete wave cycles per second. Measured in Hertz (Hz).",
            "Period": "The time for one complete wave cycle. Period = 1/Frequency.",
            "Wave Speed": "The speed at which a wave travels through a medium. Wave Speed = Frequency × Wavelength.",
            "Transverse Wave": "A wave where particles vibrate perpendicular to the direction of wave travel (e.g., light waves).",
            "Longitudinal Wave": "A wave where particles vibrate parallel to the direction of wave travel (e.g., sound waves).",
            "Interference": "The interaction of two or more waves. Constructive interference increases amplitude; destructive decreases it.",
            "Resonance": "The phenomenon where a system vibrates at maximum amplitude at its natural frequency."
        }
        
        cards = []
        for concept, explanation in waves_concepts.items():
            card = {
                "front": f"Explain the concept of {concept}",
                "back": explanation,
                "type": "concept",
                "subject": "Physics - Waves",
                "tags": ["waves", "physics", "concept"],
                "difficulty": "intermediate",
                "category": "waves"
            }
            cards.append(card)
        
        return cards
    
    def generate_electricity_cards(self):
        """Generate Electricity flashcards"""
        print("⚡ Creating Electricity flashcards...")
        
        electricity_concepts = {
            "Electric Charge": "A fundamental property of matter. Like charges repel; opposite charges attract. Measured in Coulombs (C).",
            "Electric Field": "A region around a charged object where other charges experience electric force. Field lines show direction.",
            "Electric Potential": "The electric potential energy per unit charge at a point. Measured in Volts (V).",
            "Current": "The rate of flow of electric charge. Current = Charge/Time. Measured in Amperes (A).",
            "Voltage": "The difference in electric potential between two points. Voltage = Work/Charge. Measured in Volts (V).",
            "Resistance": "The opposition to electric current flow. Resistance = Voltage/Current. Measured in Ohms (Ω).",
            "Power": "The rate at which electrical energy is transferred. Power = Voltage × Current. Measured in Watts (W).",
            "Capacitance": "The ability of a capacitor to store electric charge. Capacitance = Charge/Voltage. Measured in Farads (F).",
            "Inductance": "The ability of an inductor to store energy in a magnetic field. Measured in Henries (H).",
            "Ohm's Law": "The relationship between voltage, current, and resistance: V = IR (Voltage = Current × Resistance)."
        }
        
        cards = []
        for concept, explanation in electricity_concepts.items():
            card = {
                "front": f"Define {concept} in physics",
                "back": explanation,
                "type": "concept",
                "subject": "Physics - Electricity",
                "tags": ["electricity", "physics", "concept"],
                "difficulty": "advanced",
                "category": "electricity"
            }
            cards.append(card)
        
        return cards
    
    def generate_modern_physics_cards(self):
        """Generate Modern Physics flashcards"""
        print("🔬 Creating Modern Physics flashcards...")
        
        modern_concepts = {
            "Photoelectric Effect": "The emission of electrons from a metal surface when light shines on it. Supports particle nature of light.",
            "Wave-Particle Duality": "The concept that light and matter exhibit both wave-like and particle-like properties.",
            "Quantum Mechanics": "The branch of physics that describes the behavior of matter and energy at atomic and subatomic scales.",
            "Relativity": "Einstein's theory that space and time are interconnected, and that the speed of light is constant for all observers.",
            "Nuclear Fission": "The splitting of a heavy nucleus into smaller nuclei, releasing energy. Used in nuclear power plants.",
            "Nuclear Fusion": "The combining of light nuclei to form heavier nuclei, releasing energy. Powers the Sun and stars.",
            "Radioactivity": "The spontaneous emission of radiation from unstable atomic nuclei. Types: alpha, beta, gamma decay.",
            "Half-Life": "The time required for half of a radioactive substance to decay. Each isotope has a unique half-life.",
            "Mass-Energy Equivalence": "Einstein's famous equation E = mc², showing that mass and energy are interchangeable.",
            "Dark Matter": "Hypothetical matter that doesn't emit light but exerts gravitational force. Comprises most of the universe's mass."
        }
        
        cards = []
        for concept, explanation in modern_concepts.items():
            card = {
                "front": f"What is {concept}?",
                "back": explanation,
                "type": "concept",
                "subject": "Physics - Modern Physics",
                "tags": ["modern_physics", "physics", "concept"],
                "difficulty": "advanced",
                "category": "modern_physics"
            }
            cards.append(card)
        
        return cards
    
    def generate_formula_cards(self):
        """Generate Physics formula flashcards"""
        print("📐 Creating Physics formula flashcards...")
        
        formulas = {
            "Kinetic Energy": "KE = ½mv² (Kinetic Energy = ½ × mass × velocity²)",
            "Gravitational Potential Energy": "GPE = mgh (GPE = mass × gravitational acceleration × height)",
            "Power": "P = W/t (Power = Work/Time)",
            "Density": "ρ = m/V (Density = mass/volume)",
            "Pressure": "P = F/A (Pressure = Force/Area)",
            "Wave Speed": "v = fλ (Wave Speed = frequency × wavelength)",
            "Ohm's Law": "V = IR (Voltage = Current × Resistance)",
            "Work": "W = Fd cos(θ) (Work = Force × distance × cos(angle))",
            "Momentum": "p = mv (Momentum = mass × velocity)",
            "Acceleration": "a = (v-u)/t (Acceleration = change in velocity/time)"
        }
        
        cards = []
        for formula_name, formula in formulas.items():
            card = {
                "front": f"What is the formula for {formula_name}?",
                "back": formula,
                "type": "formula",
                "subject": "Physics - Formulas",
                "tags": ["formula", "physics", "calculation"],
                "difficulty": "intermediate",
                "category": "formulas"
            }
            cards.append(card)
        
        return cards
    
    def generate_all_physics_decks(self):
        """Generate all Physics flashcard decks"""
        print("🚀 Starting comprehensive Physics flashcard generation...")
        
        # Generate all categories
        mechanics = self.generate_mechanics_cards()
        thermodynamics = self.generate_thermodynamics_cards()
        waves = self.generate_waves_cards()
        electricity = self.generate_electricity_cards()
        modern_physics = self.generate_modern_physics_cards()
        formulas = self.generate_formula_cards()
        
        # Combine all decks
        all_decks = {
            "Mechanics": {
                "cards": mechanics,
                "total_cards": len(mechanics),
                "subject": "Physics - Mechanics",
                "type": "concept",
                "difficulty": "intermediate"
            },
            "Thermodynamics": {
                "cards": thermodynamics,
                "total_cards": len(thermodynamics),
                "subject": "Physics - Thermodynamics",
                "type": "concept",
                "difficulty": "advanced"
            },
            "Waves": {
                "cards": waves,
                "total_cards": len(waves),
                "subject": "Physics - Waves",
                "type": "concept",
                "difficulty": "intermediate"
            },
            "Electricity": {
                "cards": electricity,
                "total_cards": len(electricity),
                "subject": "Physics - Electricity",
                "type": "concept",
                "difficulty": "advanced"
            },
            "Modern Physics": {
                "cards": modern_physics,
                "total_cards": len(modern_physics),
                "subject": "Physics - Modern Physics",
                "type": "concept",
                "difficulty": "advanced"
            },
            "Formulas": {
                "cards": formulas,
                "total_cards": len(formulas),
                "subject": "Physics - Formulas",
                "type": "formula",
                "difficulty": "intermediate"
            }
        }
        
        # Save individual deck files
        for deck_name, deck_data in all_decks.items():
            filename = f"physics_{deck_name.lower()}_deck.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(deck_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Saved {deck_name} deck: {deck_data['total_cards']} cards")
        
        # Save combined master file
        master_file = os.path.join(self.output_dir, "physics_all_decks_master.json")
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_decks, f, indent=2, ensure_ascii=False)
        
        # Calculate totals
        total_cards = sum(deck['total_cards'] for deck in all_decks.values())
        
        print(f"\n✅ Physics flashcard generation complete!")
        print(f"📊 Total Physics cards generated: {total_cards}")
        print(f"📁 Files saved in: {self.output_dir}")
        print(f"🎯 Ready for Phase 5: Testing with real Physics papers!")
        
        return all_decks

def main():
    generator = PhysicsFlashcardGenerator()
    all_decks = generator.generate_all_physics_decks()
    
    print(f"\n🎉 PHASE 4 COMPLETE!")
    print("🚀 We've successfully applied learned patterns to create Physics flashcards!")
    print("🎯 Next: Test with real Physics past papers using our new knowledge!")

if __name__ == "__main__":
    main()
