from django.urls import path

from .views import CreateKnownDiffAPIView, ListKnownDiffAPIView


urlpatterns = [
    path('list-known-diff/', ListKnownDiffAPIView.as_view(), name='list_known_diff'),
    path('create-known-diff/', CreateKnownDiffAPIView.as_view(), name='create_known_diff'),
    # path('recipe/<int:pk>/', DetailRecipeAPIView.as_view(), name='detail_recipe'),
    # path('edit-recipe/<int:pk>/', EditRecipeAPIView.as_view(), name='edit_recipe'),
    # path("delete-recipe/<int:pk>/", DeleteRecipeAPIView.as_view(), name="delete_recipe"),

]