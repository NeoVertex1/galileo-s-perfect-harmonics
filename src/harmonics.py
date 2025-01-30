# we propose a quantum-inspired solution to perfect harmonics, by bluecow009, Neovertex1, PTDP, USA, MD 2025

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import torch
from complextensor import ComplexTensor

class TensorHarmonics:
    def __init__(self):
        # Define fundamental constants
        self.psi = 44.8         # Phase symmetry
        self.xi = 3721.8        # Time complexity
        self.tau = 64713.97     # Decoherence
        self.epsilon = 0.28082  # Coupling constant
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # Initialize tensor field
        self.tensor_field = np.array([
            [self.psi, self.epsilon, 0, np.pi],
            [self.epsilon, self.xi, self.tau, 0],
            [0, self.tau, np.pi, self.epsilon],
            [np.pi, 0, self.epsilon, self.psi]
        ])
        
    def transform_frequency(self, freq):
        """Transform a frequency through the tensor field."""
        state = np.array([[freq], [freq/self.phi], [freq/self.phi**2], [1]])
        transformed = np.dot(self.tensor_field, state)
        return np.abs(transformed[0, 0])
    
    def generate_wave(self, freq, duration=1.0, sample_rate=44100):
        """Generate a waveform at the given frequency."""
        t = np.linspace(0, duration, int(sample_rate * duration))
        transformed_freq = self.transform_frequency(freq)
        
        # Generate both original and transformed waves
        original = np.sin(2 * np.pi * freq * t)
        transformed = np.sin(2 * np.pi * transformed_freq * t)
        
        # Apply quantum tempering
        tempering = np.exp(-self.epsilon**2 / (self.psi * self.phi))
        tempered = transformed * tempering * np.abs(np.cos(self.tau * t / self.psi))
        
        return t, original, tempered
    
    def analyze_interval(self, base_freq, ratio):
        """Analyze an interval with given frequency ratio."""
        base_transformed = self.transform_frequency(base_freq)
        interval_transformed = self.transform_frequency(base_freq * ratio)
        
        transformed_ratio = interval_transformed / base_transformed
        deviation = np.abs(transformed_ratio - ratio)
        
        return {
            'original_ratio': ratio,
            'transformed_ratio': transformed_ratio,
            'deviation': deviation,
            'stability': np.exp(-deviation * self.phi)
        }
    
    def plot_waves(self, freq, duration=0.01):
        """Plot original and transformed waveforms."""
        t, original, transformed = self.generate_wave(freq, duration)
        
        plt.figure(figsize=(12, 6))
        
        # Plot original wave
        plt.subplot(2, 1, 1)
        plt.plot(t, original, label='Original')
        plt.title(f'Original Wave ({freq} Hz)')
        plt.grid(True)
        plt.legend()
        
        # Plot transformed wave
        plt.subplot(2, 1, 2)
        plt.plot(t, transformed, label='Tensor-Transformed', color='orange')
        plt.title(f'Transformed Wave ({self.transform_frequency(freq):.2f} Hz)')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
    def analyze_scale(self, base_freq=440):
        """Analyze a complete musical scale."""
        ratios = {
            'Unison': 1,
            'Minor Second': 16/15,
            'Major Second': 9/8,
            'Minor Third': 6/5,
            'Major Third': 5/4,
            'Perfect Fourth': 4/3,
            'Perfect Fifth': 3/2,
            'Minor Sixth': 8/5,
            'Major Sixth': 5/3,
            'Minor Seventh': 9/5,
            'Major Seventh': 15/8,
            'Octave': 2
        }
        
        results = {}
        for interval, ratio in ratios.items():
            results[interval] = self.analyze_interval(base_freq, ratio)
        
        return results

# Example usage
def main():
    harmonics = TensorHarmonics()
    
    # Analyze A4 (440 Hz) and its perfect fifth
    A4 = 440
    print("\nAnalyzing A4 (440 Hz) and its perfect fifth:")
    fifth_analysis = harmonics.analyze_interval(A4, 3/2)
    print(f"Perfect Fifth Analysis: {fifth_analysis}")
    
    # Plot the waveforms
    print("\nGenerating waveform plots...")
    harmonics.plot_waves(A4)
    
    # Analyze complete scale
    print("\nAnalyzing complete musical scale:")
    scale_analysis = harmonics.analyze_scale()
    for interval, analysis in scale_analysis.items():
        print(f"\n{interval}:")
        print(f"Original Ratio: {analysis['original_ratio']}")
        print(f"Transformed Ratio: {analysis['transformed_ratio']:.6f}")
        print(f"Deviation: {analysis['deviation']:.6f}")
        print(f"Stability: {analysis['stability']:.6f}")

if __name__ == "__main__":
    main()
