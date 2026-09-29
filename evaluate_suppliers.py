from src.ranking_explainer import RankingExplainer
from src.supplier_evaluator import SupplierEvaluator


def main():
    evaluator = SupplierEvaluator()

    suppliers = evaluator.load_suppliers()

    ranking = evaluator.evaluate(suppliers)

    print("=" * 60)
    print("SUPPLIER EVALUATION ENGINE")
    print("=" * 60)

    for position, supplier in enumerate(
        ranking,
        start=1,
    ):
        print()
        print(f"{position}. {supplier['name']}")
        print(
            f"   Lead Time Score: "
            f"{supplier['lead_time_score']}"
        )
        print(
            f"   Capacity Score: "
            f"{supplier['capacity_score']}"
        )
        print(
            f"   Payment Terms Score: "
            f"{supplier['payment_terms_score']}"
        )
        print(
            f"   FINAL SCORE: "
            f"{supplier['final_score']}"
        )

    print()
    print("=" * 60)
    print("EXPLICACIÓN CON IA")
    print("=" * 60)
    print()

    explainer = RankingExplainer()

    explanation = explainer.explain(
        ranking=ranking,
        weights=evaluator.weights,
    )

    print(explanation)

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()