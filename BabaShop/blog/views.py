from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post, Category, Comment, Tag
from .forms import AddCategoryForm, AddCommentForm, AddPostForm, AddTagForm, ChangePasswordForm,\
                ContactForm, EditPostForm, LoginForm, PostDeleteForm, RegisterForm,\
                CategoryDeleteForm, EditCategoryForm,TagDeleteForm, EditTagForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q

# Create your views here.


class MainPageView(ListView):
    model = Post
    template_name = "post/index.html"
    context_object_name = 'posts'
    queryset = Post.Published.all()


class PostListView(ListView):
    model = Post
    paginate_by = 20
    queryset = Post.Published.all()


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(post=context['post'])
        return context
    

def show_category_list(request):
    new_category = request.GET.get('category_box')
    form = AddCategoryForm(None or new_category)
    if form.is_valid():
        form.save()
        return redirect(reverse('category-list'))
    category_list = Category.objects.all()
    return render(request, 'post/category_list.html', {'categories': category_list, 'form_cat':form})


def each_category_posts(request, id):
    category_posts = Post.Published.filter(category__id = id)
    return render(request, 'post/category_posts.html', {'category_posts': category_posts, 'user':request.user})


def show_tag_list(request):
    new_tag = request.GET.get('tag_box')
    form = AddCategoryForm(None or new_tag)
    if form.is_valid():
        form.save()
        return redirect(reverse('tag-list'))
    tag_list = Tag.objects.all()
    return render(request, 'post/tag_list.html', {'tags': tag_list, 'form_tag': form})


def each_tag_posts(request, id):
    tag_posts = Post.Published.filter(tag__id = id)
    return render(request, 'post/tag_posts.html', {'tag_posts': tag_posts})


def login_site(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                try:
                    return redirect(next)
                except:        
                    id = request.user.id      
                    return redirect('user_posts_url')
            else :
                print('not found user') #add messege
            return render(request, 'forms/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'forms/login.html', {'form': form})


def logout_site(request):
    logout(request)
    return redirect('login_url')


def Register_site(request):
    form = RegisterForm(None or request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            return redirect('login_url')

    return render(request, 'forms/register.html', {'form':form})


@login_required(login_url='login_url')
def change_password(request):
    form = ChangePasswordForm()
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data.get('old_password')):
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                return redirect('login_url')

    return render(request, 'forms/change_password.html', {'form': form})


def search_site(request):
    if request.method == "GET":
        search = request.GET.get('search_box')
        posts = Post.Published.filter(Q(title__icontains=search) |
                                    Q(descrption__icontains=search))
    return render(request, 'post/search.html', {'posts': posts})


@login_required(login_url='login_url')
def add_category(request):
    form = AddCategoryForm(None or request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('category-list'))

    return render(request,'forms/add_category.html',{'form_cat':form})


@login_required(login_url='login_url')
def add_tag(request):
    form = AddTagForm(None or request.POST)
    if form.is_valid():
        form.save()
        # messages.add_message(request, messages.ERROR, f'Tag added successfully',extra_tags="danger")
        return redirect(reverse('tag-list'))

    return render(request,'forms/add_tag.html',{'form_tag':form})


@login_required(login_url='login_url')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryDeleteForm()
    if request.method == "POST":
        category.delete()
        return redirect(reverse('category-list'))

    return render(request,'forms/delete_category.html',{'form':form,'category':category})


@login_required(login_url='login_url')
def edit_category(request,id):
    category = get_object_or_404(Category, id=id)
    form = EditCategoryForm(instance=category)
    if request.method == "POST":
        form = EditCategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse('category-list'))

    return render(request, 'forms/edit_category.html', {'form':form,'category':category})


@login_required(login_url='login_url')
def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    form = TagDeleteForm()
    if request.method == "POST":
        tag.delete()
        return redirect(reverse('tag-list'))

    return render(request,'forms/delete_tag.html',{'form':form,'tag':tag})


@login_required(login_url='login_url')
def edit_tag(request,id):
    tag = get_object_or_404(Tag, id=id)
    form = EditTagForm(instance=tag)
    if request.method == "POST":
        form = EditTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect(reverse('tag-list'))

    return render(request, 'forms/edit_tag.html', {'form':form,'tag':tag})


@login_required(login_url='login_url')
def each_user_posts(request):
    user_posts = Post.objects.filter(author__id=request.user.id)
    return render(request, 'post/user_posts.html', {'user_posts': user_posts, 'user': request.user.username})


@login_required(login_url='login_url')
def add_post(request):
    form = AddPostForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        form.save()
        return redirect(reverse('user_posts_url'))

    return render(request,'forms/add_post.html',{'form_post':form, 'user':request.user})


@login_required(login_url='login_url')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostDeleteForm()
    if request.method == "POST" and request.user.id == post.author.id:
        post.delete()
        return redirect(reverse('user_posts_url'))

    return render(request,'forms/delete_post.html',{'form':form,'post':post})


@login_required(login_url='login_url')
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = EditPostForm(instance=post)
    if request.method == "POST" and request.user.id == post.author.id:
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('user_posts_url'))

    return render(request, 'forms/edit_post.html', {'form':form,'post':post})


def add_comment(request, slug):
    if request.user.id:
        post = Post.objects.get(slug=slug)
        print(post.like)
        comment = post.post_comment.all()
        tag = Tag.objects.filter(post__slug=slug)
        category = Category.objects.filter(post__slug=slug)
        form = AddCommentForm(request.POST, initial={})
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.post = post
            form.save()
            return redirect(f'../add_comment/{slug}')
    else:
        return redirect(f'../post-detail/{slug}')

    return render(request,'forms/add_comment.html',{
        'post':post, 'comment_list':comment, 'tags':tag,
        'categories':category, 'form_com':form, 'user':request.user})


def post_like(request, slug):
    print(slug, 'soifowejfvoijwejfosdjfosdjfo-----')
    if request.method == 'POST':
        if request.user.id:
            post = Post.objects.get(slug=slug)
            post.like += 1
            # if form.is_valid():
            return redirect(reverse(f'../add_comment/{slug}'))
    # else:
    #     return redirect(f'../post-detail/{slug}')

    # return render(request,'forms/add_comment.html',{
    #     'post':post, 'comment_list':comment, 'form_com':form, 'user':request.user})


def contact_site(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
                'name': form.cleaned_data['name'], 
                'email': form.cleaned_data['email_address'], 
                'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'hadiomidm@gmail.com', ['hadiomidm@gmail.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("index")
      
	form = ContactForm()
	return render(request, "post/contact.html", {'form':form})
