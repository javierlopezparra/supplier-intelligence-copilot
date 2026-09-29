import json
from pathlib import Path


class SupplierEvaluator:
    def __init__(
        self,
        lead_time_weight: float = 0.45,
        capacity_weight: float = 0.35,
        payment_terms_weight: float = 0.20,
    ):
        self.weights = {
            "lead_time": lead_time_weight,
            "capacity": capacity_weight,
            "payment_terms": payment_terms_weight,
        }

        total_weight = sum(self.weights.values())

        if round(total_weight, 2) != 1.00:
            raise ValueError(
                "Los pesos de evaluación deben sumar 1.00"
            )

    def load_suppliers(
        self,
        file_path: str = "data/structured/suppliers.json",
    ) -> list[dict]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {file_path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def normalize_higher_is_better(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        if maximum == minimum:
            return 100.0

        return (
            (value - minimum)
            / (maximum - minimum)
        ) * 100

    @staticmethod
    def normalize_lower_is_better(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        if maximum == minimum:
            return 100.0

        return (
            (maximum - value)
            / (maximum - minimum)
        ) * 100

    @staticmethod
    def ordinal_label(
        position: int,
        total_positions: int,
        criterion: str,
    ) -> str:
        if total_positions == 1:
            return "único valor del grupo"

        if criterion == "lead_time":
            if position == 1:
                return "menor tiempo de entrega del grupo"

            if position == total_positions:
                return "mayor tiempo de entrega del grupo"

            labels = {
                2: "segundo menor tiempo de entrega del grupo",
                3: "tercer menor tiempo de entrega del grupo",
            }

            return labels.get(
                position,
                f"posición {position} en tiempo de entrega",
            )

        if criterion == "capacity":
            if position == 1:
                return "mayor capacidad del grupo"

            if position == total_positions:
                return "menor capacidad del grupo"

            labels = {
                2: "segunda mayor capacidad del grupo",
                3: "tercera mayor capacidad del grupo",
            }

            return labels.get(
                position,
                f"posición {position} en capacidad",
            )

        if criterion == "payment_terms":
            if position == 1:
                return "plazo de pago más largo del grupo"

            if position == total_positions:
                return "plazo de pago más corto del grupo"

            labels = {
                2: "segundo plazo de pago más largo del grupo",
                3: "tercer plazo de pago más largo del grupo",
            }

            return labels.get(
                position,
                f"posición {position} en plazo de pago",
            )

        return f"posición {position}"

    def evaluate(
        self,
        suppliers: list[dict],
    ) -> list[dict]:
        if not suppliers:
            return []

        lead_times = [
            supplier["lead_time_days"]
            for supplier in suppliers
        ]

        capacities = [
            supplier["monthly_capacity"]
            for supplier in suppliers
        ]

        payment_terms = [
            supplier["payment_terms_days"]
            for supplier in suppliers
        ]

        # Valores únicos para que los empates compartan posición
        lead_time_values = sorted(set(lead_times))

        capacity_values = sorted(
            set(capacities),
            reverse=True,
        )

        payment_values = sorted(
            set(payment_terms),
            reverse=True,
        )

        lead_time_positions = {
            value: position
            for position, value in enumerate(
                lead_time_values,
                start=1,
            )
        }

        capacity_positions = {
            value: position
            for position, value in enumerate(
                capacity_values,
                start=1,
            )
        }

        payment_positions = {
            value: position
            for position, value in enumerate(
                payment_values,
                start=1,
            )
        }

        results = []

        for supplier in suppliers:
            lead_time = supplier["lead_time_days"]
            capacity = supplier["monthly_capacity"]
            payment = supplier["payment_terms_days"]

            lead_time_score = self.normalize_lower_is_better(
                lead_time,
                min(lead_times),
                max(lead_times),
            )

            capacity_score = self.normalize_higher_is_better(
                capacity,
                min(capacities),
                max(capacities),
            )

            payment_score = self.normalize_higher_is_better(
                payment,
                min(payment_terms),
                max(payment_terms),
            )

            final_score = (
                lead_time_score
                * self.weights["lead_time"]
                + capacity_score
                * self.weights["capacity"]
                + payment_score
                * self.weights["payment_terms"]
            )

            lead_time_position = (
                lead_time_positions[lead_time]
            )

            capacity_position = (
                capacity_positions[capacity]
            )

            payment_position = (
                payment_positions[payment]
            )

            results.append(
                {
                    "name": supplier["name"],

                    "lead_time_days":
                        lead_time,

                    "monthly_capacity":
                        capacity,

                    "payment_terms_days":
                        payment,

                    "lead_time_position":
                        lead_time_position,

                    "capacity_position":
                        capacity_position,

                    "payment_terms_position":
                        payment_position,

                    "lead_time_comparison":
                        self.ordinal_label(
                            lead_time_position,
                            len(lead_time_values),
                            "lead_time",
                        ),

                    "capacity_comparison":
                        self.ordinal_label(
                            capacity_position,
                            len(capacity_values),
                            "capacity",
                        ),

                    "payment_terms_comparison":
                        self.ordinal_label(
                            payment_position,
                            len(payment_values),
                            "payment_terms",
                        ),

                    "lead_time_score":
                        round(lead_time_score, 2),

                    "capacity_score":
                        round(capacity_score, 2),

                    "payment_terms_score":
                        round(payment_score, 2),

                    "final_score":
                        round(final_score, 2),
                }
            )

        return sorted(
            results,
            key=lambda supplier:
                supplier["final_score"],
            reverse=True,
        )