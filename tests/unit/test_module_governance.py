"""Governance checks for target-oracle module structure."""

from __future__ import annotations

import ast
from pathlib import Path

from tests import c, m, t


def _package_root() -> Path:
    parent_depth = int(c.TargetOracle.Tests.PROJECT_ROOT_PARENT_DEPTH)
    return Path(
        Path(__file__).resolve().parents[parent_depth]
        / c.TargetOracle.Tests.SRC_DIR
        / c.TargetOracle.Tests.PACKAGE_DIR
    )


def _iter_package_modules() -> t.MutableSequenceOf[Path]:
    return sorted(_package_root().rglob("*.py"))


def _read_module_tree(module_path: Path) -> ast.Module:
    return ast.parse(module_path.read_text(encoding="utf-8"), filename=str(module_path))


class TestsFlextTargetOracleModuleGovernance:
    """Behavior contract for test_module_governance."""

    def test_package_modules_do_not_define_module_level_loggers(self) -> None:
        violations: t.MutableSequenceOf[str] = []
        for module_path in _iter_package_modules():
            module_tree = _read_module_tree(module_path)
            for node in module_tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                if any(
                    isinstance(target, ast.Name) and target.id in {"logger", "_logger"}
                    for target in node.targets
                ):
                    violations.append(
                        str(module_path.relative_to(_package_root().parent))
                    )
        assert not violations, (
            f"Module-level logger assignments are forbidden: {violations}"
        )

    def test_package_modules_do_not_define_unapproved_top_level_functions(self) -> None:
        violations: t.MutableSequenceOf[str] = []
        for module_path in _iter_package_modules():
            relative_module_path = str(module_path.relative_to(_package_root()))
            allowed_functions = c.TargetOracle.Tests.ALLOWED_MODULE_FUNCTIONS.get(
                relative_module_path,
                frozenset(),
            )
            module_tree = _read_module_tree(module_path)
            unexpected_functions = sorted(
                node.name
                for node in module_tree.body
                if isinstance(node, ast.FunctionDef)
                and node.name not in allowed_functions
            )
            if unexpected_functions:
                violations.append(
                    f"{module_path.relative_to(_package_root().parent)}: {unexpected_functions}",
                )
        assert not violations, (
            "Top-level functions are forbidden outside approved entrypoints: "
            f"{violations}"
        )

    def test_target_oracle_namespace_does_not_wrap_meltano_singer_models(self) -> None:
        assert hasattr(m.TargetOracle, "SingerStreamModel")
        assert not hasattr(m.TargetOracle, "Meltano")
        assert not hasattr(m.TargetOracle, "SingerSchemaMessage")
        assert not hasattr(m.TargetOracle, "SingerRecordMessage")
        assert not hasattr(m.TargetOracle, "SingerStateMessage")
        assert not hasattr(m.TargetOracle, "SingerActivateVersionMessage")
        assert not hasattr(m.TargetOracle, "SingerCatalogMetadata")
        assert not hasattr(m.TargetOracle, "SingerCatalogEntry")
        assert not hasattr(m.TargetOracle, "SingerCatalog")
