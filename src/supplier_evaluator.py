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

        return ((value - minimum) / (maximum - minimum)) * 100

    @staticmethod
    def normalize_lower_is_better(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        if maximum == minimum:
            return 100.0

        return ((maximum - value) / (maximum - minimum)) * 100

    def evaluate(self, suppliers: list[dict]) -> list[dict]:
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

        results = []

        for supplier in suppliers:
            lead_time_score = self.normalize_lower_is_better(
                supplier["lead_time_days"],
                min(lead_times),
                max(lead_times),
            )

            capacity_score = self.normalize_higher_is_better(
                supplier["monthly_capacity"],
                min(capacities),
                max(capacities),
            )

            payment_score = self.normalize_higher_is_better(
                supplier["payment_terms_days"],
                min(payment_terms),
                max(payment_terms),
            )

            final_score = (
                lead_time_score * self.weights["lead_time"]
                + capacity_score * self.weights["capacity"]
                + payment_score * self.weights["payment_terms"]
            )

            results.append(
                {
                    "name": supplier["name"],
                    "lead_time_score": round(lead_time_score, 2),
                    "capacity_score": round(capacity_score, 2),
                    "payment_terms_score": round(payment_score, 2),
                    "final_score": round(final_score, 2),
                }
            )

        return sorted(
            results,
            key=lambda supplier: supplier["final_score"],
            reverse=True,
        )