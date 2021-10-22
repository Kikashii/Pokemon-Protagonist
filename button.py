def inPlay(x, y):
    x0, y0, x1, y1 = 20, 20, 90, 90
    return x < x1 and x > x0 and y > y0 and y < y1


def inPause(x, y):
    x0, y0, x1, y1 = 110, 20, 180, 90
    return x < x1 and x > x0 and y > y0 and y < y1