import argparse
import os
import sys
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin


def validate_args(args):
    """Проверка корректности аргументов"""
    errors = []

    # Имя пакета
    if not args.package_name:
        errors.append("Ошибка: имя анализируемого пакета не указано")

    # Проверка URL или локального пути
    if args.repo_path:
        parsed = urlparse(args.repo_path)
        if parsed.scheme in ("http", "https"):
            if not parsed.netloc:
                errors.append("Ошибка: некорректный URL-адрес репозитория")
        else:
            if not os.path.exists(args.repo_path):
                errors.append(f"Ошибка: путь '{args.repo_path}' не существует")

    # Проверка режима
    if args.mode not in ("local", "remote", "mock"):
        errors.append("Ошибка: режим работы должен быть 'local', 'remote' или 'mock'")

    # Проверка глубины
    if args.max_depth is not None and args.max_depth < 0:
        errors.append("Ошибка: максимальная глубина анализа не может быть отрицательной")

    # Проверка имени файла
    if not args.output_file.endswith((".png", ".svg", ".jpg")):
        errors.append("Ошибка: имя выходного файла должно оканчиваться на .png, .svg или .jpg")

    if errors:
        print("\n".join(errors))
        sys.exit(1)


def download_nupkg(package_name, repo_url):
    """Скачивает .nupkg из NuGet-репозитория"""
    # Для NuGet v2 API правильный формат URL
    if "nuget.org" in repo_url:
        # Используем прямой URL для скачивания последней версии
        url = f"https://www.nuget.org/api/v2/package/{package_name.lower()}/"
    else:
        # Для других репозиториев оставляется старый формат
        if not repo_url.endswith("/"):
            repo_url += "/"
        url = urljoin(repo_url, f"{package_name.lower()}/latest/download")

    filename = f"{package_name}.nupkg"

    print(f"Загрузка пакета: {url}")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Пакет сохранён как: {filename}")
        return filename
    except Exception as e:
        print(f"Ошибка при загрузке пакета: {e}")
        sys.exit(1)


def extract_nuspec(nupkg_file):
    try:
        with zipfile.ZipFile(nupkg_file, "r") as z:
            for name in z.namelist():
                if name.endswith(".nuspec"):
                    z.extract(name)
                    return name
        print("Ошибка: файл .nuspec не найден в архиве")
        sys.exit(1)
    except zipfile.BadZipFile:
        print("Ошибка: повреждённый или некорректный .nupkg файл")
        sys.exit(1)


def parse_dependencies(nuspec_file):
    try:
        tree = ET.parse(nuspec_file)
        root = tree.getroot()

        deps = []
        for elem in root.iter():
            if elem.tag.endswith("dependency"):
                deps.append((elem.attrib.get("id"), elem.attrib.get("version", "")))

        return deps
    except ET.ParseError:
        print("Ошибка: неверный формат XML в .nuspec файле")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Этап 2: Сбор данных о зависимостях NuGet-пакета")
    parser.add_argument("--package-name", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo-path", required=True, help="URL репозитория или путь к нему")
    parser.add_argument("--mode", default="local", help="Режим работы: local | remote | mock")
    parser.add_argument("--output-file", default="graph.png", help="Имя выходного файла")
    parser.add_argument("--max-depth", type=int, default=3, help="Максимальная глубина анализа")
    args = parser.parse_args()

    # Проверка аргументов
    validate_args(args)

    # Сбор данных
    nupkg = download_nupkg(args.package_name, args.repo_path)
    nuspec = extract_nuspec(nupkg)
    deps = parse_dependencies(nuspec)

    print("\nПрямые зависимости:")
    if deps:
        for name, version in deps:
            print(f"- {name} ({version})")
    else:
        print("Зависимостей не найдено")


if __name__ == "__main__":
    main()