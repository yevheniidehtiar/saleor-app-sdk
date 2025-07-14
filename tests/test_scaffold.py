"""
Test script for the Saleor App Scaffold.

This script tests the Copier template to ensure it generates valid projects.
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

DEFAULT_COPIER_ARGS = ["--quiet", "--trust", "--defaults"]


def run_command(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


@pytest.fixture
def scaffold_dir():
    """Get the scaffold directory path."""
    return Path(__file__).parent.parent / "scaffold"


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def copier_test_data():
    """Test data for Copier generation."""
    return {
        "app_name": "test-app",
        "app_display_name": "Test App",
        "app_description": "A test Saleor app",
        "app_version": "0.1.0",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.11",
        "include_docker": True,
        "include_tests": True,
        "saleor_permissions": "MANAGE_ORDERS",
        "app_url": "https://test.example.com",
    }


@pytest.fixture
def minimal_copier_data():
    """Minimal test data for Copier generation."""
    return {
        "app_name": "structure-test",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "include_docker": False,
        "include_tests": False,
    }


@pytest.fixture
def expected_full_files():
    """Expected files for full project generation."""
    return [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "Makefile",
        ".gitignore",
        "src/test_app/__init__.py",
        "src/test_app/main.py",
        "tests/__init__.py",
        "tests/test_main.py",
        "Dockerfile",
        "docker-compose.yml",
    ]


@pytest.fixture
def expected_minimal_files():
    """Expected files for minimal project generation."""
    return [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "Makefile",
        ".gitignore",
        "src/structure_test/__init__.py",
        "src/structure_test/main.py",
    ]


@pytest.fixture
def unexpected_minimal_files():
    """Files that should not be present in minimal project."""
    return ["Dockerfile", "docker-compose.yml", "tests"]


@pytest.fixture(autouse=True)
def check_copier_installed():
    """Check if Copier is installed before running tests."""
    exit_code, _, _ = run_command(["python", "-m", "copier", "--version"])
    if exit_code != 0:
        pytest.skip("Copier is not installed. Install with: pip install copier")


def generate_project_with_copier(
    scaffold_dir: Path, output_dir: Path, data: dict
) -> tuple[int, str, str]:
    """Helper function to generate project with Copier."""
    data_args = []
    for key, value in data.items():
        data_args.extend(["--data", f"{key}={value}"])

    cmd = [
        "python",
        "-m",
        "copier",
        "copy",
        str(scaffold_dir),
        str(output_dir),
        *DEFAULT_COPIER_ARGS,
        *data_args,
    ]

    return run_command(cmd)


def test_copier_generation(
    scaffold_dir, temp_output_dir, copier_test_data, expected_full_files
):
    """Test that Copier can generate a project from the scaffold."""
    output_dir = temp_output_dir / "test-app"

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, copier_test_data
    )

    assert exit_code == 0, (
        f"Copier generation failed. Exit code: {exit_code}, Stderr: {stderr}"
    )

    # Check that expected files were generated
    missing_files = []
    for file_path in expected_full_files:
        full_path = output_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    assert not missing_files, f"Missing expected files: {missing_files}"


def test_generated_project_content(scaffold_dir, temp_output_dir, copier_test_data):
    """Test that generated files have correct content."""
    output_dir = temp_output_dir / "test-app"

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, copier_test_data
    )
    assert exit_code == 0, f"Project generation failed: {stderr}"

    # Check pyproject.toml content
    pyproject_path = output_dir / "pyproject.toml"
    with open(pyproject_path) as f:
        pyproject_content = f.read()

    assert "test-app" in pyproject_content, (
        "Generated pyproject.toml doesn't contain app name"
    )
    assert "Test Author" in pyproject_content, (
        "Generated pyproject.toml doesn't contain author name"
    )

    # Check main.py content
    main_path = output_dir / "src/test_app/main.py"
    with open(main_path) as f:
        main_content = f.read()

    assert "test-app" in main_content, "Generated main.py doesn't contain app name"
    assert "MANAGE_ORDERS" in main_content, (
        "Generated main.py doesn't contain permissions"
    )


def test_generated_project_structure(
    scaffold_dir,
    temp_output_dir,
    minimal_copier_data,
    expected_minimal_files,
    unexpected_minimal_files,
):
    """Test that the generated project has the correct structure."""
    output_dir = temp_output_dir / "structure-test"

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, minimal_copier_data
    )
    assert exit_code == 0, f"Project generation failed: {stderr}"

    # Check that expected files are present
    for file_path in expected_minimal_files:
        full_path = output_dir / file_path
        assert full_path.exists(), f"Missing expected file: {file_path}"

    # Check that unexpected files are NOT present
    for file_path in unexpected_minimal_files:
        full_path = output_dir / file_path
        assert not full_path.exists(), f"Unexpected file present: {file_path}"


def test_python_syntax(scaffold_dir, temp_output_dir):
    """Test that generated Python files have valid syntax."""
    output_dir = temp_output_dir / "syntax-test"

    syntax_data = {
        "app_name": "syntax-test",
        "author_name": "Test Author",
        "author_email": "test@example.com",
    }

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, syntax_data
    )
    assert exit_code == 0, f"Project generation failed: {stderr}"

    # Find all Python files
    python_files = list(output_dir.rglob("*.py"))
    assert python_files, "No Python files found in generated project"

    # Check syntax by compiling each file
    for py_file in python_files:
        with open(py_file) as f:
            content = f.read()

        try:
            compile(content, str(py_file), "exec")
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")
        except Exception as e:
            pytest.fail(f"Error checking {py_file}: {e}")


def test_copier_data_validation_error(scaffold_dir, temp_output_dir):
    """Test that Copier handles invalid data appropriately."""
    output_dir = temp_output_dir / "validation-test"

    # Test with missing required fields
    invalid_data = {
        "app_name": "validation-test"
        # Missing author_name and author_email
    }

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, invalid_data
    )

    assert exit_code == 1
    assert 'Question "author_name" is required' in stderr


@pytest.mark.parametrize(
    "docker_flag,tests_flag",
    [(True, True), (True, False), (False, True), (False, False)],
)
def test_optional_features_combinations(
    scaffold_dir, temp_output_dir, docker_flag, tests_flag
):
    """Test different combinations of optional features."""
    output_dir = temp_output_dir / f"combo-docker-{docker_flag}-tests-{tests_flag}"

    combo_data = {
        "app_name": "combo-test",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "include_docker": docker_flag,
        "include_tests": tests_flag,
    }

    exit_code, stdout, stderr = generate_project_with_copier(
        scaffold_dir, output_dir, combo_data
    )
    assert exit_code == 0, f"Project generation failed: {stderr}"

    # Check Docker files
    docker_files = ["Dockerfile", "docker-compose.yml"]
    for docker_file in docker_files:
        file_path = output_dir / docker_file
        if docker_flag:
            assert file_path.exists(), (
                f"Docker file {docker_file} should exist when include_docker=True"
            )
        else:
            assert not file_path.exists(), (
                f"Docker file {docker_file} should not exist when include_docker=False"
            )

    # Check test files
    tests_dir = output_dir / "tests"
    if tests_flag:
        assert tests_dir.exists(), (
            "Tests directory should exist when include_tests=True"
        )
        assert (tests_dir / "test_main.py").exists(), (
            "test_main.py should exist when include_tests=True"
        )
    else:
        assert not tests_dir.exists(), (
            "Tests directory should not exist when include_tests=False"
        )
