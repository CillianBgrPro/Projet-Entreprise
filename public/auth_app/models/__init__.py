from .UserModel import User
from .StudentModel import Student
from .ProfessorModel import Professor
from .GroupModel import Group
from .ClinicalCaseModel import ClinicalCase
from .TrainingModel import Training
from .StudentPerformanceModel import StudentPerformance
from .TicketModel import Ticket, TicketReply
from .StartingSituationModel import StartingSituation
from .ItemsEDNModel import ItemsEDN

__all__ = [
    'User',
    'Student',
    'Professor',
    'Group',
    'ClinicalCase',
    'ItemsEDN',
    'Training',
    'StudentPerformance',
    'Ticket',
    'TicketReply',
    'StartingSituation'
]
