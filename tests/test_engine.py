import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from forge.engine import ForgeEngine


@pytest.fixture
def mock_openai():
    with patch("forge.engine.OpenAI") as mock_cls:
        client = MagicMock()
        mock_cls.return_value = client
        yield client


def test_constructor_creates_session(mock_openai):
    engine = ForgeEngine(model="Qwen3.6-27B", base_url="http://localhost:8000/v1")
    assert engine.session is not None
    assert engine._model_short == "Qwen3.6-27B"
    assert engine._model_hf == "Qwen/Qwen3.6-27B"


def test_hf_model_name_parsing(mock_openai):
    engine = ForgeEngine(model="Qwen/Qwen3.6-35B-A3B")
    assert engine._model_short == "Qwen3.6-35B-A3B"
    assert engine._model_hf == "Qwen/Qwen3.6-35B-A3B"


def test_system_prompt_injected(mock_openai):
    engine = ForgeEngine(system_prompt="Be concise.")
    msgs = engine.session.messages
    assert any(m.role == "system" and "Be concise" in m.content for m in msgs)


def test_mtp_recommendation_without_gpu(mock_openai):
    engine = ForgeEngine()
    assert engine.mtp_recommendation is None


def test_mtp_recommendation_with_gpu(mock_openai):
    engine = ForgeEngine(gpu_id="rtx-4090")
    rec = engine.mtp_recommendation
    assert rec is not None
    assert isinstance(rec.enable, bool)
    assert isinstance(rec.expected_gain, str)


def test_chat_delegates_to_session(mock_openai):
    engine = ForgeEngine()
    with patch.object(engine._session, "chat", return_value="response") as mock_chat:
        result = engine.chat("hello")
        mock_chat.assert_called_once()
        assert result == "response"


def test_set_context(mock_openai):
    engine = ForgeEngine()
    engine.set_context("file: main.py\nprint('hello')")
    assert engine.context_pack is not None
    assert engine._context_tokens > 0
    msgs = engine.session.messages
    assert any(m.role == "system" and "main.py" in m.content for m in msgs)


def test_ingest_local(mock_openai):
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "main.py").write_text("print('hello')\n")
        Path(tmp, "utils.py").write_text("def add(a, b): return a + b\n")
        engine = ForgeEngine()
        pack = engine.ingest_local(tmp)
        assert "main.py" in pack
        assert engine.context_pack == pack
        assert engine._context_files > 0
        assert engine._context_tokens > 0


def test_status_structure(mock_openai):
    engine = ForgeEngine(model="Qwen3.6-27B", gpu_id="rtx-4090")
    st = engine.status()
    assert st["model"] == "Qwen3.6-27B"
    assert st["model_hf"] == "Qwen/Qwen3.6-27B"
    assert "budget" in st
    assert "total" in st["budget"]
    assert "mtp" in st
    assert st["mtp"]["enable"] in (True, False)


def test_status_without_context(mock_openai):
    engine = ForgeEngine()
    st = engine.status()
    assert "context" not in st


def test_status_with_context(mock_openai):
    engine = ForgeEngine()
    engine.set_context("some context here")
    st = engine.status()
    assert "context" in st
    assert st["context"]["tokens"] > 0


def test_openai_import_error():
    with patch("forge.engine.OpenAI", None):
        with pytest.raises(ImportError, match="openai"):
            ForgeEngine()


def test_forge_engine_importable_from_top_level():
    from forge import ForgeEngine as FE

    assert FE is ForgeEngine
