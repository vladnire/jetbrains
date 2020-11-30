import sys

sys.setrecursionlimit(10000)


def match_char(reg: str, char: str) -> bool:
    """Check one char regex"""
    return reg in ("", ".") or reg == char


def matching(regex, string):
    """Check if strings match"""

    if regex:
        if string:
            # Meta char and no escapes
            if len(regex) > 1 and regex[1] in '+*?' and regex[0] != '\\':
                return stage_5(regex, string)

            else:
                # Remove the escape if present at the beginning
                if regex[0] == '\\':
                    return matching(regex[1:], string)

                elif match_char(regex[0], string[0]):
                    regex = regex[1:]
                    string = string[1:]
                    return matching(regex, string)

                return False
        else:
            # If we reached the end of string and we have ending regex
            if regex[0] == "$":
                return True

            return False

    return True


def stage_3(regex, string):
    """Check strings of different lengths"""

    if match_char(regex, string):
        return True
    else:
        if not string:
            return False
        else:
            if matching(regex, string):
                return True
            # Adjust the length of the string
            else:
                string = string[1:]
                return stage_3(regex, string)


def stage_4(regex, string):
    """Start and end check"""

    if "^" in regex:
        regex = regex[1:]
        return matching(regex, string)
    # If there is an '$' or not
    else:
        return stage_3(regex, string)


def stage_5(regex, string):
    """Regex meta char check"""

    if regex[1] == "?":
        return what(regex, string)
    elif regex[1] == "*":
        return mult(regex, string)
    elif regex[1] == "+":
        return plus(regex, string)


def what(regex, string):
    """Implement regex ? functionality"""

    if match_char(regex[0], string[0]):
        regex = regex[2:]
        string = string[1:]
        return matching(regex, string)

    # If character matches 0 times
    regex = regex[2:]
    return matching(regex, string)


def mult(regex, string):
    """Implement regex * functionality"""

    if match_char(regex[0], string[0]):
        # If character matches once
        if len(string) == 1:
            regex = regex[2:]
            return matching(regex, string)
        # If character matches multiple times
        else:
            string = string[1:]
            return matching(regex, string)

    # If character matches 0 times
    regex = regex[2:]
    return matching(regex, string)


def plus(regex, string):
    """Implement regex + functionality"""

    if match_char(regex[0], string[0]):
        # If character matches once
        if len(string) == 1:
            regex = regex[2:]
            return matching(regex, string)
        else:
            if match_char(string[0], string[1]):
                string = string[1:]
                return matching(regex, string)
            else:
                regex = regex[2:]
                string = string[1:]
                return matching(regex, string)

    return False


if __name__ == '__main__':

    print(stage_4(*input().split("|")))
