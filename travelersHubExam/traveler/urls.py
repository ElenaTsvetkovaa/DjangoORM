from django.urls import path, include

from traveler import views

urlpatterns = [
    path('create/', views.CreateTravelerView.as_view(), name='create-traveler'),
    path('edit/', views.EditTravelerView.as_view(), name='edit-traveler'),
    path('details/', views.DetailsTravelerView.as_view(), name='details-traveler'),
    path('delete/', views.DeleteTravelerView.as_view(), name='delete-traveler'),

]
