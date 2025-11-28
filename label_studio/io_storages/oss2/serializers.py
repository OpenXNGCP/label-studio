
import os
import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from io_storages.oss2.models import Oss2ExportStorage, Oss2ImportStorage
from io_storages.serializers import ExportStorageSerializer, ImportStorageSerializer

logger = logging.getLogger(__name__)

class Oss2StorageSerializerMixin:
	secure_fields = ['oss_access_key_id', 'oss_access_key_secret']

	def to_representation(self, instance):
		result = super().to_representation(instance)
		for attr in self.secure_fields:
			result.pop(attr, None)
		return result

	def validate(self, data):
		data = super().validate(data)
		if not data.get('bucket', None):
			return data

		storage = self.instance
		if storage:
			for key, value in data.items():
				setattr(storage, key, value)
		else:
			if 'id' in self.initial_data:
				storage_object = self.Meta.model.objects.get(id=self.initial_data['id'])
				for attr in self.secure_fields:
					data[attr] = data.get(attr) or getattr(storage_object, attr)
			storage = self.Meta.model(**data)
		try:
			storage.validate_connection()
		except Exception as e:
			logger.info(f'OSS2 connection validation failed: {e}', exc_info=True)
			raise ValidationError(f'Cannot connect to OSS2 {storage.bucket} with specified credentials')
		return data

class Oss2ImportStorageSerializer(Oss2StorageSerializerMixin, ImportStorageSerializer):
	type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

	class Meta:
		model = Oss2ImportStorage
		fields = '__all__'

class Oss2ExportStorageSerializer(Oss2StorageSerializerMixin, ExportStorageSerializer):
	type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

	class Meta:
		model = Oss2ExportStorage
		fields = '__all__'
