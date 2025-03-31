import random #import the 'random' module to generate random values
import string #import the 'string' module to access string-related functions and constants
import sqlite3

# connecting to the SQLite database and ensure table exists
def create_database():
    conn = sqlite3.connect("bookings.db")  # Create or open DB file
    cursor = conn.cursor()

    # Create bookings table with required columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            reference TEXT PRIMARY KEY,
            passport TEXT,
            first_name TEXT,
            last_name TEXT,
            seat_row INTEGER,
            seat_column TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def save_customer_to_database(reference, passport, first_name, last_name, row, column):
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (reference, passport, first_name, last_name, seat_row, seat_column)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (reference, passport, first_name, last_name, row, column))
    conn.commit()
    conn.close()
    
def remove_customer_from_database(row, column):
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM bookings WHERE seat_row = ? AND seat_column = ?
    ''', (row, column))
    conn.commit()
    conn.close()


# This set will keep track of all generated booking references
used_references = set()

# Function to generate a unique 8-character booking reference
def generate_unique_reference():
    """
    This function creates a random 8-character booking reference
    made up of uppercase letters and digits.
    It ensures the reference is unique by checking against a set of used references.
    """
    while True:
        # Step 1: Create a string of possible characters (A-Z and 0-9)
        characters = string.ascii_uppercase + string.digits

        # Step 2: Randomly select 8 characters from the pool
        reference = ''.join(random.choices(characters, k=8))

        # Step 3: Check if it's unique (not used before)
        if reference not in used_references:
            used_references.add(reference)  # Save it to prevent future repeats
            return reference


#defining a function to save a booking to a file
def save_booking_to_file(seat, reference):
    with open("bookings.txt", "a") as file:  # open in append mode
        file.write(f"Seat: {seat} | Reference: {reference}\n")  # Save to file


# Apache Airlines Seat Booking application (Part A4)
def create_seat_layout():
    """
  defining a function to creat the seat layout for the application 
 'F' = Free, 'R' = Reserved, 'X' = Aisle, 'S' = Storage
 """
    rows = 80 # Total number of rows in the aircraft
    seats_per_row = ['A', 'B', 'C', 'D', 'E', 'F'] # Seat labels in each row
    layout = {}  # initialising an empty dictionary to hold seat status

    for row in range(1, rows + 1): # using a for loop to iterate through rows 1 to 80
        for seat in seats_per_row:# using a for loop iterate through each seat letter
            if seat == 'D' and row > 75: # using conditions to know if the seats are a storage seat or aisle or free seats.
                layout[f"{row}{seat}"] = 'S'  # mark as storage if row > 75
            elif seat == 'E' and row > 75:
                layout[f"{row}{seat}"] = 'S'  # mark as storage
            elif seat == 'F' and row > 75:
                layout[f"{row}{seat}"] = 'S'  # mark as storage
            elif seat == 'C':  # assume aisle between C and D
                layout[f"{row}{seat}"] = 'X' # then mark 'C' as aisle
            else:
                layout[f"{row}{seat}"] = 'F' # all other seats start as free
    return layout # return the completed seat layout

# defining a function to Check if a seat is available
def check_seat_availability(layout, seat):
    if seat in layout: #using the if condition to check if seat exists
        status = layout[seat] #get the current status of the seat
        if status == 'F':
            print(f"Seat {seat} is available.") #seat is free
        elif status == 'R':
            print(f"Seat {seat} is already booked.")# seat is booked
        elif status == 'X':
            print(f"Seat {seat} is an aisle and cannot be booked.") # aisle seat 
        elif status == 'S':
            print(f"Seat {seat} is a storage area and cannot be booked.") #storage seat 
    else:
        print("This Seat number is not found. Please check your seat number and try again.") # if its invalid input, it appear this message

# defining a function to Book a seat if it's free
def book_seat(layout, seat):
   if seat in layout and layout[seat] == 'F':
            reference = generate_unique_reference() # Create booking reference
            # Ask for customer details
            passport = input("Enter passport number: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            row = int(seat[:-1])
            column = seat[-1]
            
            layout[seat] = reference  # Store reference instead of 'R'
            save_customer_to_database(reference, passport, first_name, last_name, row, column)

            print(f"Seat {seat} booked successfully.")
            print(f"Booking reference: {reference}") 
   elif seat in layout and layout[seat] != 'F':
            print("Seat is already booked or unavailable.")
   else:
            print("Invalid seat number.")
        
# defining a function to Free a booked seat
def free_seat(layout, seat):
    if seat in layout and layout[seat] != 'F' and layout[seat] != 'X' and layout[seat] != 'S':
        row = int(seat[:-1])
        column = seat[-1]
        layout[seat] = 'F'  # Reset seat to free
        remove_customer_from_database(row, column)  # Remove from DB
        print(f"Seat {seat} has been freed and booking deleted.")
    else:
        print("Seat is already free or cannot be modified.")

# defining a function to Display the entire seat layout
def display_seating(layout):
    print("\nCurrent Seat Layout (R = Reserved, F = Free, X = Aisle, S = Storage):")#header
    for row in range(1, 81): # using for loop to iterate through rows 1 to 80
        row_display = f"Row {row:02}: " # format row number
        for seat in ['A', 'B', 'C', 'D', 'E', 'F']: # using for loop to iterat through each seat in the row
            seat_code = f"{row}{seat}" # combine row and seat label
            row_display += layout.get(seat_code, ' ') + " "  # getting status symbol
        print(row_display)# show row
    print()#printing an empty line after layout
    
#defining a new Function for part A4 to find the nearest available seat to a given seat
def find_nearest_available_seat(layout, preferred_seat):  #checking if the given seat exists in the layout
    if preferred_seat not in layout:
        print("Invalid seat number.")#show this message if the the user input  invalid seat number 
        return 

    # take the row number and seat letter from input
    try:
        row = int(preferred_seat[:-1])  #to get the row number it is all characters except last
        seat_letter = preferred_seat[-1]  #get the seat letter which is the Last character
    except ValueError:
        print("Invalid seat format.") #notify the user if the input is not a propar formatted
        return

    search_radius = 3   # define how many rows above and below to search for an available seat
    for offset in range(search_radius + 1):#loop through rows within the defined search radius
        for direction in [-1, 1]:  # Check both directions: above(-1) and below(+1)
            current_row = row + (offset * direction)  # calculating the row being checked
            if current_row < 1 or current_row > 80: # Skip invalid rows
                continue  #continue to the next iteration

            for seat in ['A', 'B', 'D', 'E', 'F']:  # iterating through seat letters to check availability and avoid checking 'C' (aisle)
                seat_code = f"{current_row}{seat}"
                if seat_code in layout and layout[seat_code] == 'F': # check if the seat exists and is free ('F')
                    print(f"Nearest available seat to {preferred_seat} is: {seat_code}") #output the nearest seat
                    return #exit the function after finding a seat
    print("No available seat found nearby.") #if no seat is found within the search radius, show this message for the user


# creating the Main Menu
def main():
    
    create_database()                 
    layout = create_seat_layout()

    while True:# using while loop to show the main menu until user exits
        print("\nApache Airlines Seat Booking application ")# menu title
        print("1. Check availability of seat")# option 1
        print("2. Book a seat")# option 2
        print("3. Free a seat")# option 3
        print("4. Show booking status")# option 4
        print("5. Exit program")# option 5
        print("6. Find nearest available seat")  # new option 6 
        choice = input("Enter your choice (1-6): ")# ask the user for choice

        if choice == '1':
            seat = input("Enter seat number (for example: 12A): ").upper() # ask for seat
            check_seat_availability(layout, seat)  #calling the function
        elif choice == '2':
            seat = input("Enter seat number to book (for example: 12A): ").upper()# ask for seat
            book_seat(layout, seat) #calling the function
        elif choice == '3':
            seat = input("Enter seat number to free (for example: 12A): ").upper()# ask for seat
            free_seat(layout, seat) #calling the function
        elif choice == '4':
            display_seating(layout)# show the current layout
        elif choice == '5':
            print("Exiting the program.") # exiting message
            break
        elif choice == '6':
            seat = input("Enter your preferred seat (for example: 12A): ").upper()# ask for seat
            find_nearest_available_seat(layout, seat) #calling the function
        else:
            print("Invalid option. Please enter a number between 1 and 6.") # this message will appear if it was a wrong input

# Run the program
if __name__ == "__main__":
    main()  #call main menu
   