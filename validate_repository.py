#!/usr/bin/env python3
"""Проверки целостности репозитория ФОС.

Запуск:
    python3 validate_repository.py            # проверить (для CI / pre-commit)
    python3 validate_repository.py --update   # перегенерировать артефакты

Сейчас реализована одна проверка — соответствие файла repository-tree.txt
фактическому составу репозитория. Источник истины — список отслеживаемых
git-файлов (`git ls-files`), поэтому в дерево не попадают игнорируемые файлы
(.venv, __pycache__, локальные отчёты и т. п.) и оно не расходится с содержимым
репозитория. Новые проверки добавляются в список CHECKS в конце файла.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
TREE_FILE = REPO_ROOT / "repository-tree.txt"

# Символы для отрисовки дерева.
BRANCH = "├── "
LAST = "└── "
PIPE = "│   "
SPACE = "    "


def tracked_files() -> list[str]:
    """Отслеживаемые git-файлы репозитория, относительными путями."""
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line]


def build_tree(paths: list[str]) -> dict:
    """Вложенный словарь каталогов из плоского списка путей.

    Каталог — вложенный dict, файл — None.
    """
    root: dict = {}
    for path in paths:
        node = root
        parts = path.split("/")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = None
    return root


def _sort_key(item: tuple[str, object]) -> tuple[int, str]:
    """Каталоги раньше файлов, затем по имени без учёта регистра."""
    name, child = item
    is_file = 1 if child is None else 0
    return (is_file, name.lower())


def render(node: dict, prefix: str = "") -> list[str]:
    """Строки дерева для одного уровня (рекурсивно)."""
    lines: list[str] = []
    items = sorted(node.items(), key=_sort_key)
    for index, (name, child) in enumerate(items):
        last = index == len(items) - 1
        connector = LAST if last else BRANCH
        suffix = "/" if child is not None else ""
        lines.append(f"{prefix}{connector}{name}{suffix}")
        if child is not None:
            lines.extend(render(child, prefix + (SPACE if last else PIPE)))
    return lines


def expected_tree_text() -> str:
    """Каноничный текст repository-tree.txt по фактическому составу."""
    tree = build_tree(tracked_files())
    lines = ["."] + render(tree)
    return "\n".join(lines) + "\n"


def check_tree(update: bool) -> bool:
    """Сверить (или перегенерировать) repository-tree.txt. True = всё в порядке."""
    expected = expected_tree_text()
    if update:
        TREE_FILE.write_text(expected, encoding="utf-8")
        print(f"[tree] repository-tree.txt перегенерирован ({len(expected.splitlines())} строк).")
        return True

    actual = TREE_FILE.read_text(encoding="utf-8") if TREE_FILE.exists() else ""
    if actual == expected:
        print("[tree] repository-tree.txt соответствует составу репозитория.")
        return True

    print("[tree] ОШИБКА: repository-tree.txt расходится с фактическим составом репозитория.")
    _print_diff(actual, expected)
    print("       Обновите файл: python3 validate_repository.py --update")
    return False


def _print_diff(actual: str, expected: str) -> None:
    import difflib

    diff = difflib.unified_diff(
        actual.splitlines(),
        expected.splitlines(),
        fromfile="repository-tree.txt (сейчас)",
        tofile="repository-tree.txt (ожидается)",
        lineterm="",
    )
    for line in diff:
        print("       " + line)


# Список проверок: (имя, функция(update) -> bool). Расширяется по мере надобности.
CHECKS = [
    ("repository-tree", check_tree),
]


def main(argv: list[str]) -> int:
    update = "--update" in argv[1:]
    ok = True
    for name, check in CHECKS:
        try:
            ok = check(update) and ok
        except Exception as exc:  # noqa: BLE001 — сообщаем и продолжаем
            print(f"[{name}] проверка упала с ошибкой: {exc}")
            ok = False
    if not ok and not update:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
