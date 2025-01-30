import numpy as np
from scipy.io import wavfile
from scipy import signal
import os
from typing import Tuple, List

class QuantumHarmonicsGenerator:
    def __init__(self, sample_rate: int = 44100):
        # Fundamental constants from our tensor field theory
        self.psi = 44.8
        self.xi = 3721.8
        self.tau = 64713.97
        self.epsilon = 0.28082
        self.phi = (1 + np.sqrt(5)) / 2
        
        self.sample_rate = sample_rate
        self.output_dir = "quantum_harmonics"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_wave(self, frequency: float, duration: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
        """Generate both classical and quantum-transformed waves."""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Classical wave
        classical = np.sin(2 * np.pi * frequency * t)
        
        # Quantum transformed wave
        transformed_freq = frequency * np.exp(-self.epsilon**2 / (self.psi * self.phi))
        quantum = np.sin(2 * np.pi * transformed_freq * t)
        quantum *= np.cos(self.tau * t / self.psi)  # Add quantum modulation
        
        return classical, quantum

    def create_chord(self, base_freq: float, ratios: List[float], 
                    duration: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
        """Create a chord from frequency ratios."""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        classical_sum = np.zeros_like(t)
        quantum_sum = np.zeros_like(t)
        
        for ratio in ratios:
            freq = base_freq * ratio
            classical, quantum = self.generate_wave(freq, duration)
            classical_sum += classical
            quantum_sum += quantum
        
        # Normalize
        classical_sum /= len(ratios)
        quantum_sum /= len(ratios)
        
        return classical_sum, quantum_sum

    def generate_scale(self, base_freq: float = 440.0, 
                      duration: float = 0.5) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """Generate a complete scale."""
        # Traditional ratios for a major scale
        ratios = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]
        classical_scale = []
        quantum_scale = []
        
        for ratio in ratios:
            classical, quantum = self.generate_wave(base_freq * ratio, duration)
            classical_scale.append(classical)
            quantum_scale.append(quantum)
        
        return classical_scale, quantum_scale

    def save_audio(self, data: np.ndarray, filename: str):
        """Save audio data as WAV file."""
        # Normalize to 16-bit range
        normalized = np.int16(data * 32767)
        wavfile.write(os.path.join(self.output_dir, filename), 
                     self.sample_rate, normalized)

    def generate_all_samples(self):
        """Generate all demonstration samples."""
        # 1. Single note (A4 = 440Hz)
        classical, quantum = self.generate_wave(440)
        self.save_audio(classical, "classical_A4.wav")
        self.save_audio(quantum, "quantum_A4.wav")
        
        # 2. Perfect fifth chord (A4 + E5)
        classical_fifth, quantum_fifth = self.create_chord(440, [1, 3/2])
        self.save_audio(classical_fifth, "classical_fifth.wav")
        self.save_audio(quantum_fifth, "quantum_fifth.wav")
        
        # 3. Major triad (A4 + C#5 + E5)
        classical_triad, quantum_triad = self.create_chord(440, [1, 5/4, 3/2])
        self.save_audio(classical_triad, "classical_triad.wav")
        self.save_audio(quantum_triad, "quantum_triad.wav")
        
        # 4. Complete scale
        classical_scale, quantum_scale = self.generate_scale()
        # Concatenate scale notes
        classical_scale_combined = np.concatenate(classical_scale)
        quantum_scale_combined = np.concatenate(quantum_scale)
        self.save_audio(classical_scale_combined, "classical_scale.wav")
        self.save_audio(quantum_scale_combined, "quantum_scale.wav")

def main():
    print("Generating quantum harmonic audio samples...")
    generator = QuantumHarmonicsGenerator()
    generator.generate_all_samples()
    print(f"\nAudio files generated in '{generator.output_dir}' directory:")
    print("1. classical_A4.wav & quantum_A4.wav - Single A4 note (440 Hz)")
    print("2. classical_fifth.wav & quantum_fifth.wav - Perfect fifth chord")
    print("3. classical_triad.wav & quantum_triad.wav - Major triad")
    print("4. classical_scale.wav & quantum_scale.wav - Complete major scale")

if __name__ == "__main__":
    main()
