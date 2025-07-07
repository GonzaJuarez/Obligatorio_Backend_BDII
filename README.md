# Sistema de Votación Electrónico - Backend

## Descripción del Proyecto

Este es un sistema de votación electrónico desarrollado como parte del obligatorio de Bases de Datos II. El sistema permite gestionar elecciones, votantes, votos y operadores de manera eficiente y segura.

### Características Principales

- **Gestión de Operadores**: Sistema de login con contraseñas hasheadas y asignación de circuitos
- **Gestión de Votantes**: Registro y administración de votantes con credenciales por circuito
- **Sistema de Votación**: Emisión de votos con validación de observados
- **Gestión de Elecciones**: Creación y administración de elecciones y listas electorales
- **Estadísticas y Reportes**: Generación de reportes detallados por circuito y departamento
- **Control de Votación**: Apertura y cierre de votación por circuito

### Estructura de la Base de Datos

El sistema utiliza una base de datos MySQL con las siguientes entidades principales:

- **Votante**: Información personal de los votantes
- **Circuito**: Circuitos electorales con sus establecimientos
- **MiembroMesa**: Operadores y administradores del sistema
- **Eleccion**: Elecciones disponibles
- **Lista**: Listas electorales con candidatos
- **Voto**: Registro de votos emitidos
- **IntegranteLista**: Integrantes de las listas electorales
- **ListaCredenciales**: Habilitación de votantes por circuito
- **RegistroDeEmision**: Control de votos ya emitidos

## Instrucciones Paso a Paso para Levantar el Proyecto

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.8 o superior
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd Backend_Obligatorio_BD2
```

### Paso 2: Levantar la Base de Datos con Docker

```bash
cd BaseDatos
docker-compose up --build
```

Esto levantará un contenedor MySQL con las siguientes configuraciones:
- Host: localhost
- Puerto: 3306
- Usuario: root
- Contraseña: contraseña root
- Base de datos: XR_Grupo5

### Paso 3: Ejecutar Scripts de Base de Datos

Ejecutar los script de base de datos de creacion de base de datos y datos iniciales

### Paso 5: Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD='contraseña root'
MYSQL_DB='XR_Grupo5'
```

### Paso 6: Crear entorno virtual e instalar dependencias

```bash
python -m venv nombre_entorno_virtual
nombre_entorno_virtual/Scripts/activate
pip install -r requirements.txt
```

### Paso 7: Ejecutar la Aplicación

```bash
cd app
uvicorn main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

### Paso 8: Verificar la Instalación

1. **Test de Conexión**: Visita http://localhost:8000/test-db
2. **Documentación API**: Visita http://localhost:8000/docs
3. **Documentación Alternativa**: Visita http://localhost:8000/redoc

## Endpoints Principales

### Operadores
- `POST /operadores/login` - Login de operador
- `GET /operadores/{cc}` - Obtener operador por CC
- `POST /operadores/` - Crear operador
- `DELETE /operadores/{cc}` - Eliminar operador

### Votantes
- `GET /votantes/` - Listar votantes
- `GET /votantes/{cc}` - Obtener votante por CC
- `POST /votantes/` - Crear votante
- `DELETE /votantes/{cc}` - Eliminar votante

### Votos
- `POST /votos/` - Emitir voto
- `GET /votos/resultados` - Ver resultados
- `POST /votos/verificar-observado` - Verificar si voto es observado

### Elecciones
- `POST /elecciones/` - Crear elección
- `DELETE /elecciones/{id}` - Eliminar elección
- `POST /elecciones/listas` - Crear lista
- `GET /elecciones/listas` - Obtener listas
- `DELETE /elecciones/listas/{numero}` - Eliminar lista

### Estadísticas
- `GET /estadisticas/resultados-circuito/{id}` - Resultados por circuito
- `GET /estadisticas/resultados-partido-circuito/{id}` - Resultados por partido en circuito
- `GET /estadisticas/resultados-candidato-circuito/{id}` - Resultados por candidato en circuito
- `GET /estadisticas/resultados-departamento/{departamento}` - Resultados por departamento
- `GET /estadisticas/ganadores-departamentos` - Ganadores por departamento
- `POST /estadisticas/abrir-votacion/{id}` - Abrir votación
- `POST /estadisticas/cerrar-votacion/{id}` - Cerrar votación

## Datos de Prueba

El sistema incluye datos de prueba con:
- 21 votantes
- 7 circuitos electorales
- 4 operadores (incluyendo 1 admin)
- 2 partidos políticos
- 4 candidatos
- 8 listas electorales
- 8 votos de ejemplo

### Usuario Administrador
- **CC**: ABC1111
- **Contraseña**: admin123
- **Rol**: ADMIN

## Tecnologías Utilizadas

- **Backend**: FastAPI (Python)
- **Base de Datos**: MySQL
- **Contenedores**: Docker
- **Autenticación**: bcrypt para hashing de contraseñas
- **Documentación**: Swagger/OpenAPI

## Estructura del Proyecto

```
Backend_Obligatorio_BD2/
├── app/
│   ├── routers/           # Endpoints de la API
│   ├── models.py          # Modelos y schemas
│   ├── utils.py           # Utilidades (hashing, etc.)
│   ├── db.py             # Conexión a base de datos
│   └── main.py           # Aplicación principal
├── BaseDatos/
│   ├── docker-compose.yml # Configuración Docker
│   ├── Script_ObligatorioBDII_Grupo5.sql # Esquema de BD
│   └── insert_initial_data.sql # Datos de prueba
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

## Notas Importantes

- Las contraseñas se almacenan hasheadas usando bcrypt
- No se requiere autenticación JWT (removida según especificaciones)
- Todos los endpoints utilizan consultas SQL directas (sin ORM)
- El sistema incluye validación de votos observados
- Los reportes incluyen porcentajes calculados dinámicamente

## Soporte

Para cualquier consulta o problema, revisa la documentación de la API en `/docs` o contacta al equipo de desarrollo.
