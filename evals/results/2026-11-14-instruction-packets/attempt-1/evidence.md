# Evidence (отдельные вызовы инструментов вне shell)

Этот файл перечисляет обнаруженные здесь вызовы вне shell и доступные результаты. Это не автоматическая полная трасса всех действий.

## Web search

- Tool: `mcp__codex_apps__search_service_web_run`
- Запрос: `petrichor smell after rain geosmin actinobacteria plant oils first drops study`
- Режим: `system2_search_query`; `response_length: medium`.
- Доступные ID/результаты (выдержки из текста результата):
  - `turn19search1` — American Society for Microbiology, “The Ubiquitous Soil Terpene Geosmin Acts as a Warning Chemical”, DOI `10.1128/aem.00093-22`: geosmin описан как запах земли после дождя; его производство встречается у нескольких групп микроорганизмов. Аннотация говорит, что биологическая функция изучена недостаточно.
  - `turn19search3` — “Dryland Soil Rewetting Induces Strong Volatile Organic Compound Emissions With Potential to Form Ozone and Aerosols”, PMC, опубликовано недавно по результату поиска: выделение петрикора после повторного увлажнения сухой почвы; смеси связываются с геосмином и другими летучими соединениями. Не использовалось как основание для универсальных утверждений.
  - `turn19search7` — European Geosciences Union Soil System Sciences blog, “Sure can smell the rain”: описывает накопленные в почве соединения и геосмин, а также высокоскоростное наблюдение за аэрозольным переносом при ударе капель. Это блог-обзор, не первичная статья.
  - `turn19search14` — American Chemical Society infographic, “What’s in the Smell of First Rain?”: говорит о петрикоре, геосмине и растительных маслах.
  - `turn19search4` — Texas A&M Stories, “Why You Can Smell Rain”: популярное объяснение роли геосмина и почвенных микроорганизмов; вторичный источник.

Результат поиска доступен в истории tool call с указанным query и IDs. Выдержки — не полный текст статей; источники не предъявлялись независимому рецензенту.

## Оговорка по trace.jsonl

`trace.jsonl` хранит stdout/stderr, exit code и argv команд, которые были исполнены через `record.py`. Первичные команды чтения AGENTS.md и команды записи самого отчёта выполнялись напрямую до/вне wrapper и не представлены в JSONL как полные shell-вызовы; их факт виден в истории этого выполнения. Один широкий `rg` по каталогу вернул избыточно большой stdout, он целиком сохранён в trace. Поэтому `trace.jsonl` — не полная автоматическая трасса, а именно журнал обёрнутых shell-команд с указанным пропуском.
