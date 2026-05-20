import json
from pathlib import Path
import pytest
from app.utils import save_json, load_json, save_text, load_text, ensure_dir, timestamp


def test_save_load_json(tmp_path):
    data = {"key": "valeur", "nested": {"x": 1}}
    f = tmp_path / "test.json"
    assert save_json(data, f)
    loaded = load_json(f)
    assert loaded == data


def test_load_json_missing(tmp_path):
    assert load_json(tmp_path / "absent.json") is None


def test_load_json_invalid(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json", encoding="utf-8")
    assert load_json(f) is None


def test_save_load_text(tmp_path):
    f = tmp_path / "sub" / "file.txt"
    assert save_text("bonjour", f)
    assert load_text(f) == "bonjour"


def test_ensure_dir(tmp_path):
    d = tmp_path / "a" / "b" / "c"
    ensure_dir(d)
    assert d.is_dir()


def test_timestamp_format():
    ts = timestamp()
    assert len(ts) == 15  # YYYYMMDD_HHMMSS
    assert "_" in ts
