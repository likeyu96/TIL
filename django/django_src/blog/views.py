# django에서 제공하는 import
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

# 내가 만든 import
from .models import Post
from .forms import PostModelForm, PostForm

def post_list(request):
    name = 'Django'
    # return HttpResponse('''<h2>Post List</h2>
    #                         <p>{name}</p>
    #                         <p>{content}</p>'''.format(name=name, content = request.user))
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts' : posts})

# Post 상세조회
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

# post 등록
def post_new(request):
    if request.method == 'POST': # save버튼을 눌렀을때,
        form = PostForm(request.POST)
        if form.is_valid(): # 유효성 검사
            print(form.cleaned_data)
            post = Post.objects.create(author=User.objects.get(username = request.user),
                                       published_date=timezone.now(),
                                       title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text']) # save 필요없다
            # post = form.save(commit=False)
            # post.author = User.objects.get(username = request.user) # ver3에서는 이렇게 해주어야한다.
            # post.published_date = timezone.now()
            # post.save()
            return redirect('post_detail', pk=post.pk) # 저장하자 마자 post_detail로 바로 분기

    else : # http method == 'GET'
        form = PostForm() # 등록 form을 보여준다
    return render(request, 'blog/post_edit.html', {'form': form} )

# Post 수정
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST': # save버튼을 누름
        # 수정을 처리하는 부분
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username = request.user)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else : # 연필 버튼을 누름
        # 수정하기 전에 데이터를 읽어오는 부분
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# post 삭제
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete() # 삭제하기
    return redirect('post_list') # 지우자 마자 글 list로 이동