@echo off

echo ================================
echo Iniciando sistema...
echo ================================

echo Creando entorno virtual...
python -m venv venv

echo Activando entorno...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Aplicando migraciones...
cd config
python manage.py migrate

echo Iniciando servidor...
python manage.py runserver

pause