import os
import random
from NetfromGross import get_net_from_gross
from time_func import time_func
import matplotlib.pyplot as plt
from datetime import datetime


def find_power(num, base=10):
    power = 0
    while num > base:
        num /= base
        power += 1
    return power


def draw_chart(points: list, label_name: str, second_points=None, second_label=None):
    print(points[-1])
    plt.plot([itr for _, itr in points], [data for data, _ in points], label=label_name)

    if second_points:
        plt.plot([itr for _, itr in second_points], [data for data, _ in second_points], label=second_label)
        plt.title(f"Changes in {label_name} and {second_label}")
    else:
        plt.title(f"Changes in {label_name}")
        plt.ylabel(label_name)

    plt.xlabel("Iteration")
    plt.legend()
    plt.ticklabel_format(style="plain")

    if not os.path.isdir("Plots/"):
        os.mkdir("Plots")

    if second_points:
        plt.savefig(f"Plots/{label_name} and {second_label}({datetime.now().strftime('%m-%d-%Y')}).jpg")
    else:
        plt.savefig(f"Plots/{label_name}({datetime.now().strftime('%m-%d-%Y')}).jpg")

    plt.clf()


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
    chart_lrate_points = []
    chart_error_points = []
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
    chart_error_points.append((error, iteration))
    chart_lrate_points.append((rate, iteration))

    while error > width:
        calculated_net = get_net_from_gross(guess)
        error = abs(calculated_net - net_income)
        grad = (error - prev_error) / (guess - prev_guess)
        prev_guess = guess
        prev_error = error
        guess -= grad * rate

        chart_error_points.append((error, iteration))

        if net_income > 10000 and error < 0.5 * half_error_points:  # when the error reduces
            # to half the previous point, half the learning rate
            half_error_points = error
            rate *= 0.5
            chart_lrate_points.append((rate, iteration))
            # print(f"Halved learning rate. New Rate: {rate}")
        iteration += 1

    print(f"Iteration: {iteration}, Error: {error}, New Guess: {guess}")

    draw_chart(chart_error_points, "Error")
    draw_chart(chart_lrate_points, "Learning Rate")
    draw_chart(chart_error_points, "Error", chart_lrate_points, "Learning Rate")

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
