from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

# from .permissions import IsAuthorOrReadOnly
# from .serializers import (PostSerializer, GroupSerializer,
#                          CommentSerializer, FollowSerializer)

from .serializers import CommentSerializer, ReviewSerializer

from reviews.models import Review, Comment, Title, User


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=User.objects.get(pk=1))
