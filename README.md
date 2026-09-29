# Supplier Intelligence Copilot

[![Supplier Copilot Tests](https://github.com/javierlopezparra/supplier-intelligence-copilot/actions/workflows/tests.yml/badge.svg)](https://github.com/javierlopezparra/supplier-intelligence-copilot/actions/workflows/tests.yml)

Asistente de Inteligencia Artificial para consultar, comparar y evaluar información de proveedores.

El proyecto combina **RAG (Retrieval-Augmented Generation)**, búsqueda semántica, una base de datos vectorial y un motor de evaluación determinístico desarrollado en Python.

La idea principal es separar dos responsabilidades:

- **Python calcula y aplica reglas de negocio.**
- **El modelo de IA recupera información y explica resultados.**

> Todos los proveedores y datos utilizados en este repositorio son ficticios y fueron creados únicamente para demostración.

---

## ¿Qué problema busca resolver?

En compras y cadena de suministro es común encontrar información de proveedores distribuida entre diferentes documentos:

- fichas técnicas
- cotizaciones
- documentos comerciales
- certificados
- contratos
- presentaciones
- archivos PDF

Información como:

- tiempos de entrega
- condiciones de pago
- capacidad instalada
- certificaciones
- productos
- cobertura

puede terminar dispersa entre múltiples fuentes.

Consultar, comparar y evaluar esta información manualmente puede tomar tiempo y generar errores.

**Supplier Intelligence Copilot** explora cómo utilizar Inteligencia Artificial para convertir esos documentos en información consultable y apoyar el análisis de proveedores.

---

# ¿Qué puede hacer actualmente?

El proyecto puede:

- leer múltiples documentos PDF
- extraer texto automáticamente
- dividir documentos en fragmentos
- generar embeddings multilingües
- almacenar información en ChromaDB
- realizar búsquedas semánticas
- responder preguntas mediante RAG
- comparar información entre proveedores
- identificar las fuentes utilizadas
- aplicar un fallback cuando no existe evidencia suficiente en los documentos
- ejecutar un modelo de lenguaje local con Ollama
- calcular un ranking de proveedores mediante Python
- normalizar diferentes criterios de evaluación
- manejar empates entre proveedores
- explicar el ranking utilizando IA
- detectar documentos nuevos o modificados
- reutilizar embeddings de documentos que no cambiaron
- ejecutar pruebas automatizadas con pytest
- validar automáticamente mediante GitHub Actions la lógica cubierta por las pruebas

---

# Ejemplos de uso

## Consulta documental

Pregunta:

```text
¿Qué proveedor tiene el menor tiempo de entrega?
```

Respuesta:

```text
El proveedor con el menor tiempo de entrega es PackPro Norte,
con un tiempo de entrega de 8 días calendario.

Fuentes utilizadas:
- [Fuente: packpro_norte_supplier.pdf | Chunk: 0]
```

También se pueden realizar preguntas como:

```text
¿Qué certificaciones tiene NovaPack?

¿Cuál proveedor tiene mayor capacidad mensual?

Compara los tiempos de entrega de todos los proveedores.

Compara capacidad, tiempo de entrega y condiciones de pago.
```

Cuando la información solicitada no está disponible en los documentos:

```text
No hay información suficiente en los documentos disponibles.
```

---

# Ranking de proveedores

Además del RAG documental, el proyecto incluye un motor de evaluación de proveedores desarrollado en Python.

Desde la aplicación se puede escribir:

```text
ranking
```

para obtener una evaluación estructurada de los proveedores.

El motor utiliza actualmente tres criterios:

| Criterio | Peso |
|---|---:|
| Tiempo de entrega | 45% |
| Capacidad mensual | 35% |
| Condiciones de pago | 20% |

Los valores se normalizan en una escala relativa de **0 a 100**.

Para esta demostración:

- menor tiempo de entrega = mayor puntuación
- mayor capacidad mensual = mayor puntuación
- mayor plazo de pago = mayor puntuación desde la perspectiva del comprador

Los pesos utilizados corresponden únicamente al caso demostrativo y pueden modificarse desde el motor de evaluación.

---

## Resultado actual del caso demo

| Posición | Proveedor | Puntaje |
|---:|---|---:|
| 1 | Empaques Delta Solutions | 59.09 |
| 2 | FlexiPack Mexico | 55.00 |
| 3 | PackPro Norte | 45.00 |
| 4 | NovaPack Industrial Solutions | 29.89 |

Estos puntajes son **relativos al conjunto de proveedores evaluado**.

Por esta razón:

- un puntaje de 100 no significa que un proveedor sea perfecto
- un puntaje de 0 no significa que un proveedor sea inviable

El resultado depende de los proveedores comparados, los criterios seleccionados y los pesos configurados.

---

# Separación entre Python e Inteligencia Artificial

Una decisión importante de arquitectura fue evitar que el modelo de lenguaje realizara los cálculos críticos del ranking.

```text
Python
│
├── calcula puntuaciones
├── normaliza criterios
├── aplica los pesos
├── genera el ranking
├── identifica posiciones relativas
├── maneja empates
└── determina comparaciones objetivas

Ollama + Qwen3
│
└── explica los resultados en lenguaje natural
```

Por ejemplo, Python determina:

```text
FlexiPack Mexico

Capacidad mensual:
400,000 unidades

Comparación:
mayor capacidad del grupo
```

El modelo de IA recibe esta información ya calculada y genera una explicación en lenguaje natural.

Esto permite que los resultados numéricos sean:

- repetibles
- verificables
- independientes del comportamiento generativo del LLM

El modelo explica el resultado, pero no modifica el ranking calculado por Python.

---

# Arquitectura general

El proyecto tiene actualmente dos flujos principales.

## 1. Consulta documental con RAG

```text
PDF de proveedores
        ↓
Extracción de texto
        ↓
Chunking
        ↓
Embeddings multilingües
        ↓
ChromaDB
        ↓
Búsqueda semántica
        ↓
Contexto relevante
        ↓
Ollama + Qwen3
        ↓
Respuesta basada en evidencia
```

## 2. Evaluación estructurada

```text
Datos estructurados de proveedores
        ↓
SupplierEvaluator
        ↓
Normalización
        ↓
Aplicación de pesos
        ↓
Ranking
        ↓
Comparaciones calculadas por Python
        ↓
RankingExplainer
        ↓
Explicación con IA
```

---

# Indexación incremental

Los documentos no se vuelven a procesar innecesariamente cada vez que inicia la aplicación.

El sistema calcula una huella digital **SHA-256** de cada PDF.

```text
Documento
    ↓
SHA-256
    ↓
¿Cambió desde la última indexación?
    │
    ├── NO → reutilizar vectores existentes
    │
    └── SÍ → volver a procesar e indexar
```

Ejemplo:

```text
Vectors stored: 4
Documentos indexados: 0
Documentos reutilizados: 4
```

Esto evita volver a:

- extraer texto
- generar chunks
- calcular embeddings
- reemplazar vectores

cuando un documento no ha cambiado.

Si un PDF desaparece de la carpeta de entrada, sus vectores también pueden eliminarse del índice.

---

# RAG

**RAG** significa **Retrieval-Augmented Generation**.

En lugar de pedirle al modelo de lenguaje que responda únicamente utilizando su conocimiento interno, primero se recupera información relevante de los documentos.

```text
Pregunta
   ↓
Buscar evidencia relevante
   ↓
Entregar evidencia al modelo
   ↓
Generar respuesta
```

Esto permite que las respuestas estén fundamentadas en documentos específicos del proyecto.

---

# Embeddings

Los embeddings convierten texto en representaciones numéricas que capturan su significado.

El proyecto utiliza el modelo multilingüe:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Esto permite que una pregunta en español como:

```text
¿Cuánto tarda el proveedor en entregar?
```

pueda recuperar información escrita como:

```text
Lead Time: 15 calendar days
```

aunque las palabras utilizadas no sean exactamente iguales.

---

# ChromaDB

ChromaDB funciona como base de datos vectorial.

Almacena información como:

- fragmentos de documentos
- embeddings
- nombre del documento
- número de chunk
- hash SHA-256 del documento

Posteriormente permite recuperar los fragmentos semánticamente más cercanos a una pregunta.

---

# Ollama y Qwen3

El proyecto utiliza:

```text
qwen3:4b-instruct
```

mediante Ollama.

Esto permite ejecutar el modelo de lenguaje localmente para la demostración actual, sin depender de una API pagada por cada consulta.

El LLM se utiliza principalmente para:

- generar respuestas a partir del contexto recuperado
- comparar información documental recuperada
- explicar resultados previamente calculados por Python

---

# Control de respuestas sin evidencia

El prompt del sistema indica al modelo que utilice únicamente la información recuperada de los documentos.

Cuando no existe evidencia suficiente, el sistema utiliza el siguiente fallback:

```text
No hay información suficiente en los documentos disponibles.
```

Este mecanismo busca reducir respuestas no sustentadas.

Sin embargo, al tratarse de un modelo generativo, este control no debe interpretarse como una garantía absoluta contra errores o alucinaciones.

---

# Proveedores ficticios utilizados

| Proveedor | Entrega | Capacidad mensual | Pago |
|---|---:|---:|---:|
| PackPro Norte | 8 días | 180,000 | 30 días |
| Empaques Delta Solutions | 12 días | 300,000 | 45 días |
| NovaPack Industrial Solutions | 15 días | 250,000 | 30 días |
| FlexiPack Mexico | 20 días | 400,000 | 60 días |

Todos los datos fueron creados únicamente para demostrar el funcionamiento del sistema.

---

# Tecnologías utilizadas

## Inteligencia Artificial

- Ollama
- Qwen3 4B Instruct
- Sentence Transformers
- Retrieval-Augmented Generation
- Embeddings
- Prompt Engineering

## Backend y datos

- Python
- PyPDF
- ChromaDB
- NumPy
- JSON
- SHA-256

## Calidad y desarrollo

- pytest
- Git
- GitHub
- GitHub Actions
- Visual Studio Code

---

# Estructura del proyecto

```text
supplier-intelligence-copilot/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   ├── raw/
│   │   ├── empaques_delta_supplier.pdf
│   │   ├── flexipack_mexico_supplier.pdf
│   │   ├── packpro_norte_supplier.pdf
│   │   └── sample_supplier.pdf
│   │
│   ├── structured/
│   │   └── suppliers.json
│   │
│   └── vector_store/
│
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── embedding_model.py
│   ├── rag_generator.py
│   ├── ranking_explainer.py
│   ├── semantic_search.py
│   ├── supplier_evaluator.py
│   ├── text_chunker.py
│   └── vector_store.py
│
├── tests/
│   └── test_supplier_evaluator.py
│
├── app.py
├── evaluate_suppliers.py
├── requirements.txt
├── .gitignore
├── .gitattributes
├── .env.example
├── LICENSE
└── README.md
```

> `data/vector_store/` se genera localmente y no se almacena en GitHub.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/javierlopezparra/supplier-intelligence-copilot.git
```

Entrar al proyecto:

```bash
cd supplier-intelligence-copilot
```

---

## 2. Crear un entorno virtual

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

## 4. Instalar y preparar Ollama

Ollama debe estar instalado en el equipo.

Después se puede descargar o ejecutar el modelo utilizado por el proyecto:

```bash
ollama run qwen3:4b-instruct
```

Una vez descargado, el modelo queda disponible localmente para las siguientes ejecuciones.

---

# Ejecutar el proyecto

```bash
python app.py
```

La aplicación mostrará:

```text
COPILOT READY

Puedes:
- Hacer preguntas sobre los proveedores.
- Escribir 'ranking' para ver la evaluación.
- Escribir 'explicar ranking' para obtener el análisis con IA.
- Escribir 'salir' para terminar.

Pregunta >
```

---

# Comandos disponibles

## Consulta documental

Ejemplo:

```text
¿Cuál proveedor tiene la mayor capacidad mensual?
```

## Mostrar ranking

```text
ranking
```

## Explicar ranking utilizando IA

```text
explicar ranking
```

## Finalizar la sesión

```text
salir
```

---

# Pruebas automatizadas

El proyecto utiliza **pytest** para validar la lógica crítica del motor de evaluación.

Ejecutar:

```bash
python -m pytest -v
```

Actualmente las pruebas verifican:

- orden correcto del ranking
- puntajes finales esperados
- manejo de empates
- validación de los pesos
- comportamiento con una lista vacía

Resultado actual:

```text
5 passed
```

Estas pruebas se concentran actualmente en `SupplierEvaluator`.

Las demás capas del proyecto, como RAG, ChromaDB y Ollama, todavía requieren ampliar la cobertura automatizada.

---

# Integración continua

El repositorio utiliza **GitHub Actions** para ejecutar automáticamente las pruebas existentes.

El workflow se encuentra en:

```text
.github/workflows/tests.yml
```

Se ejecuta cuando:

- se realiza un `push` hacia `main`
- se abre o actualiza un Pull Request hacia `main`

Flujo actual:

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Ubuntu
        ↓
Python 3.13
        ↓
pytest
        ↓
PASS / FAIL
```

Actualmente GitHub Actions valida automáticamente la lógica cubierta por las pruebas de `SupplierEvaluator`.

---

# Estado actual

## Completado

- ✅ Lectura de múltiples PDF
- ✅ Extracción de texto
- ✅ Chunking
- ✅ Embeddings multilingües
- ✅ Búsqueda semántica
- ✅ ChromaDB persistente
- ✅ RAG
- ✅ Modelo local con Ollama
- ✅ Comparación entre proveedores
- ✅ Identificación de fuentes por archivo y chunk
- ✅ Fallback cuando no existe evidencia suficiente
- ✅ Conversación interactiva
- ✅ Motor de evaluación de proveedores
- ✅ Ranking determinístico en Python
- ✅ Normalización de criterios
- ✅ Pesos configurables desde el motor de evaluación
- ✅ Manejo de empates
- ✅ Comparaciones relativas calculadas por Python
- ✅ Explicación del ranking mediante IA
- ✅ Indexación incremental mediante SHA-256
- ✅ Pruebas automatizadas con pytest
- ✅ Integración continua con GitHub Actions

---

# Próximas etapas

- ⏳ ampliar las pruebas automatizadas
- ⏳ pruebas del flujo RAG
- ⏳ API REST con FastAPI
- ⏳ interfaz web
- ⏳ configuración interactiva de pesos
- ⏳ mejores citas por página y sección
- ⏳ Docker
- ⏳ pipeline de CI/CD más completo
- ⏳ despliegue en nube
- ⏳ integración con otros proveedores de LLM
- ⏳ evaluación y monitoreo del sistema RAG
- ⏳ separación completa entre proceso de ingesta y proceso de consulta

---

# Limitaciones actuales

Este proyecto se encuentra en desarrollo y utiliza un conjunto de datos demostrativo.

Actualmente:

- los proveedores y sus datos son ficticios
- los pesos del ranking corresponden al caso demo
- los puntajes son relativos al grupo evaluado
- las fuentes se identifican principalmente mediante archivo y chunk
- todavía no existen citas robustas por página
- las pruebas automatizadas cubren principalmente el motor de evaluación
- todavía no existe una interfaz web
- Ollama debe ejecutarse localmente
- el proyecto aún no está desplegado como servicio en nube

Estas limitaciones forman parte de las siguientes etapas de desarrollo.

---

# Principio de diseño

El proyecto busca que la Inteligencia Artificial **apoye el análisis sin sustituir la lógica verificable del sistema ni la decisión del usuario**.

```text
Datos
  ↓
Python calcula
  ↓
IA explica
  ↓
Usuario decide
```

La intención es combinar capacidades generativas con cálculos determinísticos que puedan ser revisados y reproducidos.

---

# Autor

**Javier Alfonso López Parra**

Supply Chain | Planeación de Materiales | Compras Estratégicas | Analítica de Datos | Inteligencia Artificial
