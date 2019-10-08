from .final import FinalLevel
from .random_level import RandomLevel
from .tutorial import TutorialLevel


levels = [
    TutorialLevel(),
    RandomLevel(65, 60, 2),
    RandomLevel(65, 60, 3),
    RandomLevel(65, 60, 4),
    FinalLevel(),
]


def reset_levels():
    levels.clear()
    levels.append(TutorialLevel())
    levels.append(RandomLevel(65, 60, 2))
    levels.append(RandomLevel(65, 60, 3))
    levels.append(RandomLevel(65, 60, 4))
    levels.append(FinalLevel())
