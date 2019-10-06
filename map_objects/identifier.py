

class Description(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


def identify(char):
    if char == '~':
        return Description('Water', 'This is flowing water.')
    if char == '+':
        return Description('Door', 'To open this door, walk on it.')
    if char == '0':
        return Description('altar', 'The place where you were born.')
    if char == chr(25):
        return Description('Stairway down', 'Walk on this tile to go down.')
    if char == ' ':
        return Description('Floor', 'Strangely clean floor.')
    if char == '"':
        return Description('Grass', 'Healty green grass.')
    elif char in ['Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù',]:
        return Description('Water', 'This is flowing water.')
