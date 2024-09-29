from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """
    Custom file storage for GCS that generates correct media URLs.
    """
    bucket_name = setting('GS_BUCKET_NAME')

    def url(self, name):
        """
        Generate correct media URLs using MEDIA_URL instead of default Google URL.
        """
        return urljoin(settings.MEDIA_URL, name)
