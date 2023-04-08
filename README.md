# Проект по определению авторства текста на основе его стиля

## участники:
- [Владимир Голод](https://github.com/Vigolod)
- [Максим Демидов](https://github.com/Dm12H)
- [Никита Праздников](https://github.com/kuchen1911)

## Данные 
Вручную собранный датасет текстов русскоязычных писателей,
находящихся в открытом доступе. Начальный размер выборки - собрание сочинений 15 авторов XVIII-XX века.

## [План работ](checkpoint_1/README.md)
## [Описание данных](checkpoint_2/README.md)
## [Разведочный анализ](checkpoint_3/README.md)

## Структура проекта

- В папке `experiments` находятся ноутбуки с актуальными ноутбуками
- папка `text_authorship/ta_model` содержит основную структуру проекта:
    * `base_models` содержит функции для обучения актуальных моделей
    * `data_extraction` подготавливает датасет из сырых документов и обрабатывает загрузку-выгрузку
    * `data_preparation` собирает все признаки, использующиеся в моделях
    * `model_selection` содержит функции для кроссвалидации и анализа результатов
    * `stacking` содержит инструменты для энсэмблинга
    * `logreg` содержит инструменты для логистической регрессии

## Запуск проекта
Для запуска неободимо скачать подготовленный [датасет](https://drive.google.com/drive/folders/1S7ZPEsi2yiW5C7TP-1ICO1pZJp0YUXQ9?usp=share_link)\
установка зависимостей:\
`pip install -r requirements.txt`
скрипт для подготовки датасета и сериализации трансформера:\
`./prepare_dataset.py --data_dir=<path-to-raw-data-folder> --output_dir=<path-to-output-folder> --pickle=<file-to-serialize-transformer>`\
скрипт для получения скора модели на тестовой выборке:\
`./train_test_model.py --prepared_data=<path-to-transformed-dataset> --model=<logreg|stacking>`\
скрипт для обучения и сериализации модели:\
`./train_model.py --prepared_data=<path-to-transformed-dataset> --model=<logreg|stacking> --pickle=<file-to-serialize-model>`

## Структура сервиса

- Файл `main.py` содержит основной файл для запуска сервиса на `fastapi`
- папка `app` содержит реализации основных функций сервиса, а также логирование:
    * папка `app_models` содержит в себе модули `inference` и `model_manager`, отвечающие за выгрузку и применение моделей
    * папка `forms` содержит необходимые HTML-шаблоны и CSS файлы
    * папка `utils` содержит визуализацию и другие мелкие инструменты
    * модуль `config` отвечает за выгрузку конфигураций в настройки сервера
    * модуль `logs` отвечает за логирование
    * модуль `session_id` содержит потоко-безопасный генератор уникальных id (в данный момент не используется сервисом)
- конфигурационный файл `settings.yml` содержит конфигурацию сервиса:
    * параметры `transformer_path` и `model_paths` содержат пути к сериализованным трансформеру и моделям, соответственно
    * `log_config` содержит настройки для логирования

## Запуск сервиса

При запуске сервиса на локальной машине (не из docker образа) нужно загрузить [архив](https://drive.google.com/drive/folders/1w05x8hz_RO8Pn_oDCySCi0soXTbj9nm2?usp=sharing) и распаковать лежащие внутри `.pkl` файлы в корневую директорию проекта\
установка зависимостей:\
`pip install -r requirements.txt`\
запуск сервиса:\
`uvicorn main:app` (при желании можно указать конкретный порт)\
после появления в консоли лога вида `server started after <time-spent>` можно открыть сервис в браузере (по умолчанию `localhost:8000`)

### Функционал

Сервис по введенному тексту определеят автора (на выбор предлагаются две модели), а также выводит barplot, показывающий, на стиль каких авторов по мнению модели больше всего похож введенный текст (список поддерживаемых авторов можно найти в папке `checkpoint_2`).

### Примечание

Чтобы посмотреть на то, как логи выводят ошибки, можно попробовать испортить файл `settings.yml` (например, добавить в списке моделей еще одну с несуществующим файлом `nothing_here.pkl`). Логи ошибок появятся в файле `logerrors.log`. Конфигурацию логирования при этом лучше не менять. 