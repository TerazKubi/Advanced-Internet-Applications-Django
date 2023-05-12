from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("genre/<int:genre_id>", views.view_genre, name="index"),
    # path("movie/<int:movie_id>", views.view_movie, name="index"),

    path("", views.IndexView.as_view(), name="index"),
    path("genre/<int:pk>", views.GenreView.as_view(), name="index"),
    path("movie/<int:pk>", views.MovieView.as_view(), name="index"),
    path("userRatings", views.user_ratings_request, name="user_ratings"),
    path("rateMovie/<int:pk>", views.rate_movie_request, name="rate_movie"),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),

]