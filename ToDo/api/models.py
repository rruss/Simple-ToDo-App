from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin


class MyUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(validators=[validate_email], unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_logged = models.BooleanField(default=False)
    token = models.CharField(max_length=100, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @classmethod
    def logged(cls, new):
        cls.is_logged = new

    def __str__(self):
        return f'{self.email}'


class TaskManager(models.Manager):
    def for_user_order_by_name(self, user):
        return self.filter(created_by=user).order_by('name')


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    execution_date = models.DateField(null=True, blank=True)
    is_executed = models.BooleanField(default=False)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    objects = TaskManager()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ('name', 'created_by')

    def _str_(self):
        return '{}: {}'.format(self.id, self.name)
