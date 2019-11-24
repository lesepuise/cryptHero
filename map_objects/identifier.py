import tcod


def identify(char):
    if char == ord('~'):
        return ('Water', 'This is flowing water.', tcod.light_blue, tcod.darkest_blue)
    if char == ord('+'):
        return ('Door', 'To open this door, walk on it.', tcod.white, tcod.black)
    if char == ord('0'):
        return ('altar', 'The place where you were born.', tcod.white, tcod.black)
    if char == 25:
        return ('Stairway down', 'Walk on this tile to go down.', tcod.white, tcod.black)
    if char in [ord(' ')]:
        return ('Floor', 'Strangely clean floor.', tcod.black, tcod.black)
    if char in [250]:
        return ('Floor', 'Strangely clean floor.', tcod.black, tcod.darkest_gray)
    if char == tcod.constants.CHAR_BLOCK1:
        return (
            'Detailed floor', 'That floor has been detailed by an artist.\n'
            'You can see a wonderful sculptur of a tempest at sea.',\
            tcod.black,
            tcod.darkest_gray
        )
    if char == ord('='):
        return ('Brige floor', 'Floor of a bridge.', tcod.white, tcod.black)
    if char == ord('"'):
        return ('Grass', 'Healty green grass.', tcod.light_green, tcod.black)
    if char == ord('O'):
        return ('Tree trunk', 'If you were a dwarf, you could cut it.', tcod.dark_sepia, tcod.black)
    if char == ord('#'):
        return ('Rough wall', 'This is a wall, looks like it was carved from stone', tcod.light_grey, tcod.black)
    elif char in [ord('Ú'), ord('Ä'), ord('Â'), ord('¿'), ord('³'), ord('Ã'), ord('Å'), ord('´'), ord('À'), ord('Á'), ord('Ù'),]:
        return ('Wall', 'This is a wall, nothing special.', tcod.white, tcod.black)
    elif char in [ord('É'), ord('Í'), ord('Ë'), ord('»'), ord('º'), ord('Ì'), ord('Î'), ord('¹'), ord('È'), ord('Ê'), ord('¼'),]:
        return ('Wall', 'This is a wall, nothing special.', tcod.white, tcod.black)
    else:
        return ('', '', tcod.white, tcod.black)