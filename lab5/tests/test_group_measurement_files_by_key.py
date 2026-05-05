import pytest
from pathlib import Path
from app.group_measurement_files_by_key import group_measurement_files_by_key


def test_groups_files_by_year_measurement_frequency(tmp_path):
    (tmp_path / "2023_PM10_1g.csv").touch()
    (tmp_path / "2023_NO2_24g.csv").touch()
    result = group_measurement_files_by_key(tmp_path)
    assert ("2023", "PM10", "1g") in result
    assert ("2023", "NO2", "24g") in result


def test_value_is_path_to_file(tmp_path):
    csv_file = tmp_path / "2023_PM10_1g.csv"
    csv_file.touch()
    result = group_measurement_files_by_key(tmp_path)
    assert result[("2023", "PM10", "1g")] == csv_file


def test_ignores_non_csv_files(tmp_path):
    (tmp_path / "2023_PM10_1g.txt").touch()
    (tmp_path / "readme.md").touch()
    result = group_measurement_files_by_key(tmp_path)
    assert len(result) == 0


def test_ignores_subdirectories(tmp_path):
    (tmp_path / "2023_PM10_1g").mkdir()
    (tmp_path / "2023_NO2_1g.csv").touch()
    result = group_measurement_files_by_key(tmp_path)
    assert len(result) == 1
    assert ("2023", "NO2", "1g") in result


def test_raises_for_non_directory(tmp_path):
    file_path = tmp_path / "file.csv"
    file_path.touch()
    with pytest.raises(NotADirectoryError):
        group_measurement_files_by_key(file_path)


@pytest.mark.parametrize("filename,expected_key", [
    ("2023_BaP(PM10)_24g.csv", ("2023", "BaP(PM10)", "24g")),
    ("2022_Hg(TGM)_1g.csv", ("2022", "Hg(TGM)", "1g")),
    ("2023_C6H6_1g.csv", ("2023", "C6H6", "1g")),
])
def test_handles_complex_measurement_names(tmp_path, filename, expected_key):
    (tmp_path / filename).touch()
    result = group_measurement_files_by_key(tmp_path)
    assert expected_key in result
