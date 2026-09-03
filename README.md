# Supplier Intelligence Copilot

Asistente de inteligencia de proveedores basado en Inteligencia Artificial y RAG
(Retrieval-Augmented Generation).

El proyecto permite consultar y comparar información contenida en documentos PDF
de proveedores utilizando búsqueda semántica, una base vectorial y un modelo de
lenguaje ejecutado localmente.

> Todos los proveedores y documentos incluidos en este repositorio son ficticios
> y fueron creados exclusivamente con fines de demostración.

---

## Problema

En compras y cadena de suministro es común tener información de proveedores
distribuida entre diferentes documentos.

Por ejemplo:

- tiempos de entrega
- condiciones de pago
- capacidad instalada
- certificaciones
- categorías de productos
- cobertura
- información comercial

Buscar y comparar esta información manualmente puede consumir tiempo y generar
errores.

---

## Solución

Supplier Intelligence Copilot convierte documentos de proveedores en una base
de conocimiento que puede ser consultada mediante preguntas en lenguaje natural.

Actualmente el sistema puede:

- leer varios documentos PDF
- extraer su contenido
- dividir la información en fragmentos
- generar embeddings
- almacenar la información en ChromaDB
- buscar información por significado
- responder preguntas mediante un modelo de IA local
- comparar varios proveedores
- indicar las fuentes utilizadas
- evitar responder cuando la información no existe en los documentos

---

## Ejemplo

Pregunta:

```text
¿Qué proveedor tiene el menor tiempo de entrega?