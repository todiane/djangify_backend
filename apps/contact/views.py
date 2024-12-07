from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from django.core.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle
import logging

logger = logging.getLogger(__name__)

class ContactRateThrottle(AnonRateThrottle):
    rate = '5/hour'  # Limit to 5 messages per hour per IP

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    throttle_classes = [ContactRateThrottle]
    http_method_names = ['post']  # Only allow POST requests

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            
            # Add IP address and user agent
            contact = serializer.save(
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            logger.info(
                f"New contact message received from {contact.email} - IP: {contact.ip_address}"
            )
            
            return Response(
                {"message": "Your message has been sent successfully."},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            logger.warning(
                f"Invalid contact submission from IP {self.get_client_ip(request)}: {str(e)}"
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                f"Error processing contact submission: {str(e)}",
                exc_info=True
            )
            return Response(
                {"error": "An error occurred processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    