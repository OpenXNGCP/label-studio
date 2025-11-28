
from io_storages.api import (
	ExportStorageDetailAPI,
	ExportStorageFormLayoutAPI,
	ExportStorageListAPI,
	ExportStorageSyncAPI,
	ExportStorageValidateAPI,
	ImportStorageDetailAPI,
	ImportStorageFormLayoutAPI,
	ImportStorageListAPI,
	ImportStorageSyncAPI,
	ImportStorageValidateAPI,
)
from io_storages.oss2.models import Oss2ExportStorage, Oss2ImportStorage
from io_storages.oss2.serializers import Oss2ExportStorageSerializer, Oss2ImportStorageSerializer

class Oss2ImportStorageListAPI(ImportStorageListAPI):
	queryset = Oss2ImportStorage.objects.all()
	serializer_class = Oss2ImportStorageSerializer

class Oss2ImportStorageDetailAPI(ImportStorageDetailAPI):
	queryset = Oss2ImportStorage.objects.all()
	serializer_class = Oss2ImportStorageSerializer

class Oss2ImportStorageSyncAPI(ImportStorageSyncAPI):
	serializer_class = Oss2ImportStorageSerializer

class Oss2ImportStorageValidateAPI(ImportStorageValidateAPI):
	serializer_class = Oss2ImportStorageSerializer

class Oss2ExportStorageValidateAPI(ExportStorageValidateAPI):
	serializer_class = Oss2ExportStorageSerializer

class Oss2ExportStorageListAPI(ExportStorageListAPI):
	queryset = Oss2ExportStorage.objects.all()
	serializer_class = Oss2ExportStorageSerializer

class Oss2ExportStorageDetailAPI(ExportStorageDetailAPI):
	queryset = Oss2ExportStorage.objects.all()
	serializer_class = Oss2ExportStorageSerializer

class Oss2ExportStorageSyncAPI(ExportStorageSyncAPI):
	serializer_class = Oss2ExportStorageSerializer

class Oss2ImportStorageFormLayoutAPI(ImportStorageFormLayoutAPI):
	pass

class Oss2ExportStorageFormLayoutAPI(ExportStorageFormLayoutAPI):
	pass
