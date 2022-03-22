import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from users.models import UserAccount as User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse('blogger:post_list')

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    post_image = models.ImageField(upload_to='blog_pics/%Y/%m/%d/', null=True, blank=True)
    body = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts')
    likes = models.ManyToManyField(User, related_name='blog_post')
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager

    class Meta:
        ordering = ('-publish',)

    def total_likes(self):
        return self.likes.count()

    def get_days(self):
        current = timezone.now()
        delta = current - self.created
        if delta.days <= 1:
            return f'{delta.days} day ago'
        else:
            return f'{delta.days} days ago'

    def get_absolute_url(self):
        return reverse('blogger:post_detail',
                       args=[self.id,
                             self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def get_absolute_url(self):
        return reverse('blogger:post_list')