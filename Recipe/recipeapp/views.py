from django.shortcuts import render
from rest_framework import generics,viewsets
from .models import recipe,review
from .serializers import RecipeSerializer,ReviewSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


# class RecipeList(generics.ListCreateAPIView):
#       queryset = recipe.objects.all()
#       serializer_class = RecipeSerializer
#
# class ReviewList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = review.objects.all()
#     serializer_class = ReviewSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = recipe.objects.all()
    serializer_class = RecipeSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = review.objects.all()
    serializer_class = ReviewSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class user_logout(APIView):
    # permission_classes = [IsAuthenticated,]
    def get(self, request):
        self.request.user.auth_token.delete()
        return Response({'msg': 'Logout Successfully'}, status=status.HTTP_200_OK)

class createreview(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        r = ReviewSerializer(data=request.data)
        if r.is_valid():
            r.save()
            return Response(r.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class detailreview(APIView):
    # permission_classes = [IsAuthenticated]
    def get_object(self,pk):
       try:
            return recipe.objects.get(pk=pk)
       except:
            raise Http404
    def get(self,request,pk):
        r=self.get_object(pk)
        rev=review.objects.filter(recipe_name=r)
        revd=ReviewSerializer(rev,many=True)
        return Response(revd.data)

class cuisinefilter(APIView):
    def get(self,request):
        query=self.request.query_params.get('cuisine')
        recipes=recipe.objects.filter(cuisine=query)
        r=RecipeSerializer(recipes,many=True)
        return Response(r.data)
class mealfilter(APIView):
    def get(self, request):
        query = self.request.query_params.get('meal_type')
        recipes = recipe.objects.filter(meal_type=query)
        r = RecipeSerializer(recipes, many=True)
        return Response(r.data)







