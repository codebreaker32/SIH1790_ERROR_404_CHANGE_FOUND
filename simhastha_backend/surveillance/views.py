from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import public_user, Report, User
from .otp_service import send_otp
from .serializers import PublicUserSerializer, PublicUserLandingPageSerializer, ReportStatusSerializer, LogoutSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
import logging
from django.utils import timezone
from django.contrib.auth import authenticate, login
from .models import Report, StaffUser, ReportMatch
from .serializers import ReportSerializer, StaffUserLoginSerializer, ReportUpdateSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Logging current time for debugging
logging.info(f"Current Time: {timezone.now()}")

class Get_live_time(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Return the current server time."""
        return Response({"current_time": timezone.now()}, status=status.HTTP_200_OK)

def get_tokens_for_user(user):
    """Generate JWT tokens for the authenticated user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SendOtpView(APIView):
    """Handles sending an OTP to the user's phone number."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create a public_user instance based on phone number
        user, created = public_user.objects.get_or_create(phone_number=phone_number)

        # Send OTP
        otp = send_otp(phone_number)
        if otp:
            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework_simplejwt.tokens import RefreshToken

class VerifyOtpView(APIView):
    """Handles verifying the OTP and logging the user in."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response({"error": "Phone number and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the user based on the phone number
            public_user_instance = public_user.objects.get(phone_number=phone_number)
            serializer = PublicUserSerializer()

            # Validate OTP using the serializer method
            if serializer.validate_otp(public_user_instance, otp):
                # Ensure the public_user instance has a linked User object
                if public_user_instance.user is None:
                    # Create the User instance if it doesn't exist
                    user = User.objects.create(
                        username=public_user_instance.phone_number
                    )
                    user.set_password('mypassword123')  # Set a default password
                    user.save()

                    # Link the User instance to the public_user instance
                    public_user_instance.user = user
                    public_user_instance.save()
                else:
                    user = public_user_instance.user

                # Generate JWT token using the linked User instance
                refresh = RefreshToken.for_user(user)

                return Response({
                    "message": "Phone number verified successfully.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        except public_user.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class PublicUserLandingPageView(APIView):
    """Handles viewing report status and filing reports."""
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this

    def get(self, request):
        # Retrieve all reports associated with the authenticated public_user
        user = get_object_or_404(public_user, user=request.user)  # Fetch public_user using request.user

        # Fetch all reports related to this public_user
        reports = Report.objects.filter(user=user)

        if not reports.exists():
            return Response({"message": "No reports found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the reports
        serializer = ReportStatusSerializer(reports, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PublicUserLandingPageSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save()
            return Response({"message": "Report filed successfully.", "report_id": report.report_id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request, format=None):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data['refresh_token'])
            token.blacklist()
            return Response({'msg': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'errors': {'non_field_errors': ['Invalid token or token has already been blacklisted.']}}, status=status.HTTP_400_BAD_REQUEST)

###############################################
# Staff User Views
###############################################
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Successful. Request for permission of staff user has been sent'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffUserLoginView(APIView):
    permission_classes = [AllowAny]
    """Handles staff login and returns JWT tokens."""
    
    def post(self, request):
        serializer = StaffUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            # Check if user exists, is a staff member, and is verified
            if user and hasattr(user, 'staff_profile'):
                staff_profile = user.staff_profile
                if not staff_profile.is_verified:
                    return Response({'error': 'You are not a valid user. Please contact the administrator if you think this is a mistake.'}, 
                                    status=status.HTTP_403_FORBIDDEN)
                
                # If verified, generate JWT tokens for the authenticated user
                tokens = get_tokens_for_user(user)
                return Response({'message': 'Staff logged in successfully.', 'tokens': tokens}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials or not a staff user.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 


class StaffReportListView(APIView):
    """Get all reports for staff users."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'staff_profile'):
            return Response({'error': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
        
        reports = Report.objects.all()  # Get all reports
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportDetailAPIView(APIView):
    """Retrieve, update, and delete a report by its report_id. Only staff users can access this."""
    permission_classes = [IsAuthenticated]

    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportUpdateSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        report.delete()
        return Response({'message': 'Report deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UpdateReportStatusAPIView(APIView):
    """
    Update the status of a report and handle matches. Staff can mark as 'Match Found'
    or append new match data using this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        # Retrieve the report instance
        report = get_object_or_404(Report, report_id=report_id)

        # Extract data from request (location and match data are optional for now)
        location = request.data.get('location', None)
        match_data = request.data.get('match_data', {})  # Leave as blank if not provided

        # Set the report status to "Match Found"
        report.status = 'Found'
        report.save()  # This will trigger the signal to notify staff users
        
        # Check if a ReportMatch already exists for the report
        try:
            report_match, created = ReportMatch.objects.get_or_create(report=report)

            # If new match data or location is provided, append/update it
            if match_data or location:
                report_match.append_match_data(new_data=match_data, location=location)
            else:
                # If no new data is provided, just update the timestamp
                report_match.timestamp = timezone.now()
                report_match.save()

        except Exception as e:
            logging.error(f"Error creating or updating ReportMatch: {e}")
            return Response({'error': 'Failed to update match data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Response after successful match update and status change
        return Response({
            'message': 'Match found, report status updated. Staff will be notified.'
        }, status=status.HTTP_200_OK)


class CreateReportAPIView(APIView):
    """Create a new report."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # The report_id will be auto-generated in the model's save method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)