from rest_framework import serializers
from .models import Agent, Campaign, CampaignResult,User


class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "role"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)   # password hash
        user.save()
        return user


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class CampaignResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignResult
        fields = '__all__'
