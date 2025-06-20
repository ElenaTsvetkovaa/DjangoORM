from django.urls import path, include

from furryFunniesExam.posts import views

urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create-post'),
    path('<int:id>/', include([
        path('edit/', views.EditPostView.as_view(), name='edit-post'),
        path('details/', views.DetailsPostView.as_view(), name='details-post'),
        path('delete/', views.DeletePostView.as_view(), name='delete-post'),
    ]))
]
