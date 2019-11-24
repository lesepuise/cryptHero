from .final import FinalLevel
from .random_level import RandomLevel
from .tutorial import TutorialLevel
from .debug import DebugLevel


levels = [
    # DebugLevel(),
    TutorialLevel(),
    RandomLevel(60, 60, 2),
    RandomLevel(60, 60, 3),
    RandomLevel(60, 60, 4),
    FinalLevel(),
]


def reset_levels():
    levels.clear()
    levels.append(TutorialLevel())
    levels.append(RandomLevel(60, 60, 2))
    levels.append(RandomLevel(60, 60, 3))
    levels.append(RandomLevel(60, 60, 4))
    levels.append(FinalLevel())
