from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ...services.log_activity import log_event
from .serializers import ActivityIn, ActivityBulkIn

@extend_schema(
    summary="Create one activity (requires login)",
    tags=["Activities"],
    request=ActivityIn,
    responses={201: OpenApiResponse(description="Created, returns id")}
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def create_activity(request):
    # support JWT principal via request.user or fallback to session
    customer_id = None
    if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
        customer_id = getattr(request.user, 'id', None)
    if customer_id is None:
        customer_id = request.session.get("customer_id")
    if customer_id is None:
        return Response({"detail": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ActivityIn(data=request.data)
    serializer.is_valid(raise_exception=True)

    # ensure session exists / has a key
    if hasattr(request, "session") and request.session.session_key is None:
        request.session.create()

    ua = log_event(
        customer_id=customer_id,
        book_id=serializer.validated_data["book_id"],
        action=serializer.validated_data["action"],
        session_id=request.session.session_key if hasattr(request, "session") else None,
        when=serializer.validated_data["activity_time"],
    )
    return Response({"id": ua.ActivityID}, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Create many activities in bulk (requires login)",
    tags=["Activities"],
    request=ActivityBulkIn,
    responses={201: OpenApiResponse(description="Created count")}
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def create_activity_bulk(request):
    customer_id = None
    if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
        customer_id = getattr(request.user, 'id', None)
    if customer_id is None:
        customer_id = request.session.get("customer_id")
    if customer_id is None:
        return Response({"detail": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ActivityBulkIn(data=request.data)
    serializer.is_valid(raise_exception=True)

    # ensure session exists / has a key
    if hasattr(request, "session") and request.session.session_key is None:
        request.session.create()
    sid = request.session.session_key if hasattr(request, "session") else None

    items = serializer.validated_data["events"]
    if len(items) > 500:
        return Response({"detail": "Too many events"}, status=status.HTTP_400_BAD_REQUEST)

    created = 0
    for e in items:
        log_event(
            customer_id=customer_id,
            book_id=e["book_id"],
            action=e["action"],
            session_id=sid,
            when=e["activity_time"],
        )
        created += 1

    return Response({"created": created}, status=status.HTTP_201_CREATED)
