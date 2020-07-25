def newton_sqrt(number, iters=500):
    a = float(number)
    for i in range(iters):
        number = 0.5 * (number + a / number)
    return number
