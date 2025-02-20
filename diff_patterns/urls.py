from django.urls import path

from .views import CreateKnownDiffAPIView, ListKnownDiffAPIView, \
    DetailKnownDiffAPIView, EditKnownDiffAPIView


urlpatterns = [
    path('list-known-diff/', ListKnownDiffAPIView.as_view(), name='list_known_diff'),
    path('create-known-diff/', CreateKnownDiffAPIView.as_view(), name='create_known_diff'),
    path('known-diff/<int:pk>/', DetailKnownDiffAPIView.as_view(), name='detail_known_diff'),
    path('edit-known-diff/<int:pk>/', EditKnownDiffAPIView.as_view(), name='edit_known_diff'),
    # path("delete-recipe/<int:pk>/", DeleteRecipeAPIView.as_view(), name="delete_recipe"),

]