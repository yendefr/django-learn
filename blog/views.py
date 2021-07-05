from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {
                                                  'page': page,
                                                  'posts': posts,
                                                  'tag': tag,
                                                  })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    comments = post.comments.filter(active=True)
    comment = None

    tags = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=tags).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
                                                     'post': post,
                                                     'comments': comments,
                                                     'comment': comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} wants you to read some shitpost: {}'.format(cd['name'], post.title)
            message = 'Hey u, fkn jerk! I thk u somewhat stupid, so read some text bellow:\n{} - {}\n{}' \
                      .format(post_url, post.title, cd['comment'])
            send_mail(subject, message, '', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {
                                                    'post': post,
                                                    'form': form,
                                                    'sent': sent,
                                                    })
