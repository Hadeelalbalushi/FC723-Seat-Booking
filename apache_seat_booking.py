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
    if seat in layout: #check if seat exists
        if layout[seat] == 'F':
            layout[seat] = 'R' #change status from free to reserved
            print(f"Seat {seat} has been successfully booked.") # confirm booking
        elif layout[seat] == 'R':
            print("That seat is already booked.") # already booked
        else:
            print("That seat cannot be booked (aisle or storage).") #not bookable
    else:
        print("Seat number not found.") # this message will appear if the user input was invalid 

# defining a function to Free a booked seat
def free_seat(layout, seat):
    if seat in layout:  #if condition to check if seat exists
        if layout[seat] == 'R':
            layout[seat] = 'F' # change status to free
            print(f"Seat {seat} has been freed.")  # confirm release
        elif layout[seat] == 'F':
            print("That seat is already free.")  # already free
        else:
            print("That seat cannot be changed (aisle or storage).")#not changeable
    else:
        print("Seat number not found.") #this message will appear if its invalid input

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
    layout = create_seat_layout() # creating the initial seating map

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