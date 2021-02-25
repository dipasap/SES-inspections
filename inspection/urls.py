from django.urls import path
from inspection.views import dashboard, inspection_entity, inspection_type, inspection_device, question_category, question, inspection, answer, inspection_report

urlpatterns =[
	path('', dashboard.Dashboard.as_view(), name='dashboard'),

	# Inspection Routes (URLs)
	path('inspection/list/', inspection.InspectionListView.as_view(), name='inspection-list'),
	path('inspection/create/', inspection.InspectionCreateView.as_view(), name='inspection-create'),
	path('inspection/update/<int:pk>/', inspection.InspectionUpdateView.as_view(), name='inspection-update'),
	path('inspection/details/<int:pk>/', inspection.InspectionDetailView.as_view(), name='inspection-details'),
	path('inspection/delete/<int:pk>/', inspection.InspectionDeleteView.as_view(), name='inspection-delete'),
	
	path('inspection/device/question_answer/create/<str:inspection_name>/<str:device>/<int:pk>/', answer.InspectionQuestioAnswerView.as_view(), name='inspection-question-answer-form'),
	path('inspection/device/question_answer/create/<str:inspection_name>/<str:device>/<int:pk>/<int:step>/', answer.InspectionQuestioAnswerView.as_view(), name='inspection-question-answer-form-step'),

	# Inspection Routes (URLs)
	path('inspection/report/list/', inspection_report.InspectionReportListView.as_view(), name='inspection-report-list'),
	path('inspection/report/create/', inspection_report.InspectionReportCreateView.as_view(), name='inspection-report-create'),
	path('inspection/report/update/<int:pk>/', inspection_report.InspectionReportUpdateView.as_view(), name='inspection-report-update'),
	path('inspection/report/details/<int:pk>/', inspection_report.InspectionReportDetailView.as_view(), name='inspection-report-details'),
	path('inspection/report/delete/<int:pk>/', inspection_report.InspectionReportDeleteView.as_view(), name='inspection-report-delete'),

	# Inspection Entity Routes (URLs)
	path('inspection/entity/list/', inspection_entity.InspectionEntityListView.as_view(), name='inspection-entity-list'),
	path('inspection/entity/create/', inspection_entity.InspectionEntityCreateView.as_view(), name='inspection-entity-create'),
	path('inspection/entity/update/<int:pk>/', inspection_entity.InspectionEntityUpdateView.as_view(), name='inspection-entity-update'),
	path('inspection/entity/details/<int:pk>/', inspection_entity.InspectionEntityDetailView.as_view(), name='inspection-entity-details'),
	path('inspection/entity/delete/<int:pk>/', inspection_entity.InspectionEntityDeleteView.as_view(), name='inspection-entity-delete'),

	# Inspection Type Routes (URLs)
	path('inspection/type/list/', inspection_type.InspectionTypeListView.as_view(), name='inspection-type-list'),
	path('inspection/type/create/', inspection_type.InspectionTypeCreateView.as_view(), name='inspection-type-create'),
	path('inspection/type/update/<int:pk>/', inspection_type.InspectionTypeUpdateView.as_view(), name='inspection-type-update'),
	path('inspection/type/details/<int:pk>/', inspection_type.InspectionTypeDetailView.as_view(), name='inspection-type-details'),
	path('inspection/type/delete/<int:pk>/', inspection_type.InspectionTypeDeleteView.as_view(), name='inspection-type-delete'),

	# Inspection Device Routes (URLs)
	path('inspection/entites/device/list/', inspection_device.DeviceListView.as_view(), name='inspection-device-list'),
	path('inspection/entites/device/create/', inspection_device.DeviceCreateView.as_view(), name='inspection-device-create'),
	path('inspection/entites/device/update/<int:pk>/', inspection_device.DeviceUpdateView.as_view(), name='inspection-device-update'),
	path('inspection/entites/device/details/<int:pk>/', inspection_device.DeviceDetailView.as_view(), name='inspection-device-details'),
	path('inspection/entites/device/delete/<int:pk>/', inspection_device.DeviceDeleteView.as_view(), name='inspection-device-delete'),

	# Inspection Question Category Routes (URLs)
	path('inspection/entites/device/question_category/list/', question_category.QuestionCategoryListView.as_view(), name='question-category-list'),
	path('inspection/entites/device/question_category/create/', question_category.QuestionCategoryCreateView.as_view(), name='question-category-create'),
	path('inspection/entites/device/question_category/update/<int:pk>/', question_category.QuestionCategoryUpdateView.as_view(), name='question-category-update'),
	path('inspection/entites/device/question_category/details/<int:pk>/', question_category.QuestionCategoryDetailView.as_view(), name='question-category-details'),
	path('inspection/entites/device/question_category/delete/<int:pk>/', question_category.QuestionCategoryDeleteView.as_view(), name='question-category-delete'),

	# Inspection Question Category Routes (URLs)
	path('inspection/entites/device/question_category/question/list/', question.QuestionListView.as_view(), name='question-list'),
	path('inspection/entites/device/question_category/question/create/', question.QuestionCreateView.as_view(), name='question-create'),
	path('inspection/entites/device/question_category/question/update/<int:pk>/', question.QuestionUpdateView.as_view(), name='question-update'),
	path('inspection/entites/device/question_category/question/details/<int:pk>/', question.QuestionDetailView.as_view(), name='question-details'),
	path('inspection/entites/device/question_category/question/delete/<int:pk>/', question.QuestionDeleteView.as_view(), name='question-delete'),

]
