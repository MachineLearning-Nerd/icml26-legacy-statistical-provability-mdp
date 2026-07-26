from reproduction.historical import verify_measure


def test_historical_script_runs() -> None:
    assert verify_measure.main() == 0
