import tkinter as tk
from tkinter import ttk
import random
import pygame

class DiceSimulator(tk.Tk):
    """
    A professional Dice Roll Simulator with a modern GUI, animations, and sound effects using Pygame.
    """
    def __init__(self):
        """Initialize the main application window, Pygame mixer, and core components."""
        super().__init__()
        self.title("Dice Roll Simulator")
        self.geometry("600x400")
        self.resizable(True, True)  # Allow resizing for responsiveness
        
        # Initialize Pygame mixer for sound
        pygame.mixer.init()
        try:
            self.roll_sound = pygame.mixer.Sound('dice_sound.mp3')
        except pygame.error as e:
            print(f"Warning: Could not load 'dice_sound.mp3'. Sound disabled. Error: {e}")
            self.roll_sound = None
        
        # Initialize data
        self.history = []  # Store recent rolls
        self.dice_images = {}  # Store dice face images
        
        # Load assets and set up UI
        self.load_images()
        self.setup_ui()
        
        # Bind space key to roll dice for accessibility
        
        self.bind('<space>', lambda event: self.roll_button.invoke())

    def load_images(self):
        """
        Load dice images from the 'images' directory.
        Raises SystemExit if images are missing to ensure graceful failure.
        """
        try:
            for i in range(1, 7):
                self.dice_images[i] = tk.PhotoImage(file=f'images/dice{i}.png')
        except tk.TclError as e:
            print(f"Error: Unable to load dice images. Ensure 'images/dice1.png' to 'dice6.png' exist.")
            self.destroy()
            raise SystemExit

    def setup_ui(self):
        """Set up the user interface with styled widgets and a clean layout."""
        # Apply modern theme and styling
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme
        style.configure('TButton', font=('Helvetica', 14, 'bold'), padding=10)
        style.configure('TLabel', font=('Helvetica', 12))

        # Title label
        self.title_label = ttk.Label(self, text="Dice Roll Simulator", font=('Helvetica', 18, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Dice display
        self.dice_label = ttk.Label(self, image=self.dice_images[1])
        self.dice_label.grid(row=1, column=0, padx=20, pady=20)

        # Roll button
        self.roll_button = ttk.Button(self, text="Roll Dice", command=self.roll_dice)
        self.roll_button.grid(row=2, column=0, padx=20, pady=20)

        # History section
        self.history_label = ttk.Label(self, text="Roll History:\n", font=('Helvetica', 12), anchor='w')
        self.history_label.grid(row=1, column=1, rowspan=2, padx=20, pady=20, sticky='nw')

        # Configure grid weights for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def roll_dice(self):
        """Handle the dice roll action: play sound with Pygame, animate, and update state."""
        if self.roll_button['state'] == 'disabled':
            return  # Prevent multiple rolls during animation
        
        self.roll_button.config(state='disabled')
        # Play sound if loaded
        if self.roll_sound:
            self.roll_sound.play()  # Pygame plays sound asynchronously
        final_face = random.randint(1, 6)
        self.animate_roll(final_face)

    def animate_roll(self, final_face, count=5):
        """
        Animate the dice roll by cycling through random faces before showing the final result.
        
        Args:
            final_face (int): The final dice face to display.
            count (int): Number of animation frames remaining (default: 5).
        """
        if count > 0:
            random_face = random.randint(1, 6)
            self.update_dice_image(random_face)
            self.after(100, lambda: self.animate_roll(final_face, count - 1))
        else:
            self.update_dice_image(final_face)
            self.history.append(final_face)
            self.update_history()
            self.roll_button.config(state='normal')

    def update_dice_image(self, face):
        """Update the displayed dice image based on the given face value."""
        self.dice_label.config(image=self.dice_images[face])

    def update_history(self):
        """Update the history label with the last 5 rolls."""
        history_text = "Roll History:\n" + "\n".join(map(str, self.history[-5:]))
        self.history_label.config(text=history_text)

    def destroy(self):
        """Override destroy to clean up Pygame mixer before closing."""
        pygame.mixer.quit()  # Clean up Pygame resources
        super().destroy()

if __name__ == "__main__":
    """Launch the Dice Roll Simulator application."""
    app = DiceSimulator()
    app.mainloop()