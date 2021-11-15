from django import forms
from django.http import request,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import ShareForm,CommentForm,SubscribeForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count, query
from django.db.models import Q


# Create your views here.
def post_list(request,tag_slug=None):
    tag = None
    
    object_list=Post.published.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])
    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)

    return render(request,"blog/posts/list.html",{'tag':tag,'posts':posts,'page':page}) 

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    post_tag_ids=post.tag.values_list('id',flat=True)
    similar_posts=Post.published.filter(tag__in=post_tag_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags','-publish')[:4]
    
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid:
            # cd=form.cleaned_data
            nc=form.save(commit=False)
            nc.post=post
            nc.save()
    else:
        form=CommentForm()
    return render(request,'blog/posts/detail.html',{'post':post,'comments': comments,'form':form,'similar_posts':similar_posts})


def share_post(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=ShareForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comment']}"
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:    
        form=ShareForm()
    return render(request,"blog/share.html",{'post':post,'form':form,'sent':sent})

def subscribe(request):
    sent=False
    if request.method=='POST':
        form=SubscribeForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject = f"{cd['email']} subscribed "
                      
            message = f"I want to subscribe to your newsletter" 
                      
            send_mail(subject, message, 'admin@myblog.com',['admin@myblog.com'])
            sent = True
    else:    
        form=SubscribeForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def search_post(request):
#     form=SearchForm()
#     query=None
#     result=[]
#     if query in request.Get:
#         form=SearchForm(request.Get)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published
    
#             results = Post.published.filter(Q(title__icontains=query) | Q(body__icontains=query))
#     return render(request,'blog/post/search.html',{'form': form,'query': query,'results': results})
