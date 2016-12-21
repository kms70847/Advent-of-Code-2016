def abba(s):
    for i in range(len(s)-3):
        a,b,c,d = s[i:i+4]
        if d == a != b == c: return True
    return False

def tlp(s):
    sections = s.replace("[","]").split("]")
    outside_sections = sections[::2]
    inside_sections = sections[1::2]
    return any(abba(section) for section in outside_sections) and not any(abba(section) for section in inside_sections)

def iter_abas(s):
    for i in range(len(s)-2):
        a,b,c = s[i:i+3]
        if c == a != b:
            yield a+b+c

def ssl(s):
    sections = s.replace("[","]").split("]")
    outside_sections = sections[::2]
    inside_sections = sections[1::2]
    abas = {aba for section in outside_sections for aba in iter_abas(section)}
    babs = {aba for section in inside_sections for aba in iter_abas(section)}
    invert = lambda s: s[1]+s[0]+s[1]
    return bool(abas.intersection(map(invert, babs)))

with open("input") as file:
    data = list(file)

print(sum(1 for row in data if tlp(row)))
print(sum(1 for row in data if ssl(row)))