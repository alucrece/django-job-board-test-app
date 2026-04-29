import os
import logging
from storages.backends.azure_storage import AzureStorage

logger = logging.getLogger(__name__)


class AzureMediaStorage(AzureStorage):
    """
    Configuration pour stocker les fichiers média (uploads utilisateurs)
    sur Azure Blob Storage.

    Conteneur : 'media'
    Accès : Public (blob)
    """
    account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('STORAGE_ACCOUNT_KEY')
    azure_container = 'media'
    overwrite_files = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.account_name or not self.account_key:
            logger.warning(
                "Azure Storage Account credentials not found. "
                "Ensure STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY are set."
            )


class AzureStaticStorage(AzureStorage):
    """
    Configuration pour stocker les fichiers statiques (CSS, JS, images)
    sur Azure Blob Storage.

    Conteneur : 'static'
    Accès : Privé
    """
    account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('STORAGE_ACCOUNT_KEY')
    azure_container = 'static'
    overwrite_files = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.account_name or not self.account_key:
            logger.warning(
                "Azure Storage Account credentials not found. "
                "Ensure STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY are set."
            )

