#!/bin/bash
# Script de despliegue inicial para el VPS
# Corre este script como root en el servidor Hostinger
# Uso: bash deploy.sh

set -e

echo "======================================"
echo "  Despliegue de Edgecom en Docker"
echo "======================================"

# 1. Actualizar sistema e instalar Docker
echo "[1/6] Instalando Docker..."
apt-get update -q
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -q
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
echo "Docker instalado correctamente."

# 2. Clonar el repositorio
echo "[2/6] Clonando repositorio..."
cd /opt
if [ -d "edgecom" ]; then
    echo "El directorio /opt/edgecom ya existe. Haciendo pull..."
    cd edgecom
    git pull
else
    git clone https://github.com/jairoo-dev/edgecom.git
    cd edgecom
fi

# 3. Crear el archivo .env
echo "[3/6] Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "IMPORTANTE: Edita /opt/edgecom/.env con tus valores reales antes de continuar."
    echo "  nano /opt/edgecom/.env"
    echo ""
    echo "Cuando termines de editar el .env, vuelve a correr:"
    echo "  cd /opt/edgecom && bash deploy.sh"
    exit 0
fi

# 4. Construir y levantar los contenedores
echo "[4/6] Construyendo contenedores (puede tardar unos minutos)..."
docker compose build --no-cache

echo "[5/6] Levantando servicios..."
docker compose up -d

# 5. Esperar a que la BD esté lista y correr migraciones
echo "[6/6] Corriendo migraciones..."
sleep 5
docker compose exec web python manage.py migrate

# 6. Crear superusuario si no existe
docker compose exec web python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='edge').exists():
    User.objects.create_superuser('edge', 'edge@edgecom.mx', 'Edge123!')
    print('Superusuario edge creado.')
else:
    print('El superusuario edge ya existe.')
"

echo ""
echo "======================================"
echo "  ¡Despliegue completado!"
echo "  Edgecom disponible en http://$(curl -s ifconfig.me)"
echo "======================================"
