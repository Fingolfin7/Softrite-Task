import threading
from tkinter import *
from tkinter import messagebox
from datetime import datetime
# from PIL import ImageTk, Image
from time_func import time_func


class SalaryCalculatorGUI:
    def __init__(self, tk_root: Tk):
        self.salary = DoubleVar()
        self.benefits = DoubleVar()
        self.estimatedGrossIncome = DoubleVar()
        self.desiredNetSalary = DoubleVar()

        self.remainingPeriods = IntVar()
        self.remainingPeriods.set((12 - datetime.today().month) + 1)

        # if your in month 10, you've paid 9 months worth in salaries
        self.salaryYTD = DoubleVar()
        # self.salaryYTD.set(
        #    (self.salary.get() * datetime.today().month) - self.salary.get()
        # )

        self.annualisedDeductibles = DoubleVar()
        self.bonusUsedYTD = DoubleVar()
        self.annualisedTaxCredits = DoubleVar()
        self.payeYTD = DoubleVar()
        self.netSalary = DoubleVar()
        self.payeThisPeriod = DoubleVar()

        self.brackets = [0.2, 0.25, 0.3, 0.35, 0.4]  # don't include the bottom bracket
        self.bracket_widths = [2400, 8400, 12000, 12000]  # don't include the first and top brackets

        self.__aidsPercentage = 1.03

        # GUI
        # tk_root.resizable(width=False, height=False)
        self.frame = Frame(tk_root)
        self.UserInputSection = LabelFrame(self.frame)
        self.NetSection = LabelFrame(self.frame)
        self.GrossSection = LabelFrame(self.frame)

        # user input section
        Label(self.UserInputSection, text="Salary").grid(row=0, column=0, sticky=W, pady=2)
        self.salaryEntry = Entry(self.UserInputSection, textvariable=self.salary)
        self.salaryEntry.grid(row=0, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Benefits").grid(row=1, column=0, sticky=W, pady=2)
        self.benefitsEntry = Entry(self.UserInputSection, textvariable=self.benefits)
        self.benefitsEntry.grid(row=1, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Periods(months)").grid(row=2, column=0, sticky=W, pady=2)
        self.periodsEntry = Entry(self.UserInputSection, textvariable=self.remainingPeriods)
        self.periodsEntry.grid(row=2, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Salary YTD").grid(row=3, column=0, sticky=W, pady=2)
        self.salaryYTDEntry = Entry(self.UserInputSection, textvariable=self.salaryYTD)
        self.salaryYTDEntry.grid(row=3, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Annual Deductibles").grid(row=4, column=0, sticky=W, pady=2)
        self.deductiblesEntry = Entry(self.UserInputSection, textvariable=self.annualisedDeductibles)
        self.deductiblesEntry.grid(row=4, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Bonus Used YTD").grid(row=5, column=0, sticky=W, pady=2)
        self.bonusEntry = Entry(self.UserInputSection, textvariable=self.bonusUsedYTD)
        self.bonusEntry.grid(row=5, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="Tax Credits").grid(row=6, column=0, sticky=W, pady=2)
        self.creditsEntry = Entry(self.UserInputSection, textvariable=self.annualisedTaxCredits)
        self.creditsEntry.grid(row=6, column=1, sticky=W, padx=4)

        Label(self.UserInputSection, text="PAYE YTD").grid(row=7, column=0, sticky=W, pady=2)
        self.payeYTDEntry = Entry(self.UserInputSection, textvariable=self.payeYTD)
        self.payeYTDEntry.grid(row=7, column=1, sticky=W, padx=4)

        # net calc section
        Label(self.NetSection, text="PAYE this period").grid(row=0, column=0, sticky=W, pady=4)
        Label(self.NetSection, textvariable=self.payeThisPeriod, width=18,
              background="grey", fg="white").grid(row=0, column=1, sticky=W, pady=4)

        Label(self.NetSection, text="Net Salary", font="Calibri 10 bold").grid(row=1, column=0, sticky=W, pady=4)
        Label(self.NetSection, textvariable=self.netSalary, width=18,
              background="dark blue", fg="white", font="Calibri 10 bold").grid(row=1, column=1, sticky=W, pady=4)

        self.netButton = Button(self.NetSection, text="Calculate Net Salary")
        self.netButton.bind("<Button-1>", self.handle_netButton)
        self.netButton.grid(row=2, column=0, sticky=W, pady=4)

        # gross calc section
        Label(self.GrossSection, text="Target Net Salary").grid(row=0, column=0, sticky=W, pady=4)
        self.creditsEntry = Entry(self.GrossSection, textvariable=self.desiredNetSalary)
        self.creditsEntry.grid(row=0, column=1, sticky=W, pady=4)

        Label(self.GrossSection, text="Estimated Gross", font="Calibri 10 bold").grid(row=1, column=0, sticky=W, pady=4)
        Label(self.GrossSection, textvariable=self.estimatedGrossIncome, width=16,
              background="dark blue", fg="white", font="Calibri 10 bold").grid(row=1, column=1, sticky=W, pady=4)

        self.grossButton = Button(self.GrossSection, text="Calculate Gross Salary")
        self.grossButton.bind("<Button-1>", self.handle_grossButton)
        self.grossButton.grid(row=2, column=0, sticky=W, pady=4)

        self.UserInputSection.pack(side=TOP, fill=BOTH)
        self.NetSection.pack(side=TOP, fill=BOTH)
        self.GrossSection.pack(side=TOP, fill=BOTH)
        self.frame.pack(pady=2, padx=2)

    def __calculateAnnualPAYE(self, taxable_income: float):

        def calc_total_bracket_tax(index):
            if index == 0:  # base case
                return self.bracket_widths[index] * self.brackets[index]
            return (self.bracket_widths[index] * self.brackets[index]) + calc_total_bracket_tax(index - 1)

        if taxable_income >= 36000:
            return ((taxable_income - 36000) * self.brackets[4]) + calc_total_bracket_tax(3)
        elif 24000 <= taxable_income < 36000:
            return ((taxable_income - 24000) * self.brackets[3]) + calc_total_bracket_tax(2)
        elif 12000 <= taxable_income < 24000:
            return ((taxable_income - 12000) * self.brackets[2]) + calc_total_bracket_tax(1)
        elif 3600 <= taxable_income < 12000:
            return ((taxable_income - 3600) * self.brackets[1]) + calc_total_bracket_tax(0)
        elif 1200 <= taxable_income < 3600:
            return (taxable_income - 1200) * self.brackets[0]
        elif taxable_income < 1200:
            return 0

    def calculateNetSalary(self, gross_value):
        forecasted_extra = gross_value * float(self.remainingPeriods.get())
        expected_annual_gross = forecasted_extra + float(self.salaryYTD.get())
        annual_taxable_income = expected_annual_gross - (float(self.annualisedDeductibles.get()) +
                                                         float(self.bonusUsedYTD.get()))

        annual_paye_due = self.__calculateAnnualPAYE(annual_taxable_income)
        expected_paye_plus_aids = annual_paye_due * self.__aidsPercentage
        net_regular_paye_left = expected_paye_plus_aids - float(self.annualisedTaxCredits.get())
        regular_paye_left = net_regular_paye_left - float(self.payeYTD.get())
        regular_paye_this_period = regular_paye_left / int(self.remainingPeriods.get())

        netSalary = gross_value - regular_paye_this_period
        return netSalary, regular_paye_this_period

    def handle_netButton(self, event=None):
        def netButton_thread():
            try:
                gross_value = float(self.salary.get()) + float(self.benefits.get())
                netSalary, paye_this_period = self.calculateNetSalary(gross_value)
                self.netSalary.set(round(netSalary, 2))
                self.payeThisPeriod.set(round(paye_this_period, 2))
            except ArithmeticError as e:
                messagebox.showwarning(
                    f"Error!",
                    f"Please enter in field data.\n{e}"
                )

        netThread = threading.Thread(target=netButton_thread)
        netThread.start()

    def __gradient_descent(self, desiredNetSalary):
        guess = desiredNetSalary * (1 + self.brackets[-1])
        width = 0.5
        prev_error = 0
        prev_guess = 0

        calculated_net, _ = self.calculateNetSalary(guess)
        error = abs(calculated_net - desiredNetSalary)
        half_error_points = error

        if desiredNetSalary > 10000:  # for large numbers set rate and width to 1% of the nearest power of ten
            rate = 0.1 * pow(10, find_power(desiredNetSalary))
        else:
            rate = 0.7

        iteration = 0
        while error > width:
            calculated_net, _ = self.calculateNetSalary(guess)
            error = abs(calculated_net - desiredNetSalary)

            grad = (error - prev_error) / (guess - prev_guess)
            prev_guess = guess
            prev_error = error
            guess -= grad * rate

            if desiredNetSalary >= 10000 and error < 0.5 * half_error_points:  # when the error reduces
                # to half the previous point, half the learning rate
                half_error_points = error
                rate *= 0.5
        iteration += 1
        print(f"Iteration: {iteration}, Error: {error}, New Guess: {guess}")

        return guess, calculated_net

    @time_func
    def calculateGross(self, desiredNetIncome):
        if desiredNetIncome == 0:
            raise AttributeError

        gross, cd_income = self.__gradient_descent(desiredNetIncome)

        return gross

    def handle_grossButton(self, event=None):
        def grossButton_thread():
            try:
                self.estimatedGrossIncome.set(0.0)  # clear while calculations run
                net_income_value = float(self.desiredNetSalary.get())
                calculated_gross = self.calculateGross(net_income_value)
                self.estimatedGrossIncome.set(round(calculated_gross, 2))
            except ArithmeticError as e:
                messagebox.showwarning(
                    f"Error!",
                    f"Please enter in field data.\n{e}"
                )
            except AttributeError:
                pass

        grossThread = threading.Thread(target=grossButton_thread)
        grossThread.start()


def find_power(num, base=10):
    power = 0
    while num > base:
        num /= base
        power += 1
    return power


def main():
    root = Tk()
    root.title('Softrite Salary Calculator')
    root.resizable(width=False, height=False)
    # icon = ImageTk.PhotoImage(Image.open("icon/logo.jpeg"))
    # root.iconphoto(True, icon)

    SalaryCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
