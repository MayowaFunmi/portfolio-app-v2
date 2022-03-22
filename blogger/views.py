from .forms import SearchForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
#from taggit.models import Tag
from .forms import PostForm, CommentForm, EmailPostForm
from .models import Post, Category, Comment, Tag


# create blog post
@login_required
def post_create(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    tags_objs = []
    if request.method == 'POST':
        user_category = request.POST['category']
        title = request.POST['title']
        post_image = None
        try:
            if request.FILES['post_image']:
                post_image = request.FILES['post_image']
        except:
            post_image = None
        body = request.POST['body']
        user_tags = request.POST['tags']

        tags_list = list(user_tags.split(','))
        for tag in tags_list:
            t, created = Tag.objects.get_or_create(title=tag)
            tags_objs.append(t)
        category = Category.objects.get(name=user_category)
        new_post = Post.objects.create(title=title, author=request.user, post_image=post_image, body=body)
        new_post.save()
        new_post.categories.add(category)
        new_post.tags.set(tags_objs)
        return HttpResponseRedirect('/blogger/')
    context = {
        'categories': categories,
        'tags': tags
    }

    return render(request, 'blogger/post/create.html', context)


def post_list(request):
    all_posts = Post.objects.all().order_by('-created')
    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        query = request.POST.get('q', None)
        submit_button = request.POST.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(body__icontains=query)
            all_results = Post.objects.filter(lookups).distinct()
            res_paginator = Paginator(all_results, 2)
            res_page = request.GET.get('page')
            results = res_paginator.get_page(res_page)
            context = {
                'query': query,
                'results': results,
                'submit_button': submit_button,
                'tags': tags,
                'categories': categories,
                'all_results': all_results
            }
            return render(request, 'blogger/post/search_results.html', context)

    context = {
        'posts': posts,
        'tags': tags,
        'categories': categories,
        'title': all_posts[0].title,
        'id': all_posts[0].id,
        'slug': all_posts[0].slug,
    }
    return render(request, 'blogger/post/list.html', context)


def post_detail_search(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    if request.method == 'POST':
        query = request.POST.get('q', None)
        submit_button = request.POST.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(body__icontains=query)
            all_results = Post.objects.filter(lookups).distinct()
            res_paginator = Paginator(all_results, 2)
            res_page = request.GET.get('page')
            results = res_paginator.get_page(res_page)
            context = {
                'query': query,
                'results': results,
                'submit_button': submit_button,
                'tags': tags,
                'categories': categories,
                'all_results': all_results
            }
            return render(request, 'blogger/post/search_results.html', context)

# list blog posts
'''def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    categories = Category.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogger/post/list.html', {
        'page': page,
        'posts': posts,
        'tag': tag,
        'categories': categories
    })
'''


# blog post details
def post_detail(request, id, year, month, day, posts):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post = get_object_or_404(Post, id=id, slug=posts,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    # List of active comments for this post
    comments = post.comments.filter(active=True).order_by('-created')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']

        new_comment = Comment(post=post, name=name, email=email, body=body)
        new_comment.save()
        return HttpResponseRedirect('/blogger/')

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blogger/post/detail.html', {
        'post': post,
        'comments': comments,
        'similar_posts': similar_posts,
        'liked': liked,
        'categories': categories,
        'tags': tags
    })


# edit blog post
@login_required
def post_edit(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        post_image = request.FILES['post_image']
        post.title = title
        post.body = body
        post.post_image = post_image
        post.save()
        return HttpResponseRedirect('/blogger/')
    return render(request, 'blogger/post/edit_post.html', {'post': post, 'id': id, 'slug': slug})


@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blogger/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:  # check whether the form is submitted,
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
            # search_vector = SearchVector('title', 'body', 'categories')
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B') + SearchVector('categories', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,
                                              rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank') # filter(search=search_query)
    return render(request, 'blogger/post/search.html', {'form': form,
                                                         'query': query,
                                                         'results': results})


def post_category(request, cats):
    posts = Post.objects.filter(categories__name=cats).order_by('-publish')
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'cats': cats,
        'category_posts': category_posts,
        'categories': categories,
        'tags': tags,
        'posts': posts
    }
    return render(request, "blogger/post/category_post_list.html", context)


def post_tags(request, tag):
    posts = Post.objects.filter(tags__title=tag).order_by('-publish')
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    tags_posts = paginator.get_page(page)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'tags': tags,
        'tags_posts': tags_posts,
        'categories': categories,
        'posts': posts,
        'tag': tag
    }

    return render(request, "blogger/post/tag_post_list.html", context)


#@login_required
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-publish'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blogger/post/category_post_list.html", context)


@login_required
def post_delete(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.method == 'POST':
        ask = request.POST['ask']
        if ask == 'Yes':
            post.delete()
            return redirect('/blogger/')
        elif ask == 'No':
            return redirect('/blogger/')
    return render(request, 'blogger/post/post_delete.html', {'post': post})


def like_view(request, id, year, month, day, posts):
    liked = False

    if request.method == 'POST':
        post = get_object_or_404(Post, id=request.POST.get('post_id'),
                                 slug=posts,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

    return HttpResponseRedirect(reverse('blogger:post_detail', args=[int(id), int(year), int(month), int(day), str(posts)]))