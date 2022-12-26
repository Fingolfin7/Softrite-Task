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
            print(f"\nDepth: {depth}")
            return guess, calculated_net

        """print(f"\nDepth: {depth}")
        print(f"Error: {error}")
        print(f"grad: {grad}")"""

        prev_guess = guess
        prev_error = error
        guess -= grad * rate
        # print(f"New Guess: {guess}")

        return adjust_guess(guess, desired_net, prev_error, prev_guess, depth + 1)

    # print(f"first_guess: {first_guess}")
    return adjust_guess(first_guess, net_income, 0, 0)


@time_func
def loop_gradient_descent(net_income):
    guess = net_income * 1.4
    prev_error = 0
    prev_guess = 0

    width = 0.5  # 0.5

    if net_income > 10000:  # for large numbers set rate and width to 1/10% of the nearest power of ten
        rate = 0.0001 * pow(10, find_power(net_income))
        width = rate
    else:
        rate = 0.7

    print(f"Width: {width}")

    calculated_net = get_net_from_gross(guess)
    error = abs(calculated_net - net_income)

    iteration = 0
    while error > width:
        calculated_net = get_net_from_gross(guess)
        error = abs(calculated_net - net_income)
        grad = (error - prev_error) / (guess - prev_guess)
        prev_guess = guess
        prev_error = error
        guess -= grad * rate

        iteration += 1

    print(f"Iteration: {iteration}, Error: {error}, New Guess: {guess}")
    return guess, calculated_net


@time_func
def loop_gradient_descent_annealed_lrate(net_income):
    guess = net_income * 1.4
    prev_error = 0
    prev_guess = 0

    width = 0.5  # 0.5
    calculated_net = get_net_from_gross(guess)
    error = abs(calculated_net - net_income)
    half_error_points = error

    if net_income > 10000:  # for large numbers set rate and width to 1/10% of the nearest power of ten
        rate = 0.1 * pow(10, find_power(net_income))
    else:
        rate = 0.7

    iteration = 0
    while error > width:
        calculated_net = get_net_from_gross(guess)
        error = abs(calculated_net - net_income)
        grad = (error - prev_error) / (guess - prev_guess)
        prev_guess = guess
        prev_error = error
        guess -= grad * rate

        if net_income > 10000 and error < 0.5 * half_error_points:  # when the error reduces
            # to half the previous point, half the learning rate
            half_error_points = error
            rate *= 0.5
            # print(f"Halved learning rate. New Rate: {rate}")
        iteration += 1

    print(f"Iteration: {iteration}, Error: {error}, New Guess: {guess}")
    return guess, calculated_net


@time_func
def get_gross_from_net_loop(net_income):
    guess = net_income * 1.4

    if net_income > 100000:  # for large numbers set rate and width to 1/10% of the nearest power of ten
        width = 0.001 * pow(10, find_power(net_income))
        rate = width  # 0.5
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

    print(f"Loop_counter: {loop_count}, Error: {abs(calculated_income - net_income)}, last guess: {guess}")
    return guess, calculated_income


if __name__ == "__main__":
    while True:
        try:
            net = float(input(">"))
            print(loop_gradient_descent(net))
            print()
            print(loop_gradient_descent_annealed_lrate(net))
            print()
            print(get_gross_from_net_loop(net))
            print()
            # print(get_gross_from_net_combined(net))
        finally:
            pass
