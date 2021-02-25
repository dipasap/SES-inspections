import django_filters
from users.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
	
	class Meta:
		model = CustomUser
		fields = ["first_name", "last_name", 'date_of_birth', 'phone_number', 'is_inspector', 'is_admin', 'is_active']