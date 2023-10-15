# python-video-publisher

Work In Progress

Este proyecto pretende ser una herramienta para ayudar a subir vídeos a sitios webs
y redes sociales pudiendo enviar una petición también a api propia en la que asociar
estos vídeos a contenido.

El origen de los datos será vía un json con el mismo nombre que el vídeo, para poder
de esta forma tener todos los metadatos necesarios tanto al subir el vídeo como
al comunicar en nuestra api que lo hemos asociado y cuáles son sus datos.

Los datos recibidos son:

- title: Título del vídeo
- description
- tags: Lista de etiquetas en un array para asociarlas al vídeo subido.

# Modo de uso

Para realizar la subida de un vídeo podemos utilizar la siguiente sintaxis:

```bash
python3 main.py --file="path" --move-to="new_path"
```

El parámetro del archivo fuente es obligatorio mientras mover queda como opcional.
Mover el vídeo puede ser util si automatizamos directorios por lotes para ir descartando fuera de este los ya subidos.
