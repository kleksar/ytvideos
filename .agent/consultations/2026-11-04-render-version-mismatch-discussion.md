# Renderer version mismatch — discussion evidence

Scope: read-only investigation requested by user; no production procedure, code, publication or other episode changed.
Consultation: coordinator personally used visible Google Chrome, project chat https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aeb95ec-ced0-83eb-854b-4a324650b38c . Exact mode immediately before submission: «Очень высокий». Completed answer read.

## Verified local evidence

- Actual saved full-render commands: episode 038 Work/production-20261104-v01/full_render_v03/render_command.json and Work/production-20261104-v02/full_render_v01/render_command.json.
- filter_complex strings are identical, including explicit sRGB-to-Rec.709 conversion. Prior statement that v02 introduced this conversion was incorrect: it compared the working tree with Git HEAD rather than v01's actual command.
- Apart from run-specific input/output paths, the saved final commands differ at AAC target: 192k versus 256k.
- ffprobe: both AAC, 44100 Hz, 2 channels; measured mean bit rates v01 193564 bit/s, v02 253894 bit/s.
- EXPORT_CONTRACT_v01.json already required target 256000 bit/s. Current audio owner also requires stereo target >=256k. v01 actual command disagreed with its contract.
- delivery.py validate_release compares engine file records to the currently mutable files; any engine SHA mismatch triggers Stale delivery input. This does not itself prove a defect in a historical MP4.
- Working-tree montage.py change introduces channel-dependent AAC targets; Git diff also includes color changes, but those were already active in the saved v01 command. The author and precise origin of the uncommitted changes were not established.
- Other episodes were not audited; affected count is unknown. Shared renderer creates potential cross-channel scope.

## Consultation task

Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора уже выполнено этим обращением; дай ответ здесь, не открывай рекурсивно другой ChatGPT. Режим перед отправкой виден: «Очень высокий». Одна узкая задача: оценить причину и предложить принцип исправления контроля версий рендера, без исполнения работ. Факты локального разбора: пользователь принял MP4 v01, затем upload validator отклонил его, потому что сравнивает SHA текущего montage.py с SHA, записанным при рендере. В коде после рендера изменился AAC target для стерео: 192k -> 256k. Паспорт v01 уже требовал 256k, но сохранённая фактическая FFmpeg-команда была 192k. Перерендерили v02 с 256k. Координатор сначала ошибочно сообщил ещё изменение цвета, сравнив текущий код с Git HEAD; однако сохранённые фактические filter_complex v01/v02 полностью совпадают, sRGB->Rec709 уже был в обоих. Общий renderer используется двумя каналами. Другие выпуски не проверяли, масштаб неизвестен. Нужен короткий ответ: какие разные проблемы тут установлены, почему изменение исходного кода не доказывает дефект готового MP4, как связать паспорт/фактическую команду/версии движка, и как определить затронутые выпуски без массовых перерендеров. Не обсуждай исторический контент, публикацию или креатив.

## Completed response

Причина — смешение версионирования исходного кода, фактических параметров рендера и требований к готовому MP4. Это три разных объекта контроля.

1. Установленные проблемы
- Ложная инвалидация: upload validator сравнивает SHA текущего montage.py с SHA при рендере. Любое изменение файла блокирует MP4, даже если не влияет на результат.
- Реальное расхождение с паспортом: v01 требовал AAC 256k, но FFmpeg запускался с 192k. Это подтверждённый дефект соответствия требованиям, а не обязательно дефект воспроизведения.
- Ошибочная диагностика: изменение цвета было ошибочно выведено из сравнения с Git HEAD. Фактические filter_complex v01 и v02 совпадают, поэтому оснований утверждать изменение цветовой обработки нет.

2. Принцип исправления
Паспорт задаёт требования, команда фиксирует исполнение, артефакт подтверждает результат.
Для каждого рендера сохранять неизменяемый manifest:
- artifact_sha256, render_id, engine_commit, engine_version;
- spec_version и нормализованные требования паспорта;
- фактические FFmpeg argv, filter_complex, параметры кодеков;
- версии FFmpeg и существенных зависимостей;
- результаты ffprobe и проверок соответствия паспорту.
При изменении движка не инвалидировать старые файлы автоматически. Валидировать конкретный MP4 относительно закреплённой спецификации, а происхождение проверять по manifest и хешу артефакта.
SHA исходного кода сохранять для воспроизводимости, но не использовать как универсальный критерий пригодности MP4.

3. Как определить затронутые выпуски
1. Составить реестр существующих MP4 обоих каналов с версиями движка, фактическими командами и паспортами.
2. Проверить AAC через ffprobe; сопоставить результаты с требованиями каждого выпуска. Одного bitrate недостаточно для доказательства точного FFmpeg target — использовать сохранённую команду, если она доступна.
3. Отдельно сравнить фактические графы фильтров, не выводя изменения картинки из Git diff.
4. Классифицировать выпуски: compliant, mismatch, unknown.
5. Перерендеривать только подтверждённые несоответствия, требующие изменения медиа. Для unknown сначала проводить адресную проверку.
Итог: v01 подтверждённо не соответствовал паспорту по AAC target; v02 исправил этот параметр. Изменение цвета не подтверждено. Масштаб проблемы среди остальных выпусков неизвестен. Массовый перерендер не обоснован.

## Coordinator interpretation and limits

The consultation is advice, not primary evidence or user approval. Local command and contract inspection independently establish the mismatch. Proposed fixes remain discussion only. Preserve checks on changed accepted edit/source content; renderer version pinning must not become a blanket stale-input bypass. No perceptual A/B listening or full visual comparison was performed. No claim of a widespread perceptual defect is supported.
