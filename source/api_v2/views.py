from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api_v2.serializers import QuotesSerializer
from webapp.models import Quote, QUOTE_APPROVED


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class QuoteViewSet(ModelViewSet):
    queryset = Quote.objects.none()
    serializer_class = QuotesSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Quote.objects.all()
        return Quote.objects.all()

    def get_permissions(self):
        if self.action not in ['update', 'partial_update', 'destroy']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['post'], detail=True)
    def rate_up(self, request, pk=None):
        quote = self.get_object()
        quote.rating += 1
        quote.save()
        return Response({'id': quote.pk, 'rating': quote.rating})

    @action(methods=['post'], detail=True)
    def rate_down(self, request, pk=None):
        quote = self.get_object()
        quote.rating -= 1
        quote.save()
        return Response({'id': quote.pk, 'rating': quote.rating})


# здесь может понадобится точка входа для выдачи кодов и названий статусов,
# чтобы передавать их на клиент с сервера, а не копировать в код клиента.
# (по заданию не обязательно, но желательно).
