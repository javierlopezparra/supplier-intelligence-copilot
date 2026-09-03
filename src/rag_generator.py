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

Reglas:
- No inventes información.
- Si el dato solicitado no aparece en el contexto, responde:
  "No hay información suficiente en los documentos disponibles."
- Responde en español.
- Sé claro, breve y profesional.
- Al final indica la fuente utilizada.
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