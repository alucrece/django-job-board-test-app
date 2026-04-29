#!/usr/bin/env python
"""
Script d'initialisation Azure Blob Storage
Crée les conteneurs nécessaires et upload les fichiers media/static
"""

import os
import sys
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import ContentSettings
import mimetypes


def initialize_azure_storage():
    """
    Initialise les conteneurs Azure Blob Storage
    Crée les conteneurs 'static' et 'media' s'ils n'existent pas
    Upload les fichiers media et static
    """
    storage_account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
    storage_account_key = os.environ.get('STORAGE_ACCOUNT_KEY')

    # Si les variables d'environnement ne sont pas définies, on sort
    if not storage_account_name or not storage_account_key:
        print("ℹ️  Variables d'environnement Azure non trouvées. Utilisation du stockage local.")
        return True

    try:
        # Créer le client Blob Storage
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Conteneurs à créer
        containers = [
            {'name': 'static', 'public_access': None},
            {'name': 'media', 'public_access': 'blob'}
        ]

        # 1️⃣ Créer les conteneurs
        print("\n📦 Création des conteneurs...")
        for container_config in containers:
            container_name = container_config['name']
            try:
                # Essayer de créer le conteneur
                container_client = blob_service_client.create_container(
                    name=container_name,
                    public_access=container_config['public_access']
                )
                print(f"✅ Conteneur '{container_name}' créé avec succès")
            except ResourceExistsError:
                print(f"ℹ️  Conteneur '{container_name}' existe déjà")
            except Exception as e:
                print(f"❌ Erreur lors de la création du conteneur '{container_name}': {e}")
                return False

        # 2️⃣ Upload des fichiers media et static
        print("\n📤 Upload des fichiers...")
        migrations = [
            {
                'local_path': Path('media'),
                'container_name': 'media',
                'description': 'Fichiers Media (CVs, Images profil)'
            },
            {
                'local_path': Path('staticfiles'),
                'container_name': 'static',
                'description': 'Fichiers Statiques (CSS, JS)'
            }
        ]

        for migration in migrations:
            local_path = migration['local_path']
            container_name = migration['container_name']
            description = migration['description']

            if not local_path.exists():
                print(f"ℹ️  {description} : Dossier '{local_path}' n'existe pas, passage...")
                continue

            print(f"\n📁 {description}...")
            container_client = blob_service_client.get_container_client(container_name)

            # Compter les fichiers
            files = [f for f in local_path.rglob('*') if f.is_file()]
            file_count = len(files)

            if file_count == 0:
                print(f"   ℹ️  Aucun fichier à uploader")
                continue

            print(f"   Total : {file_count} fichier(s)")

            # Upload les fichiers
            uploaded = 0
            for file_path in files:
                # Calcul du path relatif
                relative_path = file_path.relative_to(local_path)
                blob_name = str(relative_path).replace('\\', '/')
                # Déterminer le content type
                content_type, _ = mimetypes.guess_type(file_path)
                content_settings = ContentSettings(content_type=content_type)
                try:
                    with open(file_path, 'rb') as data:
                        container_client.upload_blob(
                            name=blob_name,
                            data=data,
                            content_settings=content_settings,
                            overwrite=True
                        )
                    print(f"   ✅ {blob_name} ({content_type}) uploadé")
                    uploaded += 1
                except Exception as e:
                    print(f"   ⚠️  Erreur upload {blob_name}: {e}")

            print(f"   ✅ {uploaded}/{file_count} fichiers uploadés")

        print("\n✅ Initialisation Azure Blob Storage terminée")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la connexion à Azure: {e}")
        return False


if __name__ == '__main__':
    success = initialize_azure_storage()
    sys.exit(0 if success else 1)

