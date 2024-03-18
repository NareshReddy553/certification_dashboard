from rest_framework import viewsets,status

from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from dashboard.models import Certificates
# from dashboard.serializers import CertificationSerializer
from config.pagination import StandardResultsSetPagination
from dashboard.serializers import CertificationSerializer


    
class CertificatesViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Certificates.objects.all()
    serializer_class = CertificationSerializer    
    pagination_class = StandardResultsSetPagination
    
    def apply_dynamic_filters(self, queryset, **kwargs):
        """
        Apply dynamic filters to the given queryset based on provided kwargs.
        """
        for param, value in kwargs.items():
            if hasattr(Certificates, param):
                filter_kwargs = {param: value}
                queryset = queryset.filter(**filter_kwargs)
        return queryset 
    def paginated_response(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def non_paginated_response(self, queryset, filter_params):
        queryset = self.apply_dynamic_filters(queryset, **filter_params)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())

        # Retrieve filter values from request parameters
        filter_params = request.query_params.dict()
        
        # Check if the parameter to disable pagination is provided
        disable_pagination = filter_params.pop('disable_pagination', None)

        if disable_pagination:
            return self.non_paginated_response(queryset, filter_params)
        else:
            return self.paginated_response(queryset)
    

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
    
      
    
        
    @action(detail=True, methods=['patch'],name="update_verified")
    def certificates_verify(self, request, pk=None):
        object = self.get_object()
        object.is_verified=True
        serializer=self.serializer_class(object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
