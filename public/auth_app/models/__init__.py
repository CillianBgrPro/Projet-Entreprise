from .UserModel import User
from .StudentModel import Student
from .ProfessorModel import Professor
from .AdminModel import Admin
from .GroupModel import Group
from .ClinicalCaseModel import ClinicalCase
from .TrainingModel import Training
from .StudentPerformanceModel import StudentPerformance
from .TicketModel import Ticket, TicketReply

__all__ = [
    'User',
    'Student',
    'Professor',
    'Admin',
    'Group',
    'ClinicalCase',
    'Training',
    'StudentPerformance',
    'Ticket',
    'TicketReply'
]
