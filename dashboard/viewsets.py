from rest_framework import viewsets,status
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from dashboard.models import Certificates
from dashboard.serializers import CertificationSerializer


    
class CertificatesViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Certificates.objects.all()
    serializer_class = CertificationSerializer
    

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
    @action(detail=True, methods=['patch'],name="update_verified")
    def certificates_verify(self, request, pk=None):
        object = self.get_object()
        object.is_verified=True
        serializer=self.serializer_class(object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)