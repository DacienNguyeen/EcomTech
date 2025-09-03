from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ...services.log_activity import log_event
from .serializers import ActivityIn, ActivityBulkIn
from apps.recommendations.services import recommendation_engine

@extend_schema(
    summary="Create one activity (requires login)",
    tags=["Activities"],
    request=ActivityIn,
    responses={201: OpenApiResponse(description="Created, returns id")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_activity(request):
    # support JWT principal via request.user or fallback to session
    customer_id = None
    # Prefer authenticated principal (JWT or session-based)
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
    
    # Update recommendation engine
    try:
        # Use singleton instance - no method needed as cache is handled automatically
        pass  # recommendation_engine automatically handles updates
    except Exception as e:
        # Log error but don't fail the request
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating recommendations: {e}")
    
    return Response({"id": ua.ActivityID}, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Create many activities in bulk (requires login)",
    tags=["Activities"],
    request=ActivityBulkIn,
    responses={201: OpenApiResponse(description="Created count")}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_activity_bulk(request):
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
    # Note: recommendation engine updates handled automatically
    
    for e in items:
        log_event(
            customer_id=customer_id,
            book_id=e["book_id"],
            action=e["action"],
            session_id=sid,
            when=e["activity_time"],
        )
        
        # Update recommendation engine for each event
        try:
            # Using singleton instance - no explicit update needed 
            pass  # recommendation_engine handles cache automatically
        except Exception as ex:
            # Log error but continue processing
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error updating recommendations for bulk event: {ex}")
        
        created += 1

    return Response({"created": created}, status=status.HTTP_201_CREATED)
