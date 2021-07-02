from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comments = post.comments.filter(active=True)
    comment = None
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
