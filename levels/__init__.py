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
