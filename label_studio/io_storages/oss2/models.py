
import logging
from typing import Union
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from io_storages.base_models import (
	ExportStorage, ExportStorageLink, ImportStorage, ImportStorageLink, ProjectStorageMixin
)
from io_storages.utils import StorageObject, load_tasks_json, storage_can_resolve_bucket_url

import oss2

logger = logging.getLogger(__name__)

class Oss2StorageMixin(models.Model):
	bucket = models.TextField(_('bucket'), null=True, blank=True, help_text='OSS bucket name')
	prefix = models.TextField(_('prefix'), null=True, blank=True, help_text='OSS bucket prefix')
	regex_filter = models.TextField(
		_('regex_filter'), null=True, blank=True, help_text='Cloud storage regex for filtering objects',
	)
	use_blob_urls = models.BooleanField(
		_('use_blob_urls'), default=False, help_text='Interpret objects as BLOBs and generate URLs',
	)
	oss_access_key_id = models.TextField(_('oss_access_key_id'), null=True, blank=True, help_text='OSS Access Key ID')
	oss_access_key_secret = models.TextField(_('oss_access_key_secret'), null=True, blank=True, help_text='OSS Access Key Secret')
	endpoint = models.TextField(_('endpoint'), null=True, blank=True, help_text='OSS Endpoint')

	def get_client(self):
		return oss2.Bucket(
			oss2.Auth(self.oss_access_key_id, self.oss_access_key_secret),
			self.endpoint,
			self.bucket
		)

	def validate_connection(self, client=None):
		if client is None:
			client = self.get_client()
		try:
			# Try to list objects to check connection
			_ = list(client.list_objects(prefix=self.prefix, max_keys=1))
		except Exception as e:
			logger.error(f'OSS2 connection validation failed: {e}')
			raise

	class Meta:
		abstract = True

class Oss2ImportStorageBase(Oss2StorageMixin, ImportStorage):
	url_scheme = 'oss2'
	recursive_scan = models.BooleanField(_('recursive scan'), default=False, help_text=_('Perform recursive scan over the bucket content'))

	def iter_objects(self):
		client = self.get_client()
		next_marker = ''
		regex = re.compile(str(self.regex_filter)) if self.regex_filter else None
		while True:
			result = client.list_objects(prefix=self.prefix, marker=next_marker)
			for obj in result.object_list:
				key = obj.key
				if key.endswith('/'):
					logger.debug(key + ' is skipped because it is a folder')
					continue
				if regex and not regex.match(key):
					logger.debug(key + ' is skipped by regex filter')
					continue
				logger.debug(f'oss2 {key} has passed the regex filter')
				yield obj
			if not result.is_truncated:
				break
			next_marker = result.next_marker

	def iter_keys(self):
		for obj in self.iter_objects():
			yield obj.key

	def get_unified_metadata(self, obj):
		return {
			'key': obj.key,
			'last_modified': obj.last_modified,
			'size': obj.size,
		}

	def scan_and_create_links(self):
		return self._scan_and_create_links(Oss2ImportStorageLink)

	def get_data(self, key) -> list[StorageObject]:
		uri = f'{self.url_scheme}://{self.bucket}/{key}'
		if self.use_blob_urls:
			data_key = settings.DATA_UNDEFINED_NAME
			task = {data_key: uri}
			return [StorageObject(key=key, task_data=task)]
		client = self.get_client()
		obj = client.get_object(key).read()
		return load_tasks_json(obj, key)

	def can_resolve_url(self, url: Union[str, None]) -> bool:
		return storage_can_resolve_bucket_url(self, url)

	class Meta:
		abstract = True

class Oss2ImportStorage(ProjectStorageMixin, Oss2ImportStorageBase):
	class Meta:
		abstract = False

class Oss2ExportStorage(Oss2StorageMixin, ExportStorage):
	def save_annotation(self, annotation):
		client = self.get_client()
		logger.debug(f'Creating new object on {self.__class__.__name__} Storage {self} for annotation {annotation}')
		ser_annotation = self._get_serialized_data(annotation)
		key = f"{self.prefix}/{annotation.id}.json"
		client.put_object(key, json.dumps(ser_annotation))

class Oss2ImportStorageLink(ImportStorageLink):
	pass

class Oss2ExportStorageLink(ExportStorageLink):
	pass
