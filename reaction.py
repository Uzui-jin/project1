# Import required libraries
from gpiozero import LED, Button
from time import sleep, time
from random import uniform

# Initialize hardware components
led = LED(4)                 # LED connected to GPIO4
right_button = Button(15)    # Right button connected to GPIO15
left_button = Button(14)     # Left button connected to GPIO14

# Get player names
left_name = input('Left player name: ')
right_name = input('Right player name: ')

# Initialize game variables
left_score = 0
right_score = 0
rounds = 0
max_rounds = 5               # Total number of rounds

def game_round():
    """Execute one complete round of the reaction game"""
    global left_score, right_score, rounds
    
    rounds += 1
    print(f"\n=== Round {rounds} ===")
    
    # Light the LED for random duration (5-10 seconds)
    led.on()
    delay = uniform(5, 10)
    sleep(delay)
    led.off()
    
    # Record the moment LED turns off
    start_time = time()
    reaction_time = None
    winner = None
    
    def pressed(button):
        """Callback function when a button is pressed"""
        nonlocal reaction_time, winner
        current_time = time()
        reaction_time = current_time - start_time
        
        # Determine winner based on which button was pressed
        if button.pin.number == 14:
            winner = left_name
        else:
            winner = right_name
            
        print(f"{winner} wins! Reaction time: {reaction_time:.3f} seconds")
    
    # Assign callback functions to buttons
    right_button.when_pressed = pressed
    left_button.when_pressed = pressed
    
    # Wait for button press (maximum 10 seconds)
    wait_time = 0
    while winner is None and wait_time < 10:
        sleep(0.3)
        wait_time += 0.1
    
    # Update scores
    if winner == left_name:
        left_score += 1
    elif winner == right_name:
        right_score += 1
    else:
        print("No response this round!")
    
    # Display current score
    print(f"Current score: {left_name} {left_score} - {right_score} {right_name}")
    
    # Reset button callbacks
    right_button.when_pressed = None
    left_button.when_pressed = None

# Main game loop
print(f"\nGame starting! Best of {max_rounds} rounds")
try:
    while rounds < max_rounds:
        game_round()
        sleep(2)  # Pause between rounds
        
    # Game over - display final results
    print("\n=== Game Over ===")
    print(f"Final score: {left_name} {left_score} - {right_score} {right_name}")
    
    if left_score > right_score:
        print(f"Congratulations {left_name}, you win!")
    elif right_score > left_score:
        print(f"Congratulations {right_name}, you win!")
    else:
        print("It's a tie!")
        
except KeyboardInterrupt:
    print("\nGame interrupted")
finally:
    # Clean up GPIO resources
    led.off()
    right_button.close()
    left_button.close()


