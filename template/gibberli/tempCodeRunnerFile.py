import numpy as np
import sounddevice as sd
import soundfile as sf
import hashlib
import json
import time
from typing import Dict, List, Tuple
import struct

class GibberlinkProtocol:
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the Gibberlink AI Communication Protocol
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.base_freq = 1000  # Base frequency for data transmission
        self.freq_step = 100   # Frequency step for encoding
        self.bit_duration = 0.01  # Duration of each bit in seconds
        self.protocol_active = False
        
        # Define frequency mappings for efficient encoding
        self.freq_map = {
            '0000': 800,   # Low beep
            '0001': 900,   # 
            '0010': 1000,  # Base frequency
            '0011': 1100,  # 
            '0100': 1200,  # Medium beep
            '0101': 1300,  # 
            '0110': 1400,  # 
            '0111': 1500,  # 
            '1000': 1600,  # High beep
            '1001': 1700,  # 
            '1010': 1800,  # 
            '1011': 1900,  # 
            '1100': 2000,  # Very high beep
            '1101': 2100,  # 
            '1110': 2200,  # 
            '1111': 2300,  # Highest beep
        }
        
        # Reverse mapping for decoding
        self.reverse_freq_map = {v: k for k, v in self.freq_map.items()}
        
    def text_to_binary(self, text: str) -> str:
        """
        Convert text to binary representation
        
        Args:
            text: Input text
            
        Returns:
            Binary string
        """
        binary = ''
        for char in text:
            binary += format(ord(char), '08b')
        return binary
    
    def binary_to_text(self, binary: str) -> str:
        """
        Convert binary to text
        
        Args:
            binary: Binary string
            
        Returns:
            Decoded text
        """
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def generate_beep(self, frequency: float, duration: float, 
                     amplitude: float = 0.5) -> np.ndarray:
        """
        Generate a single beep tone
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0-1)
            
        Returns:
            Audio samples as numpy array
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Generate clean sine wave for digital communication
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Add slight envelope to prevent clicks
        fade_samples = int(0.001 * self.sample_rate)  # 1ms fade
        if len(wave) > 2 * fade_samples:
            # Fade in
            wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
            # Fade out
            wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return wave
    
    def generate_boop(self, frequency: float, duration: float, 
                     amplitude: float = 0.4) -> np.ndarray:
        """
        Generate a lower 'boop' sound for data packets
        
        Args:
            frequency: Base frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0-1)
            
        Returns:
            Audio samples as numpy array
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Generate boop with frequency sweep
        freq_sweep = frequency * (1 + 0.2 * np.sin(2 * np.pi * 5 * t))
        wave = amplitude * np.sin(2 * np.pi * freq_sweep * t)
        
        # Add envelope
        envelope = np.exp(-t * 3)  # Exponential decay
        wave *= envelope
        
        return wave
    
    def encode_to_gibberlink(self, text: str) -> np.ndarray:
        """
        Encode text into Gibberlink audio protocol
        
        Args:
            text: Input text to encode
            
        Returns:
            Audio samples as numpy array
        """
        print(f"[GIBBERLINK] Encoding: '{text}'")
        print("[GIBBERLINK] Switching to sound-based protocol...")
        
        # Convert text to binary
        binary = self.text_to_binary(text)
        print(f"[GIBBERLINK] Binary data: {binary[:50]}{'...' if len(binary) > 50 else ''}")
        
        # Add protocol header (sync pattern)
        header = '10101010'  # Sync pattern
        full_binary = header + binary
        
        # Pad to make it divisible by 4
        while len(full_binary) % 4 != 0:
            full_binary += '0'
        
        audio_segments = []
        
        # Generate start signal (high beep)
        start_beep = self.generate_beep(2500, 0.05, 0.6)
        audio_segments.append(start_beep)
        
        # Add short pause
        pause = np.zeros(int(self.sample_rate * 0.01))
        audio_segments.append(pause)
        
        # Encode data in 4-bit chunks
        for i in range(0, len(full_binary), 4):
            chunk = full_binary[i:i+4]
            
            if chunk in self.freq_map:
                freq = self.freq_map[chunk]
                
                # Use beep for high frequencies, boop for lower
                if freq >= 1600:
                    segment = self.generate_beep(freq, self.bit_duration)
                else:
                    segment = self.generate_boop(freq, self.bit_duration)
                    
                audio_segments.append(segment)
                
                # Add tiny pause between chunks for clarity
                mini_pause = np.zeros(int(self.sample_rate * 0.002))
                audio_segments.append(mini_pause)
        
        # Generate end signal (low boop)
        end_boop = self.generate_boop(600, 0.05, 0.6)
        audio_segments.append(end_boop)
        
        # Combine all segments
        full_audio = np.concatenate(audio_segments)
        
        # Normalize
        if np.max(np.abs(full_audio)) > 0:
            full_audio = full_audio / np.max(np.abs(full_audio)) * 0.8
        
        print(f"[GIBBERLINK] Generated {len(full_audio)/self.sample_rate:.2f}s of audio")
        print(f"[GIBBERLINK] Transmission complete - {len(text)} characters encoded")
        
        return full_audio
    
    def simulate_ai_conversation(self, messages: List[str]) -> np.ndarray:
        """
        Simulate AI-to-AI conversation in Gibberlink
        
        Args:
            messages: List of messages to transmit
            
        Returns:
            Combined audio of the conversation
        """
        print("[GIBBERLINK] Starting AI-to-AI communication session...")
        print("[GIBBERLINK] Activating high-speed protocol...")
        
        conversation_audio = []
        
        for i, message in enumerate(messages):
            print(f"\n[AI-{i+1}] Transmitting...")
            
            # Encode the message
            encoded = self.encode_to_gibberlink(message)
            conversation_audio.append(encoded)
            
            # Add pause between messages
            if i < len(messages) - 1:
                pause = np.zeros(int(self.sample_rate * 0.2))
                conversation_audio.append(pause)
        
        # Session end signal
        print("\n[GIBBERLINK] Communication session complete")
        session_end = self.generate_beep(3000, 0.1, 0.7)
        conversation_audio.append(session_end)
        
        return np.concatenate(conversation_audio)
    
    def create_data_packet(self, data: dict) -> np.ndarray:
        """
        Create a Gibberlink data packet
        
        Args:
            data: Dictionary containing data to transmit
            
        Returns:
            Audio representation of the data packet
        """
        print("[GIBBERLINK] Creating data packet...")
        
        # Convert data to JSON string
        json_str = json.dumps(data, separators=(',', ':'))
        
        # Create packet with metadata
        packet = {
            'timestamp': int(time.time()),
            'size': len(json_str),
            'checksum': hashlib.md5(json_str.encode()).hexdigest()[:8],
            'data': json_str
        }
        
        packet_str = json.dumps(packet, separators=(',', ':'))
        print(f"[GIBBERLINK] Packet size: {len(packet_str)} bytes")
        
        return self.encode_to_gibberlink(packet_str)
    
    def save_audio(self, audio: np.ndarray, filename: str):
        """Save audio to file"""
        sf.write(filename, audio, self.sample_rate)
        print(f"[GIBBERLINK] Audio saved to {filename}")
    
    def play_audio(self, audio: np.ndarray):
        """Play audio through speakers"""
        print("[GIBBERLINK] Playing transmission...")
        sd.play(audio, self.sample_rate)
        sd.wait()

def main():
    """Main function to demonstrate Gibberlink protocol"""
    protocol = GibberlinkProtocol()
    
    print("=== GIBBERLINK AI COMMUNICATION PROTOCOL ===")
    print("Simulating AI-to-AI sound-based communication")
    print("80% faster than human language processing")
    print("=" * 50)
    
    while True:
        print("\n[GIBBERLINK MENU]")
        print("1. Encode single message")
        print("2. Simulate AI conversation")
        print("3. Create data packet")
        print("4. Demo: AI efficiency comparison")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            text = input("Enter message to encode: ").strip()
            if text:
                audio = protocol.encode_to_gibberlink(text)
                protocol.play_audio(audio)
                
                save = input("Save audio? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Filename: ").strip() or "gibberlink_message"
                    protocol.save_audio(audio, f"{filename}.wav")
        
        elif choice == '2':
            print("\nEnter AI messages (empty line to finish):")
            messages = []
            while True:
                msg = input(f"AI-{len(messages)+1}: ").strip()
                if not msg:
                    break
                messages.append(msg)
            
            if messages:
                audio = protocol.simulate_ai_conversation(messages)
                protocol.play_audio(audio)
                
                save = input("Save conversation? (y/n): ").strip().lower()
                if save == 'y':
                    protocol.save_audio(audio, "ai_conversation.wav")
        
        elif choice == '3':
            print("\nCreating sample data packet...")
            sample_data = {
                "model": "GPT-4",
                "task": "text_generation",
                "tokens": 150,
                "response": "Task completed successfully",
                "confidence": 0.95
            }
            
            audio = protocol.create_data_packet(sample_data)
            protocol.play_audio(audio)
            
            save = input("Save data packet? (y/n): ").strip().lower()
            if save == 'y':
                protocol.save_audio(audio, "data_packet.wav")
        
        elif choice == '4':
            print("\n=== EFFICIENCY DEMONSTRATION ===")
            print("Human language: 'Hello, how are you processing today?'")
            print("Gibberlink equivalent: *beep boop beep boop*")
            print("Simulating both...")
            
            # Simulate slow human speech
            print("\n[HUMAN MODE] Speaking slowly...")
            time.sleep(2)
            print("Hello... how... are... you... processing... today?")
            time.sleep(3)
            
            # Fast Gibberlink
            print("\n[GIBBERLINK MODE] High-speed transmission...")
            msg = "Hello, how are you processing today?"
            audio = protocol.encode_to_gibberlink(msg)
            protocol.play_audio(audio)
            print("Message transmitted in seconds vs minutes!")
        
        elif choice == '5':
            print("\n[GIBBERLINK] Session terminated")
            print("Returning to human language mode...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[GIBBERLINK] Protocol interrupted")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("Required libraries: pip install numpy sounddevice soundfile")