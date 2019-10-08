import tcod


def identify(char):
    if char == '~':
        return ('Water', 'This is flowing water.', tcod.light_blue, tcod.darkest_blue)
    if char == '+':
        return ('Door', 'To open this door, walk on it.', tcod.white, tcod.black)
    if char == '0':
        return ('altar', 'The place where you were born.', tcod.white, tcod.black)
    if char == chr(25):
        return ('Stairway down', 'Walk on this tile to go down.', tcod.white, tcod.black)
    if char == ' ':
        return ('Floor', 'Strangely clean floor.', tcod.black, tcod.black)
    if char == '=':
        return ('Brige floor', 'Floor of a bridge.', tcod.white, tcod.black)
    if char == '"':
        return ('Grass', 'Healty green grass.', tcod.light_green, tcod.black)
    if char == 'O':
        return ('Tree trunk', 'If you were a dwarf, you could cut it.', tcod.dark_sepia, tcod.black)
    if char == '#':
        return ('Rough wall', 'This is a wall, looks like it was carved from stone', tcod.light_grey, tcod.black)
    elif char in ['Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù',]:
        return ('Wall', 'This is a wall, nothing special.', tcod.white, tcod.black)
    elif char in ['É', 'Í', 'Ë', '»', 'º', 'Ì', 'Î', '¹', 'È', 'Ê', '¼',]:
        return ('Wall', 'This is a wall, nothing special.', tcod.white, tcod.black)
    else:
        return ('', '', tcod.white, tcod.black)