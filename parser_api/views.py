from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from parser import run_parser
from parser_api.models import Product
from parser_api.serializers import ProductSerializer, ProductExactFieldSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page"
    max_page_size = 100


@api_view(http_method_names=["POST"])
@csrf_exempt
def index(request):
    run_parser()
    return Response({'message': 'successfully run parser'})


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'pk'


class ProductExactFieldViewSet(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductExactFieldSerializer
    all_fields = (
        "title",
        "description",
        "calories",
        "fats",
        "carbs",
        "proteins",
        "unsaturated_fats",
        "sugar",
        "salts",
        "portion"
    )

    def get_serializer(self, *args, **kwargs):
        field = self.kwargs["field"]
        if field:
            kwargs['fields'] = (field,)
        return super().get_serializer(*args, **kwargs)
