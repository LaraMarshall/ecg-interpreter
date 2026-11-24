import pytest

from ecg_interpreter.ecg.interpreter import interpret_ecg
from ecg_interpreter.models.ecg_data import Rhythm, STSegment
from ecg_interpreter.models.interpretation import Interpretation, Diagnosis, Urgency

@pytest.mark.parametrize(
    "fixture_name, expected_diagnosis, expected_urgency",
    [
        ("normal_reading", Diagnosis.NORMAL, Urgency.NONE),
        ("infarction_reading", Diagnosis.INFARCTION, Urgency.URGENT),
        ("suspected_infarction_reading", Diagnosis.SUSPECTED_INFARCTION, Urgency.URGENT),
        ("ischemia_reading", Diagnosis.ISCHEMIA, Urgency.PLANNED),
        ("arrhythmia_reading", Diagnosis.ARRHYTHMIA, Urgency.PLANNED),
        ("previous_infarction_reading", Diagnosis.PREVIOUS_INFARCTION, Urgency.PLANNED)
    ], ids=["normal", "infarction", "suspected_infarction", "ischemia", "arrhythmia", "previous_infarction"]
)
def test_interpret_ecg(request: pytest.FixtureRequest, fixture_name, expected_diagnosis, expected_urgency):
    data = request.getfixturevalue(fixture_name)
    result = interpret_ecg(data)
    assert result.diagnosis == expected_diagnosis, (f"Ожидался диагноз {expected_diagnosis}, получен {result.diagnosis}")
    assert result.urgency == expected_urgency, (f"Ожидался уровень срочности {expected_urgency}, получен {result.urgency}")