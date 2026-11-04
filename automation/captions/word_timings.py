#!/usr/bin/env python3
"""Convert matching ElevenLabs character alignment into reviewable word timings."""
import argparse
import hashlib
import json
import math
import sys
import unicodedata
from pathlib import Path


class AlignmentError(ValueError):
    pass


def _word_char(char):
    return unicodedata.category(char)[0] in ('L', 'N', 'M')


def _normalised_chars(entries, starts, ends):
    # Normalize base + combining marks together, including across API entries.
    clusters = []
    for entry, start, end in zip(entries, starts, ends):
        for char in entry:
            if unicodedata.combining(char) and clusters:
                clusters[-1][0] += char
                clusters[-1][2] = max(clusters[-1][2], end)
            else:
                clusters.append([char, start, end])
    result = []
    for chars, start, end in clusters:
        result.extend((char, start, end) for char in unicodedata.normalize('NFC', chars))
    # tts.py strips the approved text before submitting it.
    while result and result[0][0].isspace():
        result.pop(0)
    while result and result[-1][0].isspace():
        result.pop()
    return result


def convert(source, data, language, field='alignment'):
    if language not in ('ru', 'en'):
        raise AlignmentError('язык должен быть ru или en')
    if not isinstance(data, dict) or not isinstance(data.get(field), dict):
        raise AlignmentError(f'{field} отсутствует или равен null; требуется отдельное выравнивание')
    alignment = data[field]
    chars = alignment.get('characters')
    starts = alignment.get('character_start_times_seconds')
    ends = alignment.get('character_end_times_seconds')
    if not all(isinstance(v, list) for v in (chars, starts, ends)):
        raise AlignmentError('в alignment отсутствуют массивы символов или времени')
    if not chars or len(chars) != len(starts) or len(chars) != len(ends):
        raise AlignmentError('массивы alignment пусты или имеют разную длину')
    previous_start = previous_end = -1.0
    for i, (char, start, end) in enumerate(zip(chars, starts, ends)):
        if not isinstance(char, str) or not char:
            raise AlignmentError(f'пустой или неверный символ alignment на позиции {i}')
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (start, end)):
            raise AlignmentError(f'нечисловое время alignment на позиции {i}')
        if start < 0 or end < start or start < previous_start or end < previous_end:
            raise AlignmentError(f'нарушен порядок времени alignment на позиции {i}')
        previous_start, previous_end = start, end
    aligned = _normalised_chars(chars, starts, ends)
    actual = ''.join(c for c, _, _ in aligned)
    approved = unicodedata.normalize('NFC', source.strip())
    if actual != approved:
        pos = next((i for i, (a, b) in enumerate(zip(approved, actual)) if a != b), min(len(approved), len(actual)))
        lo, hi = max(0, pos - 20), pos + 20
        raise AlignmentError(f'{field} не совпадает с утверждённым текстом на позиции {pos}: '
                             f'текст={approved[lo:hi]!r}; alignment={actual[lo:hi]!r}. '
                             'Нужна ручная проверка, автоматическая подмена текста запрещена')
    words = []
    i = 0
    while i < len(approved):
        if not _word_char(approved[i]):
            i += 1
            continue
        start = i
        i += 1
        while i < len(approved):
            c = approved[i]
            if _word_char(c):
                i += 1
            elif c in "-'’‐‑" and i + 1 < len(approved) and _word_char(approved[i - 1]) and _word_char(approved[i + 1]):
                i += 1
            else:
                break
        token = approved[start:i]
        words.append({'text': token, 'display': token.upper(),
                      'start_seconds': aligned[start][1], 'end_seconds': aligned[i - 1][2]})
    if not words:
        raise AlignmentError('в утверждённом тексте нет слов')
    return {'version': 1, 'language': language, 'alignment_field': field,
            'source_sha256': hashlib.sha256(source.encode('utf-8')).hexdigest(),
            'words': words,
            'review_required': 'Тайминги не являются готовой смысловой картой титров; проверьте звук и разбейте текст вручную.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Подготовить пословные тайминги из ElevenLabs alignment')
    parser.add_argument('--text', type=Path, required=True, help='утверждённый текст озвучки UTF-8')
    parser.add_argument('--alignment', type=Path, required=True, help='JSON с alignment и normalized_alignment')
    parser.add_argument('--language', choices=('ru', 'en'), required=True)
    parser.add_argument('--field', choices=('alignment', 'normalized_alignment'), default='alignment')
    parser.add_argument('--output', type=Path, required=True, help='новый JSON; существующий файл не перезаписывается')
    args = parser.parse_args(argv)
    try:
        source = args.text.read_text(encoding='utf-8')
        data = json.loads(args.alignment.read_text(encoding='utf-8'))
        result = convert(source, data, args.language, args.field)
        with args.output.open('x', encoding='utf-8') as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
        print(f"Сохранено {len(result['words'])} слов: {args.output}. Проверьте тайминг на слух и смысловую карту вручную.")
        return 0
    except (AlignmentError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'Ошибка: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
