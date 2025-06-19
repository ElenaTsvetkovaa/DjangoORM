from django.urls import path, include

from travelersHubExam.trips import views

urlpatterns = [
    path('create/', views.CreateTripView.as_view(), name='create-trip'),
    path('<int:pk>/', include([
        path('details/', views.DetailsTripView.as_view(), name='details-trip'),
        path('edit/', views.EditTripView.as_view(), name='edit-trip'),
        path('delete/', views.DeleteTripView.as_view(), name='delete-trip'),
    ]))
]



