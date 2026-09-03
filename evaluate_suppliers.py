from src.supplier_evaluator import SupplierEvaluator


def main():
    evaluator = SupplierEvaluator()

    suppliers = evaluator.load_suppliers()

    ranking = evaluator.evaluate(suppliers)

    print("=" * 60)
    print("SUPPLIER EVALUATION ENGINE")
    print("=" * 60)

    for position, supplier in enumerate(ranking, start=1):
        print()
        print(f"{position}. {supplier['name']}")
        print(f"   Lead Time Score: {supplier['lead_time_score']}")
        print(f"   Capacity Score: {supplier['capacity_score']}")
        print(f"   Payment Terms Score: {supplier['payment_terms_score']}")
        print(f"   FINAL SCORE: {supplier['final_score']}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()