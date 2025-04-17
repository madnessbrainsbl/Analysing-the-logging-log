# Django Log Analyzer

CLI-приложение для анализа логов Django-приложения и формирования отчетов.

## Описание

Приложение анализирует журналы логов Django и формирует отчеты о состоянии API-ручек по каждому уровню логирования. Отчеты выводятся в консоль.

## Основные возможности

- Обработка нескольких файлов логов одновременно
- Параллельная обработка файлов для увеличения производительности
- Формирование отчетов о состоянии API-ручек
- Расширяемая архитектура для добавления новых типов отчетов


## Использование

```bash
python main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```

### Параметры

- `logs`: пути к файлам логов (один или несколько)
- `--report`: тип отчета (сейчас доступен только `handlers`)
- `--verbose`: включение режима отладки

### Пример вывода

```
Total requests: 1000

HANDLER              DEBUG  INFO  WARNING  ERROR  CRITICAL
/admin/dashboard/     20     72     19      14      18     
/api/v1/auth/login/   23     78     14      15      18     
/api/v1/orders/       26     77     12      19      22     
/api/v1/payments/     26     69     14      18      15     
/api/v1/products/     23     70     11      18      18     
/api/v1/shipping/     60     128    26      32      25     
TOTAL                 178    494    96      116     116    
```

## Архитектура

Проект имеет модульную структуру, что позволяет легко добавлять новые типы отчетов:

- `main.py`: основной скрипт, обрабатывает аргументы командной строки
- `analyzer.py`: содержит логику анализа файлов логов
- `reports/`: пакет с модулями для генерации отчетов
  - `base.py`: абстрактный базовый класс для всех отчетов
  - `handlers.py`: реализация отчета о состоянии API-ручек

## Добавление нового отчета

Для добавления нового типа отчета:

1. Создайте новый файл в директории `reports/`
2. Создайте класс, наследующийся от `Report` из `reports.base`
3. Реализуйте метод `generate()` для вашего отчета
4. Добавьте ваш отчет в словарь `REPORTS` в `reports/__init__.py`

Пример:

```python
# reports/my_report.py
from .base import Report

class MyReport(Report):
    name = "my_report"
    
    def generate(self, data, total):
        # Логика формирования отчета
        return "My report output"

# reports/__init__.py
from .handlers import HandlersReport
from .my_report import MyReport

REPORTS = {
    HandlersReport.name: HandlersReport(),
    MyReport.name: MyReport(),
}
```

## Тестирование

Запуск тестов:

```bash
pytest
```

Запуск тестов с отчетом о покрытии:

```bash
pytest --cov=.
```

## Требования

- Python 3.8+
- Стандартная библиотека Python
