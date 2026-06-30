from django.db import models


class MembershipRole(models.TextChoices):
    """
    Membership roles within a tenant.
    """

    OWNER = "OWNER", "Owner"
    ADMIN = "ADMIN", "Admin"
    TRAINER = "TRAINER", "Trainer"
    MEMBER = "MEMBER", "Member"
