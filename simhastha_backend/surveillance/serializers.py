from rest_framework import serializers
from .models import public_user, Report, StaffUser
from .otp_service import send_otp, verify_otp  # Import the OTP service
from django.utils import timezone
from django.contrib.auth.models import User

# Serializer for public users

class PublicUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = public_user
        fields = ['phone_number', 'otp', 'verified', 'created_at', 'password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return data

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        password = validated_data.pop('password')  # Remove password from validated_data
        password2 = validated_data.pop('password2')  # Remove password2 from validated_data

        # Create or get a User instance where username is the phone number
        user, created = User.objects.get_or_create(
            username=phone_number
        )

        # Check if the user is already verified to avoid re-sending OTP
        public_user_instance = public_user.objects.filter(user=user).first()
        if public_user_instance and public_user_instance.verified:
            raise serializers.ValidationError("This user is already verified.")

        # Set the password using set_password to hash it
        user.set_password(password)
        user.save()

        # Send OTP using your otp_service
        send_otp(phone_number)
        
        # Create and save the public_user instance linked with the User model
        public_user_instance = public_user.objects.create(
            user=user,
            phone_number=phone_number,
            otp='',  # This will be updated after OTP verification
            verified=False,
            otp_created_at=timezone.now(),
            **validated_data
        )
        
        return public_user_instance

    def validate_otp(self, user, entered_otp):
        """Validate OTP using the otp_service and model logic."""
        is_valid, message = verify_otp(user.phone_number, entered_otp)

        if not is_valid:
            raise serializers.ValidationError(message)

        # Mark the user as verified after successful OTP verification
        user.verified = True
        user.otp = ''  # Clear OTP after validation
        user.save()

        return True

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs


# Serializer for creating and viewing reports
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        # Reflecting all fields from the updated Report model
        fields = ['report_id', 'user', 'report_type', 'image','name', 'age', 'gender', 'description', 'last_seen_location', 'status', 'timestamp']
        read_only_fields = ['report_id', 'status', 'timestamp']

    def validate_user(self, value):
        """Ensure the user is verified before allowing them to file a report."""
        if not value.verified:
            raise serializers.ValidationError("User must be verified to file a report.")
        return value

    def create(self, validated_data):
        """
        Override the default create method to handle custom report creation logic.
        """
        report = Report.objects.create(
            user=validated_data['user'],
            report_type=validated_data.get('report_type'),
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            description=validated_data.get('description'),
            last_seen_location=validated_data.get('last_seen_location'),
            status='Pending',  # Default status for new reports
        )
        return report

# Serializer for updating reports
class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        # Reflecting the fields that can be updated
        fields = ['report_type', 'name', 'age', 'gender', 'description', 'last_seen_location', 'image']
        read_only_fields = ['report_id']  # Keep report_id read-only to prevent modification

# Serializer for the landing page (Public User Report)
class PublicUserLandingPageSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6, write_only=True, required=False)  # OTP field for verification
    report_type = serializers.CharField(max_length=50, required=False)  # Type of report (person/item)
    name = serializers.CharField(max_length=100, required=False)  # Name of the missing person/item
    age = serializers.IntegerField(required=False)  # Age of missing person (if applicable)
    gender = serializers.ChoiceField(choices=[('Male', 'male'), ('Female', 'female'), ('Other', 'other')], required=False)  # Gender of the missing person
    description = serializers.CharField(required=False)  # Description of missing person/item
    last_seen_location = serializers.CharField(max_length=255, required=False)  # Last known location
    report_id = serializers.CharField(read_only=True)  # Report ID (auto-generated after filing a report)

    def validate(self, attrs):
        """
        Ensure the user is verified via OTP before filing a report or checking status.
        """
        phone_number = attrs.get('phone_number')
        otp = attrs.get('otp')

        if otp:
            # OTP verification flow
            user = public_user.objects.get(phone_number=phone_number)

            # Check if OTP is valid and not expired
            if not user.otp_is_valid():
                raise serializers.ValidationError("OTP has expired. Please request a new one.")

            is_valid = verify_otp(phone_number, otp)
            if not is_valid:
                raise serializers.ValidationError("Incorrect OTP. Please try again.")

            # Mark user as verified after successful OTP validation
            user.verified = True
            user.save()

        return attrs

    def create(self, validated_data):
        """
        If the user is verified, allow them to file a missing report.
        """
        phone_number = validated_data.get('phone_number')
        user = public_user.objects.get(phone_number=phone_number)

        # Ensure user is verified before allowing report creation
        if not user.verified:
            raise serializers.ValidationError("User must be verified to file a report.")

        # Create the report
        report = Report.objects.create(
            user=user,
            report_type=validated_data.get('report_type'),
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            description=validated_data.get('description'),
            last_seen_location=validated_data.get('last_seen_location'),
            status='Pending',  # Default status for new reports
        )
        
        return report

# Serializer for viewing report status
class ReportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['report_id', 'status', 'name', 'description', 'last_seen_location', 'timestamp', 'image']  # Add image field if applicable
        read_only_fields = ['report_id', 'status', 'timestamp']

# Serializer for staff login


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=True)  # Make it required
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def validate(self, data):
        # Check if password and password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        
        return data

    def create(self, validated_data):
        # Remove password_confirmation from validated data as we don't need it for user creation
        validated_data.pop('password_confirmation')

        # Extract phone_number from validated_data before removing it
        phone_number = validated_data.pop('phone_number')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        # Create the StaffUser instance linked to the user
        StaffUser.objects.create(user=user, phone_number=phone_number)

        return user

class StaffUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # You can add custom validation logic here if needed
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')

        return data