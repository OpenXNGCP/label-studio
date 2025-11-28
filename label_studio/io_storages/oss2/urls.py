
from django.urls import path
from . import api

urlpatterns = [
	# Import storage endpoints
	path('import/', api.Oss2ImportStorageListAPI.as_view(), name='oss2-import-storage-list'),
	path('import/<int:pk>/', api.Oss2ImportStorageDetailAPI.as_view(), name='oss2-import-storage-detail'),
	path('import/<int:pk>/sync/', api.Oss2ImportStorageSyncAPI.as_view(), name='oss2-import-storage-sync'),
	path('import/validate/', api.Oss2ImportStorageValidateAPI.as_view(), name='oss2-import-storage-validate'),
	path('import/form-layout/', api.Oss2ImportStorageFormLayoutAPI.as_view(), name='oss2-import-storage-form-layout'),

	# Export storage endpoints
	path('export/', api.Oss2ExportStorageListAPI.as_view(), name='oss2-export-storage-list'),
	path('export/<int:pk>/', api.Oss2ExportStorageDetailAPI.as_view(), name='oss2-export-storage-detail'),
	path('export/<int:pk>/sync/', api.Oss2ExportStorageSyncAPI.as_view(), name='oss2-export-storage-sync'),
	path('export/validate/', api.Oss2ExportStorageValidateAPI.as_view(), name='oss2-export-storage-validate'),
	path('export/form-layout/', api.Oss2ExportStorageFormLayoutAPI.as_view(), name='oss2-export-storage-form-layout'),
]
