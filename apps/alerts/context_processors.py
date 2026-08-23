from apps.alerts.models import Alert


def unread_alert_count(request):

    if not request.user.is_authenticated:
        return {
            "unread_alert_count": 0,
        }

    return {
        "unread_alert_count": Alert.objects.filter(
            user=request.user,
            is_read=False,
        ).count(),
    }
