from .handlers import HandlersReport

REPORTS = {
    HandlersReport.name: HandlersReport()
}

def generate_handlers_report(data, total):
    """
    Функция для генерации отчета о состоянии ручек API по каждому уровню логирования.
    """
    return HandlersReport().generate(data, total)
