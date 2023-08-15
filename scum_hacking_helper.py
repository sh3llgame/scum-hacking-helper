import itertools
import sys
import io
from tabulate import tabulate

debug = False


def apply_operation(value, operation):
    if operation[0] == '+':
        return value + operation[1]
    elif operation[0] == '-':
        return value - operation[1]
    elif operation[0] == '*':
        return value * operation[1]
    elif operation[0] == '/':
        return value / operation[1]
    else:
        raise ValueError(f"Unsupported operation: {operation[0]}")


def generate_enable_states():
    return list(itertools.product([0, 1], repeat=8))


def test_combinations(desired_output, enable_states, operands, input_value):
    valid_states = []
    for state in enable_states:
        current_value = input_value
        for i in range(8):
            if state[i]:
                current_value = apply_operation(current_value, operands[i])
        if abs(current_value - desired_output) < 1e-6:
            valid_states.append(state)
    return valid_states


def solve(input_value, output_a, output_b, operands_a, operands_b):
    enable_states = generate_enable_states()


    valid_states_a = test_combinations(output_a, enable_states, operands_a, input_value)
    print(f"\nFound {len(valid_states_a)} valid states for line a.")
    results = test_combinations(output_b, valid_states_a, operands_b, input_value)
    print(f"Found {len(results)} possible results by narrowing down.")

    '''
    if len(results) > 0:
        if len(results) > 1:
            print("WARNING: Multiple results found. Returning the first one.")
            for result in results:
                print(result)
        return results[0]
    '''

    valid_states_b = test_combinations(output_b, enable_states, operands_b, input_value)
    print(f"Found {len(valid_states_b)} valid states for line b.")

    # Find the intersection of the two sets
    # print("Finding the intersection of the two sets.")
    for state_a in valid_states_a:
        for state_b in valid_states_b:
            if state_a == state_b:
                print(f"Found solution: {state_b}")
                results.append(state_a)

    if len(results) > 0:
        if len(results) > 1:
            for result in results:
                print(result)
        return results[0]

    return results[0]


def parse_operand_string(operand_string):
    operands = []
    parts = operand_string.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            operands.append(('+', 0))  # Default to an operation that doesn't affect the value
        else:
            try:
                op = part[0]
                val = float(part[1:])
                operands.append((op, val))
            except (ValueError, IndexError):
                print("Invalid operand format. Using default operand.")
                operands.append(('+', 0))
    return operands


def validate_operand_string(operand_string):
    parts = operand_string.split(',')
    for part in parts:
        part = part.strip()
        if part:
            if part[0] not in "+-*/":
                return False
            try:
                float(part[1:])
            except ValueError:
                return False
    return True


'''
def display_table(header, table_data):
    print("{:<10} {:<30} {:<30}".format(header[0], header[1], header[2]))
    print("-" * 75)
    for row in table_data:
        print("{:<10} {:<30} {:<30}".format(row[0], row[1], row[2]))
    print("-" * 75)
    print("{:<10} {:<30} {:<30}".format("Required:", "output_a", "output_b"))
'''


def main():
    while True:
        try:
            input_line = input("Enter input, output_a, output_b (comma-separated without spaces): ")
            input_value, output_a, output_b = map(float, input_line.split(','))

            while True:
                operands_a_str = input("Enter operand string for line a (comma-separated without spaces): ")
                if validate_operand_string(operands_a_str):
                    break
                print("Invalid operand string. Please enter a valid operand string.")

            while True:
                operands_b_str = input("Enter operand string for line b (comma-separated without spaces): ")
                if validate_operand_string(operands_b_str):
                    break
                print("Invalid operand string. Please enter a valid operand string.")

            operands_a = parse_operand_string(operands_a_str)
            operands_b = parse_operand_string(operands_b_str)

            if debug:
                # Debug: print all what was entered
                print("Using the following values:")
                print("Input: ", input_value)
                print("Output A: ", output_a)
                print("Output B: ", output_b)
                print("Operands A: ", operands_a_str, " || ", operands_a)
                print("Operands B: ", operands_b_str, " || ", operands_b)


            result = solve(input_value, output_a, output_b, operands_a, operands_b)

            if result:
                enabled_operations = result
                table_header = ["On/Off", "Line A", "Line B"]
                table_data = []

                for i in range(0, 8):
                    table_data.append(
                        ("X" if enabled_operations[i] is 1 else " ", str(f"{operands_a[i][0]} {int(operands_a[i][1])}"), str(f"{operands_b[i][0]} {int(operands_b[i][1])}"))
                    )
                table_data.append(("Required:", str(int(output_a)), str(int(output_b))))

                # print the table
                print(tabulate(table_data, headers=table_header, tablefmt="fancy_grid", stralign="center"))

            else:
                print("No solution found.")

        except ValueError:
            print("Invalid input. Please enter valid numerical values.")

        choice = input("Do you want to try again? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting the program.")
            break


if __name__ == "__main__":
    main()







