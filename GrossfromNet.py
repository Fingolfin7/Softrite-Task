import os
import random
from NetfromGross import get_net_from_gross
from time_func import time_func

def find_power(num, base=10):
    power = 0
    while num > base:
        num /= base
        power += 1
    return power


def get_gross_from_net_recursive(net_income):
    first_guess = net_income * 1.4

    rate = 0.9

    def adjust_guess(guess: float, desired_net, prev_error, prev_guess, depth=0):
        calculated_net = get_net_from_gross(guess)
        error = abs(calculated_net - desired_net)
        grad = (error - prev_error) / (guess - prev_guess)

        if depth > 700 or (error - prev_error) > 0 and depth > 0:
            return round(guess), round(calculated_net)

        """print(f"\nDepth: {depth}")
        print(f"Error: {error}")
        print(f"grad: {grad}")"""

        if grad < 0:
            prev_guess = guess
            prev_error = error
            guess += grad * rate
            # print(f"New Guess: {guess}")
        elif grad > 0:
            prev_guess = guess
            prev_error = error
            guess -= grad * rate
            # print(f"New Guess: {guess}")

        return adjust_guess(guess, desired_net, prev_error, prev_guess, depth + 1)

    # print(f"first_guess: {first_guess}")
    return adjust_guess(first_guess, net_income, 0, 0)


def get_gross_from_net_loop(net_income):
    guess = net_income * 1.4

    if net_income > 100000:  # for large numbers set rate and width to 1/10% of the nearest power of ten
        rate = 0.001 * pow(10, find_power(net_income))
        width = rate  # 0.5
    else:
        rate = 10
        width = 10  # 0.5

    calculated_income = get_net_from_gross(guess)

    loop_count = 0
    while abs(calculated_income - net_income) > width:
        # rate *= 1
        # width *= 1 # originally 10

        if calculated_income < net_income:
            guess += rate
        else:
            guess -= rate

        # print(f"Loop_counter: {loop_count}, New Guess: {guess}, "
        #      f"Calculated Income: {calculated_income}, width: {width}")
        calculated_income = get_net_from_gross(guess)
        loop_count += 1

    # print(f"Loop_counter: {loop_count}, last guess: {guess}")
    return round(guess), round(calculated_income)


def get_gross_from_net_combined(net_income, first_guess=None):
    # first_guess = net_income * 1.4
    if not first_guess:
        first_guess, _ = get_gross_from_net_loop(net_income)

    rate = 0.9

    def adjust_guess(guess: float, desired_net, prev_error, prev_guess, depth=0):
        calculated_net = get_net_from_gross(guess)
        error = abs(calculated_net - desired_net)
        grad = (error - prev_error) / (guess - prev_guess)

        if depth > 700 or (error - prev_error) > 0 and depth > 0:
            return round(guess), round(calculated_net)

        """print(f"\nDepth: {depth}")
        print(f"Error: {error}")
        print(f"grad: {grad}")"""

        if grad < 0:
            prev_guess = guess
            prev_error = error
            guess += grad * rate
            # print(f"New Guess: {guess}")
        elif grad > 0:
            prev_guess = guess
            prev_error = error
            guess -= grad * rate
            # print(f"New Guess: {guess}")

        return adjust_guess(guess, desired_net, prev_error, prev_guess, depth + 1)

    # print(f"first_guess: {first_guess}")
    return adjust_guess(first_guess, net_income, 0, 0)


@time_func
def main():
    count = 0
    combined_count = 0
    combined_error = 0
    recursive_count = 0
    recursive_error = 0
    loop_count = 0
    loop_error = 0
    max_net = int(input("Enter max net income value: "))

    while count < 300:
        print("", end=f"\rIteration {count}/300")
        desired_net_income = random.randint(0, max_net)

        gross_rcs, cd_income_rcs = get_gross_from_net_recursive(desired_net_income)
        recursive_error += abs(cd_income_rcs - desired_net_income)

        gross_loop, cd_income_loop = get_gross_from_net_loop(desired_net_income)
        loop_error += abs(cd_income_loop - desired_net_income)

        gross_combined, cd_income_combined = get_gross_from_net_combined(desired_net_income, gross_loop)
        combined_error += abs(cd_income_combined - desired_net_income)

        """print(f"Gross Figure Estimation (recursive): {gross_rcs}")
        print(f"Net income: {cd_income_rcs}\n")
        print(f"Gross Figure Estimation (loop): {gross_loop}")
        print(f"Net income: {cd_income_loop}\n")
        print(f"Gross Figure Estimation (combined): {gross_combined}")
        print(f"Net income: {cd_income_combined}")

        print()"""

        if abs(cd_income_rcs - desired_net_income) <= abs(cd_income_loop - desired_net_income) \
                and abs(cd_income_rcs - desired_net_income) <= abs(cd_income_combined - desired_net_income):
            # print(f"Best Gross Figure Estimation (recursive): {gross_rcs}")
            # print(f"Net income: {cd_income_rcs}")
            recursive_count += 1
        if abs(cd_income_loop - desired_net_income) <= abs(cd_income_rcs - desired_net_income) \
                and abs(cd_income_loop - desired_net_income) <= abs(cd_income_combined - desired_net_income):
            # print(f"Best Gross Figure Estimation (loop): {gross_loop}")
            # print(f"Net income: {cd_income_loop}")
            loop_count += 1
        if abs(cd_income_combined - desired_net_income) <= abs(cd_income_rcs - desired_net_income) \
                and abs(cd_income_combined - desired_net_income) <= abs(cd_income_loop - desired_net_income):
            # print(f"Best Gross Figure Estimation (combined): {gross_combined}")
            # print(f"Net income: {cd_income_combined}")
            combined_count += 1
        count += 1

    # os.system("cls")
    print("\nFinal Counts (300 iterations):")

    print(f"Recursive: {recursive_count} ({(recursive_count / 300) * 100}%)"
          f"\nAverage Error: {round(recursive_error / 300, 2)}\n")
    print(f"Loop: {loop_count} ({(loop_count / 300) * 100}%)"
          f"\nAverage Error: {round(loop_error / 300, 2)}\n")
    print(f"Combined: {combined_count} ({(combined_count / 300) * 100}%)"
          f"\nAverage Error: {round(combined_error / 300, 2)}\n")


if __name__ == "__main__":
    while True:
        main()
        """try:
            net = float(input(">"))
            # print(get_gross_from_net_combined(net))
            print(get_gross_from_net_loop(net))
            # print(get_gross_from_net_recursive(net))
        finally:
            pass"""
