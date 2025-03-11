from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Department, Issue

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'department']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.role = validated_data.get('role', instance.role)
        instance.department = validated_data.get('department', instance.department)
        instance.save()

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return instance

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'created_by', 'assigned_to', 'department', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assuming the user and department are passed in the context
        user = self.context['request'].user
        department = self.context['department']

        issue = Issue.objects.create(
            created_by=user,
            department=department,
            **validated_data
        )
        return issue

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.save()
        return instance