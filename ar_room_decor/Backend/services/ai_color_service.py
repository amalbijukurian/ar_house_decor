def detect_color(r, g, b):
    if r > 200 and g > 200 and b > 200:
        return "white"
    elif r > g and r > b:
        return "red"
    elif g > r and g > b:
        return "green"
    elif b > r and b > g:
        return "blue"
    else:
        return "neutral"