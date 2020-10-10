import argparse
import math
import sys


def parse_args():
    """Parse and return script arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, choices=['diff', 'annuity'])
    parser.add_argument('--payment', type=int)
    parser.add_argument('--principal', type=int)
    parser.add_argument('--periods', type=int)
    parser.add_argument('--interest', type=float)
    args = parser.parse_args()

    # count number of arguments
    arg_counter = 0
    for k, v in vars(args).items():
        if v:
            arg_counter += 1
        if type(v) == int and v < 0:
            print('Incorrect parameters')
            sys.exit()

    # interest is always needed
    # we need at least 4 arguments
    # diff type does not need payment argument
    if (args.type == 'diff' and args.payment) or not args.interest or arg_counter < 4:
        print('Incorrect parameters')
        sys.exit()
    return args


def nominal_interest(interest):
    """Calculate nominal interest"""
    return interest / 12 / 100


def mth_differentiated_payment(p, n, i, m):
    """Calculate differentiated payment for current month"""
    a = p * (m - 1)
    b = p - a / n
    c = p / n
    diff_payment = math.ceil(c + i * b)
    return diff_payment


def calc_diff_payment(p, n, interest):
    """Calculate differentiated payments"""

    i = nominal_interest(interest)
    total_payment = 0
    for month in range(1, n + 1):
        diff_payment = mth_differentiated_payment(p, n, i, month)
        total_payment += diff_payment
        print(f"Month {month}: payment is {diff_payment}")

    if total_payment > p:
        print(f"\nOverpayment = {total_payment - p}")


def calc_payment(p, n, i):
    """Calculate annuity payment"""

    a = i * pow(1 + i, n)
    b = pow(1 + i, n) - 1

    annuity = math.ceil(p * a / b)
    overpayment = annuity * n - p

    print(f"Your annuity payment = {annuity}!")
    print(f"Overpayment = {overpayment}")


def calc_principal(a, n, i):
    """Calculate loan principal"""

    b = i * pow(1 + i, n)
    c = pow(1 + i, n) - 1

    loan_principal = math.floor(a / (b / c))
    overpayment = a * n - loan_principal

    print(f"Your loan principal = {loan_principal}!")
    print(f"Overpayment = {overpayment}")


def calc_period(p, a, i):
    """Calculate loan repay period"""
    b = a - i * p

    nr_months = math.ceil(math.log((a / b), (1 + i)))

    years = nr_months // 12
    months = nr_months % 12

    if years == 0:
        print(f"It will take {months} months to repay this loan!")
    elif months == 0:
        print(f"It will take {years} years to repay this loan!")
    else:
        print(f"It will take {years} years and {months} months to repay this loan!")

    overpayment = a * nr_months - p
    print(f"Overpayment = {overpayment}")


def calc_ann_payment(params):
    """Calculate annuity payment"""
    i = nominal_interest(params.interest)

    if params.payment is None:
        calc_payment(params.principal, params.periods, i)
    elif params.principal is None:
        calc_principal(params.payment, params.periods, i)
    elif params.periods is None:
        calc_period(params.principal, params.payment, i)


if __name__ == "__main__":
    arguments = parse_args()

    if arguments.type == 'diff':
        calc_diff_payment(arguments.principal, arguments.periods, arguments.interest)
    else:
        calc_ann_payment(arguments)
