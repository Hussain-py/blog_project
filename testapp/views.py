from django.shortcuts import render,get_object_or_404
from testapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger
from taggit.models import Tag
# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()

    #tags related posts
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    # 3 post per PageNotAnInteger
    paginator=Paginator(post_list,3)
    #current page number
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    return render(request,'testapp/post_list.html',{'post_list':post_list,'tag':tag})


from testapp.forms import CommentForm

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day,)

    #Coments form & comments realted to post 'related_name=comments'
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False) #get comment
            new_comment.post=post  #assing post value associte with comment
            new_comment.save()  #save comments
            csubmit=True
    #if it is not post required to display form
    else:
        form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})


from django.core.mail import send_mail
from testapp.forms import EmailSendForm

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status="published")

    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            subject='{} ({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            #post url
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message="Read Post At:\n{}\n\n{}'S Comments:\n{}".format(post_url,cd['name'],cd['comments'])

            send_mail(subject,message,'clickin@blog.com',[cd['to']]) #email content
            sent=True
    else:
        form=EmailSendForm()

    return render(request,'testapp/sharebymail.html',{'form':form ,'post':post,'sent':sent})
