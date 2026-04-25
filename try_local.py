# This is a test for local agentic stack with LM Studio, Qwen2.5 coder 14b, Continue plugin, VS Code


# Try creating a simple python calculator for basic arithmetic


def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    else:
        return x / y

def power(x, y):
    return x ** y

def logarithm(x, base=10):
    import math
    if x <= 0 or (base == 1 and x != 1) or base <= 0:
        return "Error: Invalid input for logarithm"
    else:
        return math.log(x, base)

# Example usage
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Addition:", add(num1, num2))
print("Subtraction:", subtract(num1, num2))
print("Multiplication:", multiply(num1, num2))
print("Division:", divide(num1, num2))
print("Power:", power(num1, num2))
print("Logarithm (base 10):", logarithm(num1))