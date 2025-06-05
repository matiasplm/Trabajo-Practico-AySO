import socket
import urllib.request
import re

# Forzar solo IPv4 para evitar delays
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(*args, **kwargs):
    return [ai for ai in orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = getaddrinfo_ipv4

# Descargar HTML de Wikipedia
url = "https://en.wikipedia.org/wiki/FIFA_World_Cup"
html = urllib.request.urlopen(url).read().decode('utf-8')

# Buscar el campeón actual usando regex
match = re.search(r'Current champions.*?title="([^"]+)"', html)
campeon = match.group(1).replace("_", " ") if match else "Desconocido"

# Imagen fija de Messi
imagen_url = "https://img.goodfon.com/original/1920x1080/a/95/lionel-messi-fifa-world-cup-2022-soccer-trophy-argentina-vic.jpg"

# Generar HTML
html_salida = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Campeón del Mundo</title>
</head>
<body style="text-align:center; font-family:sans-serif;">
  <h1>Último Campeón del Mundo</h1>
  <p style="font-size:24px;">{campeon}</p>
  <img src="{imagen_url}" alt="Messi con la copa" style="max-width:90%; height:auto; margin-top:20px;">
</body>
</html>
"""

# Guardar en la carpeta de Apache
with open("/var/www/html/index.html", "w") as f:
    f.write(html_salida)

