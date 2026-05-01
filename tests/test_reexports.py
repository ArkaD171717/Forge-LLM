import forge


def test_version_exists():
    assert isinstance(forge.__version__, str)
    assert forge.__version__ == "0.3.0"


def test_all_lists_submodules():
    assert "session" in forge.__all__
    assert "mtp" in forge.__all__
    assert "context" in forge.__all__


def test_session_reexport():
    from forge.session import ThinkingSession
    from qwen_think import ThinkingSession as Original

    assert ThinkingSession is Original


def test_mtp_recommend_reexport():
    from forge.mtp import recommend
    from qwen3_6_mtp import recommend as original

    assert recommend is original


def test_mtp_quick_crossover_reexport():
    from forge.mtp import quick_crossover
    from qwen3_6_mtp import quick_crossover as original

    assert quick_crossover is original


def test_mtp_vllm_command_reexport():
    from forge.mtp import vllm_mtp_command
    from qwen3_6_mtp import vllm_mtp_command as original

    assert vllm_mtp_command is original


def test_mtp_sglang_command_reexport():
    from forge.mtp import sglang_mtp_command
    from qwen3_6_mtp import sglang_mtp_command as original

    assert sglang_mtp_command is original


def test_mtp_usecase_reexport():
    from forge.mtp import UseCase
    from qwen3_6_mtp import UseCase as original

    assert UseCase is original


def test_mtp_objective_reexport():
    from forge.mtp import Objective
    from qwen3_6_mtp import Objective as original

    assert Objective is original


def test_forge_all_consistent():
    for name in forge.__all__:
        assert hasattr(forge, name), f"forge.__all__ lists '{name}' but it is not defined"


def test_session_all_consistent():
    from forge import session

    for name in session.__all__:
        assert hasattr(session, name), f"session.__all__ lists '{name}' but it is not defined"


def test_mtp_all_consistent():
    from forge import mtp

    for name in mtp.__all__:
        assert hasattr(mtp, name), f"mtp.__all__ lists '{name}' but it is not defined"
