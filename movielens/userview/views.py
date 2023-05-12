from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.template import loader

from .forms import NewUserForm, RateForm
from .models import Movie, Genre, Rating

from django.views import generic

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages




def index(request : HttpRequest):
    movies = Movie.objects.order_by('-title')
    template = loader.get_template('userview/index.html')
    context = {
        'movies' : movies
    }
    return HttpResponse(template.render(context,request))






def register_request(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render (request=request, template_name="userview/register.html",context={"register_form":form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Login fail.")
            
        else:
            messages.error(request, "Login fail. Invalid form")


    form = AuthenticationForm()
    return render(request=request, template_name="userview/login.html", context={"login_form":form})


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    
    return redirect('/login')


def user_ratings_request(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    ratings = Rating.objects.filter(user=request.user)

    template = loader.get_template('userview/user_ratings.html')
    context = {
        'ratings' : ratings
    }
    return HttpResponse(template.render(context,request))


def rate_movie_request(request : HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    pk = kwargs['pk']
    movie = Movie.objects.get(pk=pk)

    if request.method == "POST":
        form = RateForm(request.POST)

        if form.is_valid():
            rate = form.cleaned_data.get('rate')
            rating = Rating(value=rate, movie=movie, user=request.user)
            rating.save()
            return redirect(f"/movie/{pk}")
        


    form = RateForm()
    return render(request=request, template_name="userview/rateMovie.html", context={"rate_form" : form, "movie" : movie})
    




class IndexView(generic.ListView):
    template_name = 'userview/index.html'
    context_object_name = 'movies'
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.order_by('-title')

class MovieView(generic.DetailView):
    model = Movie
    template_name = 'userview/movie.html'

class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre.html'

