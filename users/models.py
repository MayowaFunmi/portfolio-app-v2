from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, username, **extra_fields):
        if first_name is None:
            raise ValueError('Users should have First Name')
        if last_name is None:
            raise ValueError('Users should have Last Name')
        if username is None:
            raise ValueError('Users should have Username')
        if email is None:
            raise ValueError('Users should have an Email Address')
        if password is None:
            raise ValueError('Password cannot be empty')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, username, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')
        return self._create_user(email, first_name, last_name, username, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name="Email")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    username = models.CharField(max_length=50, verbose_name='Username', null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserAccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Country(models.Model):
    alpha_2 = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f' {self.name} - ({self.country.name})'


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    #country = CountryField(multiple=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True, default='/avatar.png')
    interest = models.CharField(max_length=300, help_text='Indicate what contents will you like to write/read about on this blog.', null=True, blank=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Project(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    description = models.TextField(max_length=1000)
    features = models.TextField(max_length=10000, null=True, blank=True)
    github_link = models.URLField()
    demo_link = models.URLField()
    image = models.ImageField(upload_to="projects/%Y/%m/%d/")
    show = models.BooleanField(default=False)
    date_published = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.project}'


class ContactMe(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.full_name}'


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)