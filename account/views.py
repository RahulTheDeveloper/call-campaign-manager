from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Agent,Campaign,CampaignResult,User
from .serializers import AgentSerializer,CampaignSerializer,CampaignResultSerializer,UserRegistrationSerializer
from .paginations import MyPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrManager
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "role": user.role
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)    


class AgentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request):
        agents = Agent.objects.all().order_by('-updated')

        paginator = MyPagination()
        paginated = paginator.paginate_queryset(agents, request)

        serializer = AgentSerializer(paginated, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Agent created", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request, pk):
        agent = get_object_or_404(Agent, pk=pk)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    def put(self, request, pk):
        agent = get_object_or_404(Agent, pk=pk)
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Agent updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        agent = get_object_or_404(Agent, pk=pk)
        serializer = AgentSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Agent partially updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgentDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    def delete(self, request, pk):
        agent = get_object_or_404(Agent, pk=pk)
        agent.delete()
        return Response({"message": "Agent deleted"}, status=status.HTTP_204_NO_CONTENT)
    


#Campaign Views
class CampaignListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    def get(self, request):
        campaigns = Campaign.objects.all().order_by('-id')

        paginator = MyPagination()
        paginated = paginator.paginate_queryset(campaigns, request)

        serializer = CampaignSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Campaign created", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 # Campaign 
class CampaignRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data)

    def put(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Campaign updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Campaign partially updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignDeleteAPIView(APIView):
    def delete(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        campaign.delete()
        return Response({"message": "Campaign deleted"}, status=status.HTTP_204_NO_CONTENT)
    
# Campaign Result    
class CampaignResultListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = CampaignResult.objects.all().order_by('-id')

        paginator = MyPagination()
        paginated = paginator.paginate_queryset(results, request)

        serializer = CampaignResultSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CampaignResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Result created", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class CampaignResultRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    def get(self, request, pk):
        result = get_object_or_404(CampaignResult, pk=pk)
        serializer = CampaignResultSerializer(result)
        return Response(serializer.data)

    def put(self, request, pk):
        result = get_object_or_404(CampaignResult, pk=pk)
        serializer = CampaignResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Result updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        result = get_object_or_404(CampaignResult, pk=pk)
        serializer = CampaignResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Result partially updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignResultDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    def delete(self, request, pk):
        result = get_object_or_404(CampaignResult, pk=pk)
        result.delete()
        return Response({"message": "Result deleted"}, status=status.HTTP_204_NO_CONTENT)








