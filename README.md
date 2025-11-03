# Этап 1

## Функция validate_args для валидации аргументов

Настраивает имя анализируемого пакета, URL-адрес репозитория или путь к файлу тестового репозитория, режим работы с тестовым репозиторием, имя сгенерированного файла с изображением графа, максимальную глубину анализа зависимостей

Реализована обработка ошибок

При запуске приложения выводятся все параметры, настраиваемые пользователем, в формате ключ-значение

Для ввода использовать

python main.py --package-name "Some package" --repo-path "path"

<img width="747" height="272" alt="image" src="https://github.com/user-attachments/assets/fc0bd821-569f-4442-8b20-b2bb6f67ee8f" />


# Этап 2

## Функция validate_args для валидации аргументов

## Функция download_nupkg для загрузки пакета

## Функция extract_nuspec для извлечения метаданных

## Функция extract_nuspec parse_dependencies для парсинга зависимостей

Испольует формат пакетов .NET (NuGet), извлекает информацию о прямых зависимостях заданного пользователем пакета, используя URL-адрес репозитория, выводит на экран все прямые зависимости заданного пользователем пакета

Для ввода использовать

python main.py --package-name Newtonsoft.Json --repo-path https://www.nuget.org/api/v2/package

python main.py --package-name "Newtonsoft.Json" --repo-path "https://www.nuget.org" --mode remote --output-file "dependencies.png" --max-depth 2


<img width="765" height="301" alt="image" src="https://github.com/user-attachments/assets/98415262-9d0a-4fab-a1ae-49a82e17bb17" />


<img width="1412" height="257" alt="image" src="https://github.com/user-attachments/assets/0f0794f5-2004-4f1a-aa54-84c720b07c68" />


<img width="1368" height="87" alt="image" src="https://github.com/user-attachments/assets/95cdd52f-841c-4ae6-b0ec-7a3f14a83885" />

