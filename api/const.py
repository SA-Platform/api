from enum import Enum


class AnnouncementsCategory(str, Enum):
    INTERNSHIP = "internship"
    EVENT = "event"
    WORKSHOP = "workshop"
    COMPETITION = "competition"
    OTHER = "other"
