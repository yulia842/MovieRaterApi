from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Movie,Rating
from .serializers import MovieSerializer,RatingSerializer,UserSerializer
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
 

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True,methods=['POST'])
    def rate_movie(self, request,pk=None):
        if "stars" in request.data:
            
            movie = Movie.objects.get(id=pk)
            user = request.user
            stars = request.data['stars']
            print("user : ",user)

            try:
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars = stars
                rating.save()
                rate_serializer = RatingSerializer(rating,many=False)
                response = {"massage" : "Rating Updated", "resault" : rate_serializer.data}
                return Response(response,status=status.HTTP_200_OK)
            
            except:
                rating = Rating.objects.create(user=user,movie=movie,stars=stars)
                rate_serializer = RatingSerializer(rating,many=False)
                response = {"massage" : "Rating Created",  "resault" : rate_serializer.data}
                return Response(response,status=status.HTTP_200_OK)
           
        else:
            response = {"massage" : "STARS ARE REQUIRED!"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        response = {"massage" : "Can't UPDATE!"}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        response = {"massage" : "Can't CREATE!"}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


