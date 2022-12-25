
def test_calculate_annual_paye(taxable_income: float):
    """
    :param taxable_income:
    :return: total expected PAYE

    >>> test_calculate_annual_paye(35000)
    10030.0
    >>> test_calculate_annual_paye(25000)
    6530.0
    >>> test_calculate_annual_paye(47000)
    14780.0
    >>> test_calculate_annual_paye(92000)
    32780.0
    >>> test_calculate_annual_paye(52439.5)
    16955.8
    >>> test_calculate_annual_paye(17439.89)
    4211.97
    >>> test_calculate_annual_paye(1013.12)
    0
    """

    brackets = [0.2, 0.25, 0.3, 0.35, 0.4]  # don't include the bottom bracket
    bracket_widths = [2400, 8400, 12000, 12000] # don't include the first and top brackets

    def calc_total_bracket_tax(index):
        if index == 0:  # base case
            return bracket_widths[index] * brackets[index]

        return (bracket_widths[index] * brackets[index]) + calc_total_bracket_tax(index - 1)

    if taxable_income >= 36000:
        return round(((taxable_income - 36000) * brackets[4]) + calc_total_bracket_tax(3), 2)
    elif 24000 <= taxable_income < 36000:
        return round(((taxable_income - 24000) * brackets[3]) + calc_total_bracket_tax(2), 2)
    elif 12000 <= taxable_income < 24000:
        return round(((taxable_income - 12000) * brackets[2]) + calc_total_bracket_tax(1), 2)
    elif 3600 <= taxable_income < 12000:
        return round(((taxable_income - 3600) * brackets[1]) + calc_total_bracket_tax(0), 2)
    elif 1200 <= taxable_income < 3600:
        return round((taxable_income - 1200) * brackets[0], 2)
    elif taxable_income < 1200:
        return 0


def calculate_annual_paye(taxable_income: float):
    brackets = [0.2, 0.25, 0.3, 0.35, 0.4]  # don't include the bottom bracket
    bracket_widths = [2400, 8400, 12000, 12000]  # don't include the first and top brackets

    def calc_total_bracket_tax(index):
        if index == 0:  # base case
            return bracket_widths[index] * brackets[index]

        return (bracket_widths[index] * brackets[index]) + calc_total_bracket_tax(index - 1)

    if taxable_income >= 36000:
        return ((taxable_income - 36000) * brackets[4]) + calc_total_bracket_tax(3)
    elif 24000 <= taxable_income < 36000:
        return ((taxable_income - 24000) * brackets[3]) + calc_total_bracket_tax(2)
    elif 12000 <= taxable_income < 24000:
        return ((taxable_income - 12000) * brackets[2]) + calc_total_bracket_tax(1)
    elif 3600 <= taxable_income < 12000:
        return ((taxable_income - 3600) * brackets[1]) + calc_total_bracket_tax(0)
    elif 1200 <= taxable_income < 3600:
        return (taxable_income - 1200) * brackets[0]
    elif taxable_income < 1200:
        return 0


if __name__ == "__main__":
    paye = calculate_annual_paye(float(input("Enter in annual taxable income: ").replace(",", "")))
    print(paye)
