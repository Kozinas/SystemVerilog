"""Rebuild the traceability appendix without modifying the user's PLAN.md."""
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book import ROOT, load_book

DEFAULTS = {1: "01", 2: "03", 3: "05", 4: "07", 5: "09", 6: "07",
            7: "08", 8: "13", 9: "06", 10: "10", 11: "24", 12: "11",
            13: "12", 14: "15", 15: "14", 16: "16", 17: "30", 18: "32"}
OVERRIDES = {
    "1.2": "33", "1.3": "33", "1.4": "02", "1.5": "02", "1.6": "02",
    "1.4.3": "06", "1.7": "02", "1.8": "04", "1.10.1": "03", "1.10.2": "13",
    "1.10.3": "15", "1.10.4": "30", "1.10.5": "23", "1.10.6": "27",
    "1.10.7": "32", "1.11": "16", "1.12": "33", "2.11": "14",
    "2.12": "32", "3.2.2": "31", "3.2.3": "30", "3.2.4": "30",
    "3.2.5": "30", "3.2.6": "A", "3.6": "05", "3.7": "05",
    "3.8.3": "31", "7.1.8": "19", "7.1.14": "22", "8.7": "13",
    "9.5.1": "10", "10.4": "10", "11.1": "04", "11.1.3": "24",
    "11.1.4": "10", "11.2.1": "11",
    "11.2.4": "11", "11.2.6": "11", "11.3": "10", "13.10": "B",
    "14.10": "23", "17.1": "33", "17.2.3": "31",
}


def render():
    _, chapters = load_book()
    lookup = {c.number: c for c in chapters}
    output = ROOT / "docs/appendices/d-plan-map.md"
    lines = ["# D. Соответствие исходному PLAN.md", "",
             "Исходный план сохранён без изменений. Ниже перечислен каждый его",
             "нумерованный пункт и ближайшая глава новой методички. Мелкие пункты",
             "объединены в связанные объяснения; ссылка означает место рассмотрения",
             "темы, а не дословное повторение структуры или текста книги.", "",
             "Сначала введены модули и симуляция, затем типы и выражения, после них",
             "процедуры и организация проекта. Практический RTL вынесен в отдельную",
             "часть, проверочные средства дополнены классами, randomization, SVA,",
             "coverage и DPI. Примитивы/конфигурации изучаются после рабочего RTL.", "",
             "Таблица воспроизводится командой `python tools/map_plan.py`."]
    count = 0
    for source_line in (ROOT / "PLAN.md").read_text(encoding="utf-8").splitlines():
        if source_line.startswith("Глава "):
            lines += ["", "## " + source_line, "", "| Пункт исходного плана | Новая глава |", "| --- | --- |"]
        match = re.match(r"^(\d+(?:\.\d+)+)\.\s+(.+)$", source_line)
        if not match:
            continue
        number, title = match.groups()
        destination = DEFAULTS[int(number.split(".")[0])]
        for prefix in sorted(OVERRIDES, key=len, reverse=True):
            if number == prefix or number.startswith(prefix + "."):
                destination = OVERRIDES[prefix]
                break
        chapter = lookup[destination]
        relative = os.path.relpath(chapter.path, output.parent).replace(os.sep, "/")
        title = title.replace("|", "\\|")
        lines.append(f"| {number}. {title} | [{destination}. {chapter.title}]({relative}) |")
        count += 1
    lines += ["", "## Дополнения и ненумерованные материалы", "",
              "Предисловие и маршрут чтения — глава 01. Практическое завершение курса —",
              "главы 22 и 33. Ключевые слова и системные средства — приложение B,",
              "ответы — C, литература — E, сокращения и предметный указатель — F.", "",
              "По сравнению с исходным планом добавлены самостоятельные главы о RAM/FIFO,",
              "автоматах, CDC/RDC, тестбенчах и clocking, классах, constrained random,",
              "assertions, coverage, DPI/VPI, specify/SDF и изменениях IEEE 1800-2023.", "",
              f"Всего сопоставлено нумерованных пунктов: **{count}**.", ""]
    output.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Mapped {count} PLAN.md topics")


if __name__ == "__main__":
    render()
