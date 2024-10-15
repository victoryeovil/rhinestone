from auditlog.registry import auditlog

from app.models.billing import Invoice
from app.models.contacts import Applicant, Associate, Attorney, Consultant, Contact, CostCenter, Inventor, Licensee, Licensor, OtherProvider, Paralegal
from app.models.inventions import InventionDisclosure
from app.models.users import User


# Registering all models for audit logging
auditlog.register(Invoice)
auditlog.register(InventionDisclosure)
auditlog.register(User)
auditlog.register(Contact)
auditlog.register(Inventor)
auditlog.register(Applicant)
auditlog.register(Licensor)
auditlog.register(Licensee)
auditlog.register(Consultant)
auditlog.register(Associate)
auditlog.register(Paralegal)
auditlog.register(Attorney)
auditlog.register(OtherProvider)
auditlog.register(CostCenter)
