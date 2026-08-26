LINE = {
    "s": {"ul": "┌", "ur": "┐", "ll": "└", "lr": "┘", "v": "│", "b": "─"},
    "d": {"ul": "╔", "ur": "╗", "ll": "╚", "lr": "╝", "v": "║", "b": "═"},
}


def draw_line(style, size, text=""):
    char = LINE[style]

    match size:
        case "s":
            size_int = 20
        case "m":
            size_int = 25
        case "l":
            size_int = 30

    size_int -= len(text)

    return_text = char["b"] * 4 + text + char["b"] * size_int

    return return_text


def draw_box(style, text, width=None):
    char = LINE[style]

    width = 8 + len(text)

    b = char["b"] * width
    return_text = (
        char["ul"]
        + b
        + char["ur"]
        + "\n"
        + char["v"]
        + "    "
        + str(text)
        + "    "
        + char["v"]
        + "\n"
        + char["ll"]
        + b
        + char["lr"]
    )

    return return_text
