from .final import FinalLevel
from .random_level import RandomLevel
from .tutorial import TutorialLevel


levels = [
    TutorialLevel(),
    RandomLevel(),
    RandomLevel(),
    RandomLevel(),
    FinalLevel(),
]


def reset_levels():
    levels.clear()
    levels.append(TutorialLevel())
    levels.append(RandomLevel())
    levels.append(RandomLevel())
    levels.append(RandomLevel())
    levels.append(FinalLevel())
