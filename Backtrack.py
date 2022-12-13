import re

def BacktrackFull(IP: str) -> tuple:
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
