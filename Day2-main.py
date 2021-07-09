# Program created by Matheus Da Silva for Day 1 of HackAlphaX Coding Olympics
# MAIN: Python Text Calculator
# BONUS: Python Awkward Integer Value function

# Importing libraries
import math

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


# Calculator function inputs(firstNum, secondNum, operationNum), outputs(solution, operationSymbol)
def my_calculator_func(first, second, operationNum):
    # Mapping operational number input to mathematical operation and calculating result
    if operationNum == 1:  # Addition function
        solution = first + second
        operationSymbol = "+"
    elif operationNum == 2:  # Subtraction function
        solution = first - second
        operationSymbol = "-"
    elif operationNum == 3:  # Multiplication function
        solution = 1.0 * first * second
        operationSymbol = "x"
    elif operationNum == 4:  # Division function
        solution = 1.0 * first / second  # Multiply by 1.0 so result is a double (avoid precision loss)
        operationSymbol = "/"
    elif operationNum == 5:  # Exponential function
        solution = first ** second
        operationSymbol = "^"
    elif operationNum == 6:  # Factorial function
        if first == 0 or first == 1:  # If number is either zero or one, return result as 1
            solution = 1
        elif first > 1:  # If number is greater than one and positive, calculate factorial using recursion
            solution = first * my_calculator_func(first - 1, 0, 6)[0]
        else:  # Negative value entered
            solution = "UNDEFINED"
        operationSymbol = "!"
    elif operationNum == 7:  # Square root function
        if first == 0:  # sqrt(0) = 0
            solution = 0
        elif first < 0:  # Square root of negatives
            solution = "UNDEFINED"
        else:
            solution = math.sqrt(first)
        operationSymbol = "^(1/2)"
    elif operationNum == 8:  # Log function
        if first < 0 or second < 0:  # Negative logarithms rule
            solution = "UNDEFINED"
        elif second == 0:  # log of zero rule
            solution = "UNDEFINED"
        elif second == 1:  # log_anything(1) = 0
            solution = 0
        else:  # Anything else
            solution = math.log(second, first)  # Syntax: log_first(second)
        operationSymbol = "log_"

    return solution, operationSymbol


# MAIN: Python Text Calculator
# Introductory text to explain function of script
print("Welcome! This application functions as a calculator that supports "
      "Addition, Subtraction, Multiplication, Division, Exponentiation, and Factorial functions.\n"
      "Let's start by getting you to enter two numbers, "
      "and then a third number for the type of operation to execute.")

############ TO-DO: ##############
# 1. Turn calculator into function - DONE
# 2. Add Factorial function - DONE
# 3. OPTIONALLY Add Square Root - DONE and Logarithmic functions

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
                          "1. Addition (+)\n"
                          "2. Subtraction (-)\n"
                          "3. Multiplication (x)\n"
                          "4. Division (/)\n"
                          "5. Exponentiation (^)\n"
                          "6. Factorial (!)\n"
                          "7. Square Root (^1/2)\n"
                          "8. Logarithm (log_first(second))\n")

        # Check if operation input was valid, if not throw error and ask again
        if 1 <= operation <= 8:
            if operation == 6 or operation == 7:  # Factorial and sqrt operations only requires one number,
                                                    # calc each number individually

                # First number (setting secondNum to 0 as input to calculator function)
                answer = my_calculator_func(firstNum, 0, operation)
                # Print answer (formatting answer to two decimal points and printing UNDEFINED for negative numbers)
                if answer[0] == "UNDEFINED":
                    print("\nThe result of {}{} = {}.\n".format(firstNum, answer[1], answer[0]))
                else:
                    print("\nThe result of {}{} = {:.2f}.\n".format(firstNum, answer[1], answer[0]))

                # Second number (setting firstNum to 0 as input to calculator function)
                answer = my_calculator_func(secondNum, 0, operation)
                # Print answer
                if answer[0] == "UNDEFINED":
                    print("The result of {}{} = {}.\n".format(secondNum, answer[1], answer[0]))
                else:
                    print("The result of {}{} = {:.2f}.\n".format(secondNum, answer[1], answer[0]))
            else:  # Any other operational input but factorial or square root
                answer = my_calculator_func(firstNum, secondNum, operation)
                # Print answer
                if operation == 8:  # Log only
                    if answer[0] == "UNDEFINED":
                        print("\nThe result of {}{}({}) = {}.\n".format(answer[1], firstNum, secondNum, answer[0]))
                    else:
                        print("\nThe result of {}{}({}) = {:.2f}.\n".format(answer[1], firstNum, secondNum, answer[0]))
                else:
                    print("\nThe result of {}{}{} = {:.2f}.\n".format(firstNum, answer[1], secondNum, answer[0]))
            valid = True
        else:
            # Final statement controls for invalid inputs outside valid 1-5 range
            print("\nThis input is not valid, enter a valid number between 1 and 8.\n")

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
