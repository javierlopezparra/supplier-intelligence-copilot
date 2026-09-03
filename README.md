# Supplier Intelligence Copilot

Asistente de Inteligencia Artificial para consultar y comparar información de proveedores.

El proyecto utiliza RAG (Retrieval-Augmented Generation) para responder preguntas basándose en documentos PDF de proveedores.

> Todos los proveedores y datos utilizados en este proyecto son ficticios y fueron creados únicamente para demostración.

---

## ¿Qué problema busca resolver?

En compras y cadena de suministro es común tener información de proveedores distribuida en diferentes documentos.

Por ejemplo:

- tiempos de entrega
- condiciones de pago
- capacidad instalada
- certificaciones
- productos
- cobertura

Consultar y comparar esta información manualmente puede tomar tiempo y generar errores.

---

## ¿Qué hace el proyecto?

Supplier Intelligence Copilot permite cargar varios documentos PDF de proveedores y hacer preguntas en lenguaje natural.

Actualmente puede:

- leer varios PDF
- extraer su información
- buscar información por significado
- comparar proveedores
- responder utilizando un modelo de IA local
- mostrar las fuentes utilizadas
- evitar inventar respuestas cuando el dato no existe

---

## Ejemplo

Pregunta:

```text
¿Qué proveedor tiene el menor tiempo de entrega?
```

Respuesta:

```text
El proveedor con el menor tiempo de entrega es PackPro Norte,
con un tiempo de entrega de 8 días calendario.

Fuente: packpro_norte_supplier.pdf
```

También se pueden hacer preguntas como:

```text
¿Qué certificaciones tiene el proveedor?

¿Cuál tiene mayor capacidad mensual?

Compara los tiempos de entrega de todos los proveedores.

Compara capacidad, tiempo de entrega y condiciones de pago.

¿Cuál es el RFC del proveedor?
```

Si la información no existe, responde:

```text
No hay información suficiente en los documentos disponibles.
```

---

## ¿Cómo funciona?

```text
Documentos PDF
      ↓
Extracción de texto
      ↓
División del texto en fragmentos
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Búsqueda de información relevante
      ↓
Ollama + Qwen3
      ↓
Respuesta con evidencia
```

---

## Conceptos principales

### RAG

RAG permite que la Inteligencia Artificial consulte documentos antes de responder.

En lugar de depender únicamente del conocimiento del modelo:

```text
Pregunta
   ↓
Buscar información en los documentos
   ↓
Entregar esa información al modelo
   ↓
Generar respuesta
```

### Embeddings

Los embeddings convierten texto en números que representan su significado.

Esto permite que una pregunta en español como:

```text
¿Cuánto tarda el proveedor en entregar?
```

pueda encontrar información como:

```text
Lead Time: 15 calendar days
```

aunque las palabras no sean exactamente iguales.

### ChromaDB

Es la base de datos donde guardamos los embeddings y la información de los documentos para poder buscarla posteriormente.

### Ollama

Permite ejecutar el modelo de Inteligencia Artificial localmente en la computadora, sin necesidad de pagar una API por cada consulta.

---

## Tecnologías

- Python
- PyPDF
- Sentence Transformers
- ChromaDB
- Ollama
- Qwen3 4B Instruct
- Git
- GitHub

---

## Proveedores ficticios utilizados

| Proveedor | Entrega | Capacidad mensual | Pago |
|---|---:|---:|---:|
| PackPro Norte | 8 días | 180,000 unidades | 30 días |
| Empaques Delta Solutions | 12 días | 300,000 unidades | 45 días |
| NovaPack Industrial Solutions | 15 días | 250,000 unidades | 30 días |
| FlexiPack Mexico | 20 días | 400,000 unidades | 60 días |

---

## Ejecutar el proyecto

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Verificar el modelo de Ollama:

```bash
ollama run qwen3:4b-instruct
```

Ejecutar:

```bash
python app.py
```

El sistema mostrará:

```text
COPILOT READY
Puedes preguntar o comparar proveedores.
Escribe 'salir' para terminar.

Pregunta >
```

---

## Estado del proyecto

Completado:

- ✅ Lectura de múltiples PDF
- ✅ Extracción de texto
- ✅ Embeddings
- ✅ Búsqueda semántica
- ✅ ChromaDB
- ✅ RAG
- ✅ Ollama
- ✅ Comparación entre proveedores
- ✅ Fuentes
- ✅ Control básico de respuestas inventadas
- ✅ Conversación interactiva

Próximas etapas:

- ⏳ Motor de evaluación de proveedores
- ⏳ API
- ⏳ Interfaz web
- ⏳ Docker
- ⏳ Pruebas automatizadas
- ⏳ Despliegue en nube

---

## Próxima etapa

El siguiente objetivo es crear un motor de evaluación de proveedores.

Python realizará los cálculos y el modelo de IA explicará los resultados.

```text
Datos de proveedores
        ↓
Cálculos con Python
        ↓
Puntuación
        ↓
IA explica el resultado
```

La intención es que los cálculos importantes sean repetibles y no dependan únicamente de lo que decida el modelo de lenguaje.

---

## Autor

Javier Alfonso López Parra

Supply Chain | Planeación de Materiales | Compras | Analítica de Datos | Inteligencia Artificial