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
                f"{supplier['lead_time_days']} días\n"
                f"Capacidad mensual: "
                f"{supplier['monthly_capacity']:,} unidades\n"
                f"Condiciones de pago: "
                f"{supplier['payment_terms_days']} días\n"
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

El ranking y los puntajes finales ya fueron calculados por Python.
Tu función es únicamente explicar los resultados.

REGLAS OBLIGATORIAS:
- NO recalcules los puntajes.
- NO modifiques los puntajes finales.
- NO cambies el orden del ranking.
- Utiliza únicamente los valores reales proporcionados.
- NO inventes requisitos, SLA, límites o criterios.
- NO afirmes que un proveedor incumple o no es viable.
- NO inventes puntajes parciales.
- Menciona el puntaje final, pero explica usando los datos reales.
- Usa máximo 2 puntos por proveedor.
- Usa máximo 180 palabras en total.
- Termina con una conclusión de máximo 2 líneas.
- Responde en español.
- Sé breve, profesional y fácil de entender.
"""

        user_prompt = f"""
PESOS UTILIZADOS POR EL MOTOR DE PYTHON:

{weights_text}

RANKING Y DATOS REALES:

{ranking_text}

Explica brevemente por qué los proveedores quedaron en ese orden.
No realices cálculos nuevos.
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