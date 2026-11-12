# English translation consultation — 031 Jascon-4 / Harrison Okene

- Дата, задача и стадия: 2026-11-01; перевод принятой русской озвучки в английский для Paper Detour; подготовка TTS.
- Координатор / Google Chrome / URL чата: координатор лично; проект YT Видео; [Translate Russian Voiceover](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae79f8e-5e2c-83eb-82f3-6b8d49f965eb).
- Точная видимая маркировка непосредственно перед отправкой: `Extra High` (проверена перед обоими запросами).
- Принятые входы и их версии: `Source/Script/narration_ru_v01.md`, раздел «Рабочая редакция сценария»; `Source/Research/fact_check_v01.md`; принятый storyboard с 16 изображениями.

## Запрос 1

> You are the consultant in the already-open ChatGPT Extra High session; the external coordinator requirement is satisfied by this request. Handle one narrow task: translate the accepted Russian voiceover below into natural spoken English for the English-language Paper Detour channel. Preserve every factual claim, attribution, hook, reveal, and ending. Do not add facts, invented sensory details, or explanatory asides. Keep the same 15 paragraph/cue breaks and approximate narration length. Use clear internationally understandable English; keep the metric depth as ‘about 30 metres’ (or ‘about 30 meters’ consistently). Write Jascon-4 naturally for an English narrator, but do not alter the public spelling. Output only the final English spoken narration, one paragraph per cue, no headings or visual directions.

Текст источника: пятнадцать пронумерованных абзацев из рабочей русской редакции сценария; полный оригинал хранится в `Source/Script/narration_ru_v01.md`.

## Ответ 1

At a depth of about 30 metres, a diver was searching for bodies inside a sunken tugboat.
He reached for a hand—and felt it grab him.
Someone was still alive in there. Could they bring him up?
To understand how he ended up inside, let's go back to the Jascon-4 disaster.
On May 26, 2013, the tugboat sank off the coast of Nigeria. There were twelve people on board.
The divers had come to recover the bodies. By then, they had already brought up four.
Harrison Okene, the ship's cook, was still inside the hull. The diver had not seen him on his first pass.
According to Okene, he tried to find the diver in the darkness, but returned to the air pocket.
There was still an air pocket inside the hull.
Okene spent more than sixty hours in it, at a depth of about 30 metres.
Now they had to get him out of the hull.
Using a backup diver line, they guided him to the diving bell.
After he was brought up, Okene was placed in a decompression chamber.
Okene was the only survivor. The other eleven crew members died.
The divers went down to search for bodies—and saved a man they never expected to find alive.

## Запрос 2 — уточнение терминологии

> One narrow translation correction. The line ‘Using a backup diver line, they guided him to the diving bell’ sounds awkward. Translate only this accepted Russian clause into concise, natural spoken English: ‘С помощью резервной водолазной линии его сопроводили к колоколу.’ The fact check supports a backup umbilical line/cable to the diving bell; do not imply a separate backup air supply. Output one replacement sentence only.

## Ответ 2

They guided him to the diving bell along a backup umbilical line.

## Что проверено / рабочая версия

- Перевод сохраняет пятнадцать исходных cue, включая хук, атрибуцию «According to Okene», формулировку «more than sixty hours» и гибель остальных членов экипажа.
- `Jascon-4` оставлен в исходном написании. Слова `air pocket` не расширены до неподтверждённого физиологического объяснения.
- Во второй точечной консультации исправлена неестественная формулировка `backup diver line`; выбран вариант `backup umbilical line`, согласующийся с фактической опорой и не утверждающий наличие отдельной резервной подачи воздуха.
- Файл фактического текста, переданного на TTS: `voice_en_tts_v01.txt`.

## Ограничения / следующий этап

Английский текст является рабочим переводом, созданным в соответствии с прямым поручением пользователя; отдельной пользовательской вычитки текста ещё не было. После TTS требуется проверить файл технически; естественность речи, ударения и произношение имени нельзя подтвердить одним текстовым alignment или ASR. В текущей версии 15 речевых блоков при 16 принятых кадрах — соответствие кадрам предстоит решить на этапе тайминга.
