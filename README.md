# SOS Madera · Contacto con ayuntamientos

App de Streamlit para hacer el seguimiento de la campaña de presentación de SOS Madera a ayuntamientos y organismos públicos. Integra el kit completo: lista de 37 entidades priorizadas, generador de cartas (castellano y valenciano), guía de contacto y dossier PDF.

## Secciones

- **Panel**: indicadores, llamadas de seguimiento vencidas, avance por tanda y próximos envíos.
- **Seguimiento**: tabla editable con filtros; «Registrar envío» marca la fecha y programa la llamada a los 8 días.
- **Generar carta**: carta personalizada por entidad, descargable o lista para abrir en el correo.
- **Kit de contacto**: a quién contactar, qué enviar, dónde y cómo, calendario y lista de documentación.
- **Dossier**: descarga del PDF de presentación.
- **Datos**: copia de seguridad en CSV/Excel e importación.

## Publicar en Streamlit Community Cloud

1. Crea un repositorio privado en GitHub y sube todo el contenido de esta carpeta (incluida la carpeta oculta `.streamlit`).
2. Entra en share.streamlit.io → **Create app** → elige el repositorio, la rama `main` y el archivo `app.py`.
3. En **Advanced settings → Secrets** pega el contenido de `.streamlit/secrets.toml.example` con tus datos (como mínimo `app_password`).
4. Despliega.

## Guardar los datos de forma permanente (Google Sheets)

Streamlit Cloud borra los archivos locales al reiniciar la app. Para no perder el seguimiento:

1. En Google Cloud Console crea un proyecto y activa **Google Sheets API** y **Google Drive API**.
2. Crea una **cuenta de servicio** y descarga su clave JSON.
3. Crea una hoja de cálculo vacía en Google Drive y compártela como editor con el `client_email` de la cuenta de servicio.
4. En los Secrets de la app añade `sheet_url` y el bloque `[gcp_service_account]` con los datos del JSON.

La primera vez que arranque, la app rellena la hoja con la lista inicial. Sin Google Sheets la app funciona igual, pero conviene descargar una copia en **Datos** al terminar cada sesión.

## Personalizar

- **Logo**: sustituye `assets/logo.png` (idealmente en alta resolución) y `assets/icon.png`.
- **Colores**: `.streamlit/config.toml` y las variables CSS al principio de `app.py`.
- **Textos de cartas y guía**: `textos.py`.
- **Dossier**: sustituye `assets/dossier_sosmadera_ayuntamientos.pdf` por la versión final con fotos.
