from datetime import datetime
from paye_calcs import calculate_annual_paye


def get_net_from_gross(gross_income):
    today = datetime.today()

    remaining_periods = 2  # (12 - today.month) is how to find the remaining periods. For now assume 2.
    forecasted_extra = gross_income * remaining_periods

    # salary_ytd = float(input("Enter employee salary YTD: "))
    salary_ytd = 25000
    expected_annual_gross = forecasted_extra + salary_ytd

    # annualised_deductibles = float(input("Enter annualised deductibles: "))
    # ytd_bonus_used = float(input("Enter YTD Bonus: "))

    annualised_deductibles = 3900
    ytd_bonus_used = 700

    annual_taxable_income = expected_annual_gross - (annualised_deductibles + ytd_bonus_used)
    # print(f"\nAnnual Taxable Income -> {annual_taxable_income}")

    annual_paye_due = calculate_annual_paye(annual_taxable_income)
    # print(f"Annual PAYE Due -> {annual_paye_due}")

    # annualised_tax_credits = float(input("Enter annualised tax credits: "))
    annualised_tax_credits = 1400
    # annualised_tax_credits
    expected_paye_plus_aids = annual_paye_due * 1.03
    net_regular_paye_left = expected_paye_plus_aids - annualised_tax_credits

    # ytd_paye = float(input("Enter YTD PAYE: "))
    ytd_paye = 4500
    regular_paye_left = net_regular_paye_left - ytd_paye
    regular_paye_this_period = regular_paye_left / remaining_periods
    # print(f"Regular PAYE this period -> {regular_paye_this_period}")

    net_salary = gross_income - regular_paye_this_period
    # print(f"Net Salary -> {net_salary}")
    return net_salary


if __name__ == "__main__":
    # salary = float(input("Enter employee salary: "))
    salary = 2000
    # allowance_benefits = float(input("Enter employee allowance + benefits: "))
    allowance_benefits = 300
    gross_income = salary + allowance_benefits
    net_salary = round(get_net_from_gross(gross_income), 2)
    print(f"Net Salary -> {net_salary}")
