#! /usr/bin/env python
import os
import google.oauth2
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Configura la autenticación
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"

# Llena con tus credenciales
client_secrets_file = "client_secret.json"

# Crea una instancia de OAuth2
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_console()

# Crea una instancia de la API de YouTube
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Ruta del video a subir
video_path = "ruta/del/video/video.mp4"

# Datos del video
video_data = {
    "snippet": {
        "title": "Título del Video",
        "description": "Descripción del Video",
        "tags": ["etiqueta1", "etiqueta2"],
        "categoryId": "22"  # Categoría de entretenimiento
    },
    "status": {
        "privacyStatus": "public"  # Configura la privacidad del video (público)
    }
}

# Sube el video
request = youtube.videos().insert(
    part="snippet,status",
    body=video_data,
    media_body=mediaFile
)

response = request.execute()

# Obtiene el enlace al video subido
video_url = f"https://www.youtube.com/watch?v={response['id']}"
print(f"El video se ha subido correctamente. Puedes verlo aquí: {video_url}")
