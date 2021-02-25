import django_filters
from .models import Device, InspectionType, Inspection, InspectionEntity, QuestionCategory, Question, InspectionReport

# class InspectionFilter(django_filters.FilterSet):
    
#     class Meta:
#         model = Inspection
#         fields = ['device', 'inspection_type', 'user', 'building_occupied', 'all_sys_in_service', 'alarm_normal', 'all_parties_notified', 'sys_remained_in_service', 'suc_dis_by_valves_open', 'guages_in_range', 'hose_valve_closed', 'valves_free_of_water', 'power_on_light', 'transfer_switch_light', 'is_olating_switch_closed', 'jockey_pump_power', 'pump_start_automatically', 'starting_pressure', 'relief_valve_working', 'suction_pressure', 'discharge_pressure', 'packing_glands_noLeaks', 'no_noise_no_vibration', 'comments', 'pass_inspection']

class InspectionEntityFilter(django_filters.FilterSet):
	
	class Meta:
		model = InspectionEntity
		fields = ['name', 'description', 'created_by']

class InspectionTypeFilter(django_filters.FilterSet):
	
	class Meta:
		model = InspectionType
		fields = ['name', 'description', 'created_by']

class DeviceFilter(django_filters.FilterSet):
	
	class Meta:
		model = Device
		fields = ["entity", "name", "description", "inspection_type", "inspector", "assigned_by"]

class QuestionCategoryFilter(django_filters.FilterSet):
	
	class Meta:
		model = QuestionCategory
		fields = ["entity", "device", "title", "slug", "created_by"]

class QuestionFilter(django_filters.FilterSet):
	
	class Meta:
		model = Question
		fields = ["entity", "device", "category","question_text", "answer_type", "choices", "created_by"]

class InspectionFilter(django_filters.FilterSet):
	
	class Meta:
		model = Inspection
		fields = ["name", "entity", "devices", "inspectors", "inspection_type", "start_date_time", "created_by"]

class InspectionReportFilter(django_filters.FilterSet):
	
	class Meta:
		model = InspectionReport
		fields = ["inspection", "user", "is_active", "reported_datetime"]