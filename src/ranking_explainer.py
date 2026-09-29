from ollama import chat


class RankingExplainer:
    def __init__(
        self,
        model: str = "qwen3:4b-instruct",
    ):
        self.model = model

    def explain(
        self,
        ranking: list[dict],
        weights: dict,
    ) -> str:
        ranking_text = "\n".join(
            (
                f"{position}. {supplier['name']}\n"
                f"Tiempo de entrega: "
                f"{supplier['lead_time_days']} días "
                f"({supplier['lead_time_comparison']})\n"
                f"Capacidad mensual: "
                f"{supplier['monthly_capacity']:,} unidades "
                f"({supplier['capacity_comparison']})\n"
                f"Condiciones de pago: "
                f"{supplier['payment_terms_days']} días "
                f"({supplier['payment_terms_comparison']})\n"
                f"Puntaje final calculado por Python: "
                f"{supplier['final_score']}\n"
            )
            for position, supplier in enumerate(
                ranking,
                start=1,
            )
        )

        weights_text = (
            f"Tiempo de entrega: "
            f"{weights['lead_time'] * 100:.0f}%\n"
            f"Capacidad: "
            f"{weights['capacity'] * 100:.0f}%\n"
            f"Condiciones de pago: "
            f"{weights['payment_terms'] * 100:.0f}%"
        )

        system_prompt = """
Eres un asistente especializado en evaluación de proveedores.

Python ya calculó:
- los puntajes,
- el orden del ranking,
- y las comparaciones relativas de cada criterio.

Tu única función es redactar una explicación clara.

REGLAS OBLIGATORIAS:
- NO recalcules ningún dato.
- NO cambies el orden del ranking.
- NO contradigas las comparaciones proporcionadas por Python.
- NO decidas por tu cuenta qué valor es mayor o menor.
- Utiliza las etiquetas comparativas exactamente como referencia.
- NO inventes requisitos, SLA, límites o criterios.
- NO afirmes que un proveedor incumple o no es viable.
- NO inventes puntajes parciales.
- Menciona los valores reales y el puntaje final.
- Usa máximo 2 puntos por proveedor.
- Usa máximo 180 palabras en total.
- Termina con una conclusión de máximo 2 líneas.
- Responde en español.
- Sé breve, profesional y fácil de entender.
"""

        user_prompt = f"""
PESOS UTILIZADOS POR PYTHON:

{weights_text}

RANKING, DATOS Y COMPARACIONES CALCULADAS POR PYTHON:

{ranking_text}

Explica brevemente el ranking.
No realices ninguna comparación nueva.
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
            think=False,
            options={
                "temperature": 0,
                "num_predict": 400,
            },
        )

        return response["message"]["content"]