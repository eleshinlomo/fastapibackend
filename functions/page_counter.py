import os

def get_counter():
    counter_file_path = "counter.txt"

    # Check if the file exists
    if os.path.exists(counter_file_path):
        # Read the counter value from the file
        with open(counter_file_path, "r") as file:
            counter = int(file.read())
            
    else:
        # If the file doesn't exist, initialize the counter to 0
        counter = 0

    return counter

def increment_counter():
    counter_file_path = "./counter.txt"

    # Get the current counter value
    counter = get_counter()

    # Increment the counter
    counter += 1

    # Write the updated counter value back to the file
    with open(counter_file_path, "w") as file:
        file.write(str(counter))

    return counter

# Example usage:
current_counter = get_counter()
print(f"Current counter value: {current_counter}")

new_counter = increment_counter()
print(f"New counter value: {new_counter}")
