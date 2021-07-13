# Program created by Matheus Da Silva for Day 4 of HackAlphaX Coding Olympics
# MAIN: Python GUI-based Calculator

# Importing libraries
import sys
from decimal import Decimal
import pygame
from pygame.locals import *
import math

# TO-DO:
# 1. Set up text output line - DONE
# 1.5. Set up output area - DONE
# 2. Set up number pad buttons - DONE
# 2.5 Set up number pad area - DONE
# 3. Set up operator pad - DONE
# 4. Link buttons to output line - DONE
# 5. Link buttons to calculations - DONE
# 6. Modify equals button to also be clear button - DONE
# 7. Introduce brackets (left and right) - OPTIONAL
# 8. Finish setting up blinking output line
# 9. Allow continuous calculation (using old answer) - DONE

# Initialize pygame module
pygame.init()

# Initialize color values
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)
black = pygame.Color(0, 0, 0)
lightblue = pygame.Color(135, 206, 250)
red = pygame.Color(233, 116, 82)

# Initialize game screen (600[W]x800[H])
display = pygame.display.set_mode((600, 800))
display.fill(black)
pygame.display.set_caption("Python Calculator - Made by Matheus Da Silva")

# Initialize screen areas helper values
maxX, maxY = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
edgetolerance = 5  # Arbitrarily chosen, 5 pixel tolerance around major areas, buttons, and output display
height_Output = 100  # Arbitrarily chosen, height of output box
width_Operators = 100  # Arbitrarily chosen, width of operators area

height_operator_and_numbers = 800 - 3*edgetolerance - height_Output  # Height of operator and number pad areas
# debugging
print("height of operator and number pad areas:" + str(height_operator_and_numbers))

# Setting up areas known anchor points
topRight_location_output = (maxX - edgetolerance, edgetolerance)
topLeft_location_operators = (edgetolerance, 2 * edgetolerance + height_Output)
bottomRight_location_numbers = (maxX - edgetolerance, maxY - edgetolerance)
# debugging
print("output area anchor point:" + str(topRight_location_output))
print("operator area anchor point:" + str(topLeft_location_operators))
print("number pad area anchor point:" + str(bottomRight_location_numbers))

# Output text area sizing
width_output = 600 - 2 * edgetolerance
# debugging
print("Output width:" + str(width_output))

# Operators area and button sizing
width_Operator = 100 - 2 * edgetolerance  # one column, width of one button
height_Operator = (height_operator_and_numbers - 10 * edgetolerance) // 9  # 9 total operators, height of one button
# debugging
print("operator button width:" + str(width_Operator))
print("operator button height:" + str(height_Operator))

# Number pad area and button sizing
width_Numbers = 600 - 3 * edgetolerance - width_Operators  # Width of number pad area
height_Number = (height_operator_and_numbers - 5*edgetolerance)//4  # 4 rows, height of one button
width_Number = (width_Numbers - 4*edgetolerance)//3  # 3 columns, width of one button
# debugging
print("width of number pad area:" + str(width_Numbers))
print("number button height:" + str(height_Number))
print("number button width:" + str(width_Number))

# Initializing boolean counter variables to keep track of numbers and operations input
firstNum, operation, secondNum = False, False, False
firstVal, secondVal, operator = 0, 0, 0

# Reset global values
def resetglobals():
    global firstNum, operation, secondNum, firstVal, secondVal, operator
    firstNum, operation, secondNum, oldResult = False, False, False, False
    firstVal, secondVal, operator = 0, 0, 0
    if outputTextArea.text != '':
        if outputTextArea.text != 'Invalid Input' and outputTextArea.text != "UNDEFINED":  # There is a previously calculated value in the output
            firstNum = True
            firstVal = float(outputTextArea.text)

# Calculator function inputs(firstNum, secondNum, operationNum), outputs(solution)
def my_calculator_func(first, second, operationSymbol):
    # Mapping operational number input to mathematical operation and calculating result
    if operationSymbol == '+':  # Addition function
        solution = first + second

    elif operationSymbol == '-':  # Subtraction function
        solution = first - second

    elif operationSymbol == 'x':  # Multiplication function
        solution = first * second

    elif operationSymbol == '/':  # Division function
        solution = first / second  # Multiply by 1.0 so result is a double (avoid precision loss)

    elif operationSymbol == '^':  # Exponential function
        solution = first ** second

    elif operationSymbol == '^(1/2)':  # Square root function
        if first == 0:  # sqrt(0) = 0
            solution = 0
        elif first < 0:  # Square root of negatives
            solution = "UNDEFINED"
        else:
            solution = math.sqrt(first)

    elif operationSymbol == 'log_a(b)':  # Log function
        if first < 0 or second < 0:  # Negative logarithms rule
            solution = "UNDEFINED"
        elif second == 0:  # log of zero rule
            solution = "UNDEFINED"
        elif second == 1:  # log_anything(1) = 0
            solution = 0
        elif first == 1:  # log_1(anything) = UNDEFINED
            solution = "UNDEFINED"
        else:  # Anything else
            solution = math.log(second, first)  # Syntax: log_first(second)

    return solution

# Calculator function inputs(firstNum, operationNum), outputs(solution)
def my_calculator_func2(first, operationSymbol):  # Factorial and square root only
    if operationSymbol == '!':  # Factorial function
        if first == 0 or first == 1:  # If number is either zero or one, return result as 1
            solution = 1
        elif first > 1:  # If number is greater than one and positive, calculate factorial using recursion
            solution = first * my_calculator_func2(first - 1, '!')
        elif type(first) is not int:  # Non-integer value
            solution = "UNDEFINED"
        else:  # Negative value entered
            solution = "UNDEFINED"

    elif operationSymbol == '^(1/2)':  # Square root function
        if first == 0:  # sqrt(0) = 0
            solution = 0
        elif first < 0:  # Square root of negatives
            solution = "UNDEFINED"
        else:
            solution = math.sqrt(first)

    return solution

# Set up output area class
class OutputArea(pygame.sprite.Sprite):
    def __init__(self, text = None):
        cornerX = topRight_location_output[0]
        cornerY = topRight_location_output[1]

        super().__init__()
        # Font Source: https://www.1001fonts.com/source-code-pro-font.html
        self.font = pygame.font.Font('SourceCodePro-Regular.ttf', 70)

        # If no text provided, just want output box
        if text == 'Output':
            self.surf = pygame.Surface((width_output, height_Output))
            self.rect = self.surf.get_rect(topright=(cornerX, cornerY))
        elif text == 'Operators':
            cornerX = topLeft_location_operators[0]
            cornerY = topLeft_location_operators[1]
            self.surf = pygame.Surface((width_Operators, height_operator_and_numbers))
            self.rect = self.surf.get_rect(topleft=(cornerX, cornerY))
        elif text == 'Numbers':
            cornerX = bottomRight_location_numbers[0]
            cornerY = bottomRight_location_numbers[1]
            self.surf = pygame.Surface((width_Numbers, height_operator_and_numbers))
            self.rect = self.surf.get_rect(bottomright=(cornerX, cornerY))
        else:  # If text provided, print inside of output box
            self.text = text
            self.textBox = self.font.render(text, True, black)
            self.rect = self.textBox.get_rect(bottomright=(cornerX - edgetolerance, cornerY + height_Output - edgetolerance))

    def update(self, text = None, cornerX = topRight_location_output[0], cornerY = topRight_location_output[1]):
        if text is None:  # If no text passed in, just clear output line
            self.text = ''
        elif self.text == 'Invalid Input' or self.text == 'UNDEFINED':
            self.text = text
        else:  # Otherwise add what was just entered to output line
            if type(text) is not str:
                self.text = self.text + str(text)
            else:
                self.text = self.text + text
        self.textBox = self.font.render(self.text, True, black)
        self.rect = self.textBox.get_rect(bottomright=(cornerX - edgetolerance, cornerY + height_Output - edgetolerance))
        self.show()

    # TO-DO: FINISH FLASHING FUNCTION
    def flashing(self):
        # Blink output to show calculator is working only if no present values
        if self.text == ' ':
            self.text = self.font.render('', True, black)
        elif self.text == '':
            self.text = self.font.render(' ', True, black)

    def show(self, surface = display, use = None):
        if use == 'Output':
            pygame.draw.rect(surface, white, self.rect, 0, 15)
        elif use == 'Operators':
            pygame.draw.rect(surface, grey, self.rect)
        elif use == 'Numbers':
            pygame.draw.rect(surface, grey, self.rect)
        else:  # Output text only
            surface.blit(self.textBox, self.rect)

# Set up Operator Button class
class OperatorButton(pygame.sprite.Sprite):
    def __init__(self, starterText, row):
        cornerX = topLeft_location_operators[0]
        cornerY = topLeft_location_operators[1]
        self.starterText = starterText

        super().__init__()
        # Font Source: https://www.1001fonts.com/source-code-pro-font.html
        self.font = pygame.font.Font('SourceCodePro-Regular.ttf', 16)
        self.text = self.font.render(starterText, True, black)
        self.rect = pygame.draw.rect(display, white, (cornerX+edgetolerance, cornerY + edgetolerance*row + height_Operator*(row-1), width_Operator, height_Operator))

    def clicked(self, text, outputTextArea):
        # Check if button was clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Button was clicked
            global firstNum, secondNum, operation, firstVal, secondVal, operator
            if firstNum and not operation:  # First number already entered, operator just entered
                operator = self.starterText
                if operator == '=/CLEAR':  # Clear
                    outputTextArea.update()
                    resetglobals()
                elif operator == '!' or operator == '^(1/2)':  # Factorial or exponential so calculate using only one value
                    self.calculate(firstVal, operator)
                else:
                    operation = True
            elif (firstNum and operation and secondNum) and self.starterText == '=/CLEAR':  # 2 values and operator entered
                # Equal sign entered, calculate using two values
                self.calculate(firstVal, operator, secondVal)
            else:
                if operator == '=/CLEAR':  # Clear
                    outputTextArea.update()
                    resetglobals()
                else:
                    if outputTextArea.text == 'UNDEFINED' or outputTextArea.text == 'Invalid Input':
                        outputTextArea.update()
                        resetglobals()
                    else:
                        # Invalid operator used, print out invalid input
                        outputTextArea.update()
                        outputTextArea.update('Invalid Input')
                        resetglobals()

    def show(self, surface):
        # Place text in centre of corresponding button using computation to account for width of text
        if self.starterText == '=/CLEAR':  # Red equal button
            rectangle = pygame.draw.rect(surface, red, self.rect, 0, 15)
        else:  # Other operation buttons white
            rectangle = pygame.draw.rect(surface, white, self.rect, 0, 15)
        surface.blit(self.text, (rectangle.x + (width_Operator - self.text.get_width()) / 2, rectangle.y + (height_Operator - self.text.get_height()) / 2))

    def calculate(self, first, op, second = None):
        global firstNum, operation, secondNum, firstVal, operator, secondVal
        if second is None:  # Calculate using only one value
            answer = my_calculator_func2(first, op)
        else:  # Calculate using two values
            answer = my_calculator_func(first, second, op)
        # Print answer
        outputTextArea.update()
        if type(answer) is str:  # Answer was either UNDEFINED or Invalid
            outputTextArea.update(answer)
        else:
            if type(answer) is float:
                answer = str(answer)
            afterDecimal = abs(Decimal(float(answer)).as_tuple().exponent)  # Get number of decimal places in answer
            totalLength = len(answer)  # Get number of digits in answer
            # Print with maximum precision up to 13 digits total (empirical spacing limit)
            if totalLength <= 13:
                outputTextArea.update("{}".format(round(float(answer), afterDecimal)))
            else:
                if 'e+' in answer:
                    temp = answer
                    efix = answer[answer.find('e+'):]
                    rest = 13 - len(efix)
                    fixedoutput = temp[:rest] + efix
                    outputTextArea.update("{}".format(fixedoutput))
                else:
                    if afterDecimal < totalLength:  # Counteract bug with Decimal.exponent function
                        beforeDecimal = totalLength - 1 - afterDecimal
                    else:
                        beforeDecimal = answer.find('.')
                    outputTextArea.update("{}".format(round(float(answer), 12 - beforeDecimal)))
        # Reset global variables
        resetglobals()

# Set up Number Pad Button class
class NumberButton(pygame.sprite.Sprite):
    def __init__(self, starterText, row, col):
        cornerX = bottomRight_location_numbers[0]
        cornerY = bottomRight_location_numbers[1]
        self.starterText = starterText

        super().__init__()
        # Font Source: https://www.1001fonts.com/source-code-pro-font.html
        self.font = pygame.font.Font('SourceCodePro-Regular.ttf', 45)
        self.text = self.font.render(starterText, True, black)
        self.rect = pygame.draw.rect(display, white, (cornerX - (edgetolerance+width_Number)*col, cornerY - (edgetolerance + height_Number)*row, width_Number,height_Number))

    def clicked(self, text, outputTextArea):
        # Check if button was clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Button was clicked
            # Load in global variables
            global firstNum, firstVal, secondVal, secondNum, operation
            if not firstNum:  # First number being entered
                # Reset output line before writing to it
                if outputTextArea.text == '':
                    outputTextArea.update()

                # Update output
                if type(text) is not str:
                    outputTextArea.update(str(text))
                    firstVal = float(outputTextArea.text)
                else:
                    outputTextArea.update(text)
                    firstVal = outputTextArea.text
                firstNum = True
            elif firstNum and not operation:  # still first number but following digits
                if type(text) is not str:
                    outputTextArea.update(str(text))
                else:
                    if text == '-':
                        if outputTextArea.text[0] == '-' and firstVal < 0:  # Correct negative number
                            # Correct global first value and output line
                            temp = outputTextArea.text
                            outputTextArea.update()
                            outputTextArea.update(temp[1:])
                            firstVal = -firstVal
                        else:  # Make first value negative and update output
                            temp = outputTextArea.text
                            firstVal = float(temp)
                            outputTextArea.update()
                            outputTextArea.update(text)
                            outputTextArea.update(temp)
                    else:  # point button
                        if '.' not in outputTextArea.text:  # Check if a point already exists
                            outputTextArea.update(text)
                            firstVal = float(outputTextArea.text)

                if type(outputTextArea.text) is str:
                    firstVal = float(outputTextArea.text)
                else:
                    firstVal = outputTextArea.text
            elif firstNum and operation:  # First number and operator already entered
                if not secondNum:  # First digit only
                    # Reset output line before first writing to it
                    outputTextArea.update()

                # All following digits
                if type(text) is not str:
                    outputTextArea.update(str(text))
                    secondVal = float(outputTextArea.text)
                else:
                    if not secondNum:  # First digit
                        outputTextArea.update(text)
                        secondNum = True
                    elif text == '-' and secondNum:  # All other digits
                        if outputTextArea.text[0] == '-' and secondVal < 0:  # Correct negative number
                            # Correct global first value and output line
                            temp = outputTextArea.text
                            outputTextArea.update()
                            outputTextArea.update(temp[1:])
                            secondVal = -secondVal
                        else:  # Make first value negative and update output
                            temp = outputTextArea.text
                            secondVal = float(temp)
                            outputTextArea.update()
                            outputTextArea.update(text)
                            outputTextArea.update(temp)
                    else:  # Point only
                        if '.' not in outputTextArea.text:  # Check if a point already exists
                            outputTextArea.update(text)
                            secondVal = float(outputTextArea.text)
                secondNum = True

    def show(self, surface):
        # Place text in centre of corresponding button using computation to account for width of text
        if self.starterText == '(-)':  # Red equal button
            rectangle = pygame.draw.rect(surface, lightblue, self.rect, 0, 15)
        else:
            rectangle = pygame.draw.rect(surface, white, self.rect, 0, 15)
        surface.blit(self.text, (rectangle.x + (width_Number - self.text.get_width())/2, rectangle.y + (height_Number - self.text.get_height())/2))

# Setting program tick speed
FPS = pygame.time.Clock()

# Initialize output area inputs('type')
outputArea = OutputArea('Output')
# Initialize output text area inputs('text')
outputTextArea = OutputArea('')

# Initialize operators pad area inputs('type')
operatorsArea = OutputArea('Operators')
# Initialize operator pad buttons inputs('text', row)
plusButton = OperatorButton('+', 1)
minusButton = OperatorButton('-', 2)
multButton = OperatorButton('x', 3)
divButton = OperatorButton('/', 4)
expButton = OperatorButton('^', 5)
factButton = OperatorButton('!', 6)
sqrtButton = OperatorButton('^(1/2)', 7)
logButton = OperatorButton('log_a(b)', 8)
equalsButton = OperatorButton('=/CLEAR', 9)

# Initialize number pad area inputs('type')
buttonsArea = OutputArea('Numbers')
# Initialize number pad buttons inputs('text', row, col) [bottom->top && left->right]
negativeButton = NumberButton('(-)', 1, 3)
zeroButton = NumberButton('0', 1, 2)
pointButton = NumberButton('.', 1, 1)
oneButton = NumberButton('1', 2, 3)
twoButton = NumberButton('2', 2, 2)
threeButton = NumberButton('3', 2, 1)
fourButton = NumberButton('4', 3, 3)
fiveButton = NumberButton('5', 3, 2)
sixButton = NumberButton('6', 3, 1)
sevenButton = NumberButton('7', 4, 3)
eightButton = NumberButton('8', 4, 2)
nineButton = NumberButton('9', 4, 1)

# Clock helps keep time flashing operation
clock = 0
# Infinite game loop
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:  # Mouse pressed
            zeroButton.clicked(0, outputTextArea)
            oneButton.clicked(1, outputTextArea)
            twoButton.clicked(2, outputTextArea)
            threeButton.clicked(3, outputTextArea)
            fourButton.clicked(4, outputTextArea)
            fiveButton.clicked(5, outputTextArea)
            sixButton.clicked(6, outputTextArea)
            sevenButton.clicked(7, outputTextArea)
            eightButton.clicked(8, outputTextArea)
            nineButton.clicked(9, outputTextArea)
            negativeButton.clicked('-', outputTextArea)
            pointButton.clicked('.', outputTextArea)
            plusButton.clicked('+', outputTextArea)
            minusButton.clicked('-', outputTextArea)
            multButton.clicked('x', outputTextArea)
            divButton.clicked('/', outputTextArea)
            expButton.clicked('^', outputTextArea)
            factButton.clicked('!', outputTextArea)
            sqrtButton.clicked('^(1/2)', outputTextArea)
            logButton.clicked('log_a(b)', outputTextArea)
            equalsButton.clicked('=/CLEAR', outputTextArea)

    FPS.tick(60)  # 60 frames per second

    display.fill(black)

    # Draw author line
    # display.blit(authorText, authorRect)

    # Draw 3 major areas (output, operators, and number pad)
    outputArea.show(display, 'Output')
    operatorsArea.show(display, 'Operators')
    buttonsArea.show(display, 'Numbers')

    # Draw output text
    outputTextArea.show(display)

    ### Draw calculator buttons
    # Draw operator buttons
    plusButton.show(display)
    minusButton.show(display)
    multButton.show(display)
    divButton.show(display)
    expButton.show(display)
    factButton.show(display)
    sqrtButton.show(display)
    logButton.show(display)
    equalsButton.show(display)
    # Draw number and negative and point numbers
    zeroButton.show(display)
    oneButton.show(display)
    twoButton.show(display)
    threeButton.show(display)
    fourButton.show(display)
    fiveButton.show(display)
    sixButton.show(display)
    sevenButton.show(display)
    eightButton.show(display)
    nineButton.show(display)
    negativeButton.show(display)
    pointButton.show(display)