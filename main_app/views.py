from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BandReadSerializer
        return BandWriteSerializer

    def get_queryset(self):
        user = self.request.query_params.get('id')
        return Band.objects.filter(members__in=[user])
        # return Band.objects.all()


class BandDetailViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BandReadSerializer
        return BandWriteSerializer

    def get_queryset(self):
        band_id = self.kwargs['pk']
        return Band.objects.filter(id=band_id)
    
    def destroy(self, request, *args, **kwargs):
        band_id = self.kwargs['pk']
        instance = Band.objects.get(id=band_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        band_id = self.kwargs['pk']
        instance = Band.objects.get(id=band_id)
        self.perform_update(instance)
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        band_id = self.kwargs['pk']
        instance = self.get_object()
        serializer = BandWriteSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes  = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SongReadSerializer
        return SongWriteSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            band_id = self.request.query_params.get('id')
            return Song.objects.filter(band__pk=band_id)
        band_id = self.kwargs['pk']
        return Song.objects.filter(band__pk=band_id)

class SongDetailViewSet(viewsets.ModelViewSet):
    serializer_class = SongReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        song_id = self.kwargs['pk']
        return Song.objects.filter(id=song_id)         


class RehearsalViewSet(viewsets.ModelViewSet):
    queryset = Rehearsal.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes  = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RehearsalReadSerializer
        return RehearsalWriteSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            band_id = self.request.query_params.get('id')
            return Rehearsal.objects.filter(band__pk=band_id).order_by('-date')
        band_id = self.kwargs['pk']
        return Rehearsal.objects.filter(band__pk=band_id)

class RehearsalDetailViewSet(viewsets.ModelViewSet):
    serializer_class = RehearsalReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        rehearsal_id = self.kwargs['pk']
        return Rehearsal.objects.filter(id=rehearsal_id)        
    

class LogoutView(APIView):
    def post(self, request):
        permission_classes = (permissions.IsAuthenticated)
        print(permission_classes)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
