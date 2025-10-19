import argparse
import os
import sys
from urllib.parse import urlparse


def validate_args(args):
    """Проверяем корректность введённых аргументов."""
    errors = []

    # Проверка имени пакета
    if not args.package_name:
        errors.append("Ошибка: имя анализируемого пакета не указано.")

    # Проверка URL или пути
    if args.repo_path:
        # Проверяем, является ли это URL или локальным путём
        parsed = urlparse(args.repo_path)
        if parsed.scheme in ("http", "https"):
            # Примитивная проверка корректности URL
            if not parsed.netloc:
                errors.append("Ошибка: некорректный URL-адрес репозитория.")
        else:
            # Проверяем, существует ли файл/папка
            if not os.path.exists(args.repo_path):
                errors.append(f"Ошибка: путь '{args.repo_path}' не существует.")

    # Проверка режима работы
    if args.mode not in ("local", "remote", "mock"):
        errors.append(
            "Ошибка: режим работы должен быть 'local', 'remote' или 'mock'."
        )

    # Проверка глубины анализа
    if args.max_depth is not None and args.max_depth < 0:
        errors.append("Ошибка: максимальная глубина анализа не может быть отрицательной.")

    # Проверка имени выходного файла
    if not args.output_file.endswith((".png", ".svg", ".jpg")):
        errors.append(
            "Ошибка: имя выходного файла должно оканчиваться на .png, .svg или .jpg."
        )

    if errors:
        print("\n".join(errors))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (этап 1)"
    )

    parser.add_argument(
        "--package-name",
        required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="URL-адрес репозитория или путь к тестовому репозиторию"
    )
    parser.add_argument(
        "--mode",
        default="local",
        help="Режим работы: local | remote | mock"
    )
    parser.add_argument(
        "--output-file",
        default="graph.png",
        help="Имя генерируемого файла с изображением графа"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Максимальная глубина анализа зависимостей"
    )

    args = parser.parse_args()

    # Проверка корректности аргументов
    validate_args(args)

    # Вывод всех параметров в формате ключ-значение
    print("Параметры конфигурации:")
    print(f"Имя пакета: {args.package_name}")
    print(f"Репозиторий: {args.repo_path}")
    print(f"Режим: {args.mode}")
    print(f"Файл вывода: {args.output_file}")
    print(f"Максимальная глубина: {args.max_depth}")


if __name__ == "__main__":
    main()