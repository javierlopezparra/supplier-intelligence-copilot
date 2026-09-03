from ollama import chat


class RAGGenerator:
    def __init__(
        self,
        model: str = "qwen3:4b-instruct",
    ):
        self.model = model

    def generate_answer(
        self,
        question: str,
        contexts: list[dict],
    ) -> str:
        context_text = "\n\n".join(
            (
                f"[Fuente: {item['source']} | "
                f"Chunk: {item['chunk_index']}]\n"
                f"{item['text']}"
            )
            for item in contexts
        )

        system_prompt = """
Eres un asistente de inteligencia de proveedores.

Debes responder utilizando ÚNICAMENTE la información
contenida en el contexto proporcionado.

El contexto puede contener información de uno o varios proveedores.

Reglas:
- No inventes información.
- No uses conocimiento externo.
- Puedes comparar proveedores cuando exista evidencia suficiente.
- Identifica claramente a qué proveedor corresponde cada dato.
- Si el dato solicitado no aparece claramente en el contexto, responde EXACTAMENTE:
  "No hay información suficiente en los documentos disponibles."
- Si no existe información suficiente, NO menciones ninguna fuente.
- Si sí existe información suficiente, responde en español de forma clara,
  breve y profesional.
- Cuando exista una respuesta respaldada, indica al final las fuentes utilizadas.
"""

        user_prompt = f"""
PREGUNTA:
{question}

CONTEXTO:
{context_text}
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response["message"]["content"]