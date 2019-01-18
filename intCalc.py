
import csv
import numpy as np
import sys


def lumpSumSav(principle, interest, term, extraPay):
    """ Calculate the amount you will pay on a loan in total  """
    minPayment = (interest * principle / 12.) / (1. - (1. + interest / 12.) ** (term * -12.)) + extraPay
    nLoans = len(term)
    mInt = 1 + interest/12

    def fun(pay):
        payments = np.zeros(nLoans)
        rem = principle - pay
        for i in range(len(rem)):
            while rem[i] > 0:
                payments[i] = payments[i] + min(minPayment[i], rem[i])
                rem[i] = rem[i] * mInt[i] - minPayment[i]
        return payments

    return fun


def monthSumSav(principle, interest, term, extraPay):
    """ Calculate the amount you will pay on a loan in total  """
    minPayment = ((interest * principle / 12.) / (1. - (1. + interest / 12.) ** (term * -12.))) + extraPay
    nLoans = len(term)
    mInt = 1 + interest/12

    def fun(extraErPay):
        nmp = minPayment + extraErPay
        payments = np.zeros(nLoans)
        rem = principle.copy()
        for i in range(len(rem)):
            while rem[i] > 0:
                payments[i] = payments[i] + min(nmp[i], rem[i])
                rem[i] = rem[i] * mInt[i] - nmp[i]
        return payments

    return fun


if __name__ == "__main__":

    # define principles etc.
    principle = np.array([])
    interest = np.array([])
    term = np.array([])
    extraPay = np.array([])

    lumpSum = int(sys.argv[2])
    paySum = int(sys.argv[3])
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        nLoans = 0
        for row in reader:
            if nLoans > 0:
                principle = np.append(principle, float(row[0]))
                term = np.append(term, float(row[1]))
                interest = np.append(interest, float(row[2])/100)
                extraPay = np.append(extraPay, float(row[3]))

            nLoans += 1

    paymentPlan = np.zeros(nLoans-1)
    monthPlan = np.zeros(nLoans-1)

    lumpFun = lumpSumSav(principle, interest, term, extraPay)
    monthFun = monthSumSav(principle, interest, term, extraPay)

    for i in range(paySum):
        currentCost = monthFun(monthPlan)
        nextCost = monthFun(monthPlan + 1)
        savings = currentCost - nextCost
        monthPlan[savings.argmax()] += 1

    # For every dollar, check how much you will save if you pay it into each loan, then place it into that loan
    for i in range(lumpSum):
        currentCost = lumpFun(paymentPlan)
        nextCost = lumpFun(paymentPlan + 1)
        savings = currentCost - nextCost
        paymentPlan[savings.argmax()] += 1

    print "your lumpsum payment should be split as: %s" % (repr(paymentPlan.tolist()),)
    print "your additional monthly payment should be split as: %s" % (repr(monthPlan.tolist()),)
