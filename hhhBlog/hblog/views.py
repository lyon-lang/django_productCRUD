from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import serializers
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PostSerializer

# Create your views here.
# def home(request):
#     return render(request, "home.html", {})
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


# class Home(ListView):
    # model = Post
    # #template_name = "home.html"
    # ordering = ['-post_date']

    # def get_context_data(self, *args, **kwargs):
    #     cat_menu = Category.objects.all()
        
    #     context = super(Home, self).get_context_data(*args, **kwargs)
    #     context = {"results": list(cat_menu.values("id","name"))}
    #     # context["cat_menu"] = cat_menu
    #     return JsonResponse(context)
@api_view(['GET'])
def HomeView(request):
    post = Post.objects.all()
    data = {"results": list(post.values("author", "author_id", "body", "category", "comments", "header_image", "id", "likes", "post_date", "snippet", "title", "title_tag"))}
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProductList(request, *args, **kwargs):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ProductDetail(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def ProductCreate(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@api_view(['POST'])
def ProductUpdate(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def ProductDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()

    return Response('Product Succesfully Deleted!')


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    #return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})
    data = {"results": list(cat_menu_list.values("id", "name"))}
    return JsonResponse(data)

def SearchView(request):
    query = request.GET.get('search')
    if query is None:
        return render(request, 'search.html', {})

    else:
        results = Post.objects.filter(Q(title__icontains = query))
        return render(request, 'search.html', {'results':results})
 
    

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})
    



class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_details.html"

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes() 

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    #fields = "__all__"
    #fields = ('title', 'body')

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "add_comment.html"
    #fields = "__all__"

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('home')

class AddCategoryView(CreateView):
    model = Category
    template_name = "add_category.html"
    fields = "__all__"
    #fields = ('title', 'body')


class UpdatePostView(UpdateView):
    model = Post
    template_name = "update_post.html"
    form_class = EditForm
    #fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('home')


class AboutView(CreateView):
    model = Post
    # form_class = PostForm
    template_name = "about.html"
    fields = "__all__"
    #fields = ('title', 'body')

class WorkWithMeView(CreateView):
    model = Post
    # form_class = PostForm
    template_name = "work_with_me.html"
    fields = "__all__"
    #fields = ('title', 'body')

class ContactView(CreateView):
    model = Post
    # form_class = PostForm
    template_name = "contact.html"
    fields = "__all__"
    #fields = ('title', 'body')


