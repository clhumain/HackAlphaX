# Program created by Matheus Da Silva for Day 1 of HackAlphaX Coding Olympics
# MAIN: Python Text Calculator
# BONUS: Python Awkward Integer Value function

# BONUS: Python Awkward Integer Value function (?get-link)
def my_awkward_func():
    print("This portion was prepared for the extra points section found through ?get-link in the team server")
    print("Let's start by getting you to enter an integer value between 1 and 1000. \n")

    validinput = False
    while not validinput:
        x = input("Enter an integer value between 1 and 1000: ")
        if x > 1000 or x < 1:
            print("Please enter a valid integer value between 1 and 1000.")
        else:
            validinput = True

    if x % 2 == 0:  # Even numbers
        if 2 <= x <= 7:
            print("Not Awkward")
        elif 9 <= x <= 22:
            print("Awkward")
        elif x > 22:
            print("Not Awkward")
    else:  # Odd numbers
        print("Awkward")

# MAIN: Python Text Calculator
# Introductory text to explain function of script
print("Welcome! This application functions as a calculator that supports "
      "Addition, Subtraction, Multiplication, Division, and Exponentiation functions.\n"
      "Let's start by getting you to enter two numbers, "
      "and then a third number for the type of operation to execute.")

# Outer while loop allows program to repeat itself as many times as user desires
newCalc = True
while newCalc:
    # Get user to input two numbers for calculation
    firstNum = input("First number: ")
    secondNum = input("Second number: ")

    # Get user to input a valid operation, loop until this is fulfilled
    valid = False
    while not valid:
        operation = input("Desired operation:\n"
                          "1. Addition\n"
                          "2. Subtraction\n"
                          "3. Multiplication\n"
                          "4. Division\n"
                          "5. Exponentiation\n")

        # Mapping operational number input to mathematical operation
        if operation == 1:
            answer = firstNum + secondNum
            valid = True
        elif operation == 2:
            answer = firstNum - secondNum
            valid = True
        elif operation == 3:
            answer = firstNum * secondNum
            valid = True
        elif operation == 4:
            answer = firstNum / secondNum
            valid = True
        elif operation == 5:
            answer = firstNum ** secondNum
            valid = True
        else:
            # Final statement controls for invalid inputs outside valid 1-5 range
            print("This input is not valid, enter a valid number between 1 and 5.")

    # Print answer
    print("The answer is {}.\n".format(answer))

    # Ask user if they would like to repeat process, and loop infinitely until a valid answer (y/n) is entered
    valid = False
    while not valid:
        redoCalc = raw_input("Do you want to do another calculation (y/n)? ").lower()
        if redoCalc == "n":
            newCalc = False
            valid = True
        elif redoCalc == "y":
            newCalc = True
            valid = True
        else:
            # Final statement controls for invalid inputs outside valid y/n
            print("Input not valid. Please enter either y or n.\n")
            valid = False

# Demonstrate extra points challenge
# BONUS: Python Awkward Integer Value function
my_awkward_func()

# Exit
print("Thank you! Goodbye.")
