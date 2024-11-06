from rest_framework import serializers

class LeavesStatsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['total_leaves_applied','total_leaves_pending','total_leaves_approved','total_leaves_rejected']