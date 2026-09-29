import pytest

from src.supplier_evaluator import SupplierEvaluator


SUPPLIERS = [
    {
        "name": "PackPro Norte",
        "lead_time_days": 8,
        "monthly_capacity": 180000,
        "payment_terms_days": 30,
    },
    {
        "name": "Empaques Delta Solutions",
        "lead_time_days": 12,
        "monthly_capacity": 300000,
        "payment_terms_days": 45,
    },
    {
        "name": "NovaPack Industrial Solutions",
        "lead_time_days": 15,
        "monthly_capacity": 250000,
        "payment_terms_days": 30,
    },
    {
        "name": "FlexiPack Mexico",
        "lead_time_days": 20,
        "monthly_capacity": 400000,
        "payment_terms_days": 60,
    },
]


def test_supplier_ranking_order():
    evaluator = SupplierEvaluator()

    ranking = evaluator.evaluate(SUPPLIERS)

    names = [
        supplier["name"]
        for supplier in ranking
    ]

    assert names == [
        "Empaques Delta Solutions",
        "FlexiPack Mexico",
        "PackPro Norte",
        "NovaPack Industrial Solutions",
    ]


def test_supplier_final_scores():
    evaluator = SupplierEvaluator()

    ranking = evaluator.evaluate(SUPPLIERS)

    scores = {
        supplier["name"]: supplier["final_score"]
        for supplier in ranking
    }

    assert scores["Empaques Delta Solutions"] == pytest.approx(
        59.09,
        abs=0.01,
    )

    assert scores["FlexiPack Mexico"] == pytest.approx(
        55.00,
        abs=0.01,
    )

    assert scores["PackPro Norte"] == pytest.approx(
        45.00,
        abs=0.01,
    )

    assert scores["NovaPack Industrial Solutions"] == pytest.approx(
        29.89,
        abs=0.01,
    )


def test_payment_terms_tie():
    evaluator = SupplierEvaluator()

    ranking = evaluator.evaluate(SUPPLIERS)

    suppliers_by_name = {
        supplier["name"]: supplier
        for supplier in ranking
    }

    packpro = suppliers_by_name["PackPro Norte"]

    novapack = suppliers_by_name[
        "NovaPack Industrial Solutions"
    ]

    assert (
        packpro["payment_terms_position"]
        == novapack["payment_terms_position"]
    )

    assert (
        packpro["payment_terms_comparison"]
        == "plazo de pago más corto del grupo"
    )

    assert (
        novapack["payment_terms_comparison"]
        == "plazo de pago más corto del grupo"
    )


def test_weights_must_sum_to_one():
    with pytest.raises(
        ValueError,
        match="Los pesos de evaluación deben sumar 1.00",
    ):
        SupplierEvaluator(
            lead_time_weight=0.50,
            capacity_weight=0.40,
            payment_terms_weight=0.20,
        )


def test_empty_supplier_list():
    evaluator = SupplierEvaluator()

    ranking = evaluator.evaluate([])

    assert ranking == []