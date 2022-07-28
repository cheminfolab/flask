from django.db import models
from django.contrib.auth.models import Group, AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from locations.models import Building, Room, PhoneNumber


class WorkingGroup(models.Model):
    name = models.CharField(max_length=50)
    department = models.CharField(blank=True, max_length=200)
    institution = models.CharField(blank=True, max_length=200)
    address = models.ManyToManyField(Building, blank=True)

    def __str__(self):
        return f"{self.name} group"


# class Member(AbstractUser):
#     # academic title (legal/ordering)
#     working_group = models.ForeignKey(WorkingGroup, null=True, on_delete=models.PROTECT, related_name='members')
#     phones = models.ManyToManyField(PhoneNumber, blank=True, related_name='contacts')
#     rooms = models.ManyToManyField(Room, blank=True, related_name='team')
#
#     # # identifiers, links (ORCID, ResearchGate, etc.)
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name = "Member"

class Role(Group):
    class Meta:
        proxy = True
        # app_label = 'auth'
        verbose_name = _('Role')


class MemberManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        """
        Creates and saves a User with the given email, first name,
        last name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **other_fields):
        """
        Creates and saves a superuser with the given email password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            **other_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # academic title (legal/ordering)
    working_group = models.ForeignKey(WorkingGroup, null=True, on_delete=models.PROTECT, related_name='members')
    phones = models.ManyToManyField(PhoneNumber, blank=True, related_name='contacts')
    rooms = models.ManyToManyField(Room, blank=True, related_name='team')

    # # identifiers, links (ORCID, ResearchGate, etc.)

    # permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ManyToManyField(Role, blank=True, related_name='permitted_members')

    # important dates
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.last_name and self.first_name:
            return f"{self.last_name}, {self.first_name}"
        return self.email

    # def has_perm(self, perm, obj=None):
    #     """Does the user have a specific permission?"""
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     """Does the user have permissions to view the app `app_label`?"""
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # @property
    # def is_staff(self):
    #     """Is the user a member of staff?"""
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
