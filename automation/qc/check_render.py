#!/usr/bin/env python3
"""Check basic exported Shorts properties and decode; no subjective QA claims."""
import argparse
from fractions import Fraction
import json
import subprocess
import sys
from pathlib import Path


def inspect(path, decode=True):
    path = Path(path).expanduser().resolve(strict=True)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError('Файл пустой или не является обычным файлом')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                            '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    data = json.loads(probe.stdout)
    video = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
    audio = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
    errors = []
    if len(video) != 1:
        errors.append('Ожидалась одна видеодорожка')
    if len(audio) != 1:
        errors.append('Ожидалась одна аудиодорожка')
    if video:
        v = video[0]
        if (v.get('width'), v.get('height')) != (1080, 1920):
            errors.append('Размер должен быть 1080×1920')
        try:
            if Fraction(v.get('avg_frame_rate', '0/1')) != 30:
                errors.append('Средняя частота кадров должна быть 30 fps')
        except (ValueError, ZeroDivisionError):
            errors.append('Не удалось определить частоту кадров')
    decode_ok = None
    if decode:
        result = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
                                 '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        decode_ok = result.returncode == 0
        if not decode_ok:
            errors.append('Полное декодирование видео и аудио завершилось ошибкой')
    return {'path': str(path), 'duration_seconds': data.get('format', {}).get('duration'),
            'technical_status': 'failed' if errors else 'passed', 'errors': errors,
            'decoded': decode_ok,
            'not_checked': ['воспроизведение со звуком', 'произношение и синхронизация титров',
                            'визуальная композиция и интерфейс Shorts', 'чёрные кадры']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video')
    args = parser.parse_args()
    try:
        result = inspect(args.video)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['technical_status'] == 'passed' else 1
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f'Ошибка проверки: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
