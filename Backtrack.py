import re

def BacktrackFull(IP: str) -> tuple:
    """Backtracks whole program

    Decompiled compiled string to program and formats it to match a pattern (every line contains only one command)

    Args:
        IP (str): compiled program

    Returns:
         tuple: string containing backtracked program and list of numbers that point to lines where states are defined

    """
    if not IP:
        return "", []

    states = IP.split('/')
    result = "<Entry point>\n\n"
    nums = []
    c = 2

    for i in range(len(states)):
        nums.append(c)
        result += f"{i} : State {{" + "\n"
        temp = re.compile(r"((?:[^.:]|:[^:]*:)+)").split(states[i])
        for s in temp:
            if s:
                result += BacktrackCommand(s)
        result += "}\n\n"
        c = result.count('\n')
    return result, nums


def BacktrackCommand(command: str) -> str:
    """Backtracks one command

    Decompiles compiled command

    Args:
        command (str): compiled command

    Returns:
         str: decompiled command

    """
    if command[0] == 'R':
        return "    >;\n"
    if command[0] == 'L':
        return "    <;\n"
    if command[0] == 'W':
        return f"    write({command[1]});"+"\n"
    if command[0] == 'C':
        return f"    tostate({command[1]});"+"\n"
    if command[0] == 'I':
        result = f"    if({command[1]}) {{"+"\n"
        for s in command[3:-1].split('.'):
            if s:
                result += f"    {BacktrackCommand(s)}"
        return result + "    };\n"
    if command[0] == 'N':
        result = f"    if(!{command[1]}) {{"+"\n"
        for s in command[3:-1].split('.'):
            if s:
                result += f"    {BacktrackCommand(s)}"
        return result + "    };\n"
    if command[0] == 'H':
        return "    halt;\n"
    return ""
