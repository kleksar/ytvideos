import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('word_timings', HERE / 'word_timings.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def alignment(text):
    chars = list(text)
    return {'alignment': {'characters': chars,
                          'character_start_times_seconds': [i / 10 for i in range(len(chars))],
                          'character_end_times_seconds': [(i + 1) / 10 for i in range(len(chars))]}}


class WordTimingTests(unittest.TestCase):
    def test_russian_and_english_samples_are_self_contained(self):
        samples = {
            'ru': ('Это короткая тестовая строка для проверки тайминга.', 'Это', 7),
            'en': ('This is a short sample line for testing word timings.', 'This', 10),
        }
        for language, (source, first_word, expected_count) in samples.items():
            with self.subTest(language=language):
                result = module.convert(source, alignment(source), language)
                self.assertEqual(result['words'][0]['text'], first_word)
                self.assertTrue(all(w['start_seconds'] <= w['end_seconds'] for w in result['words']))
                self.assertEqual(len(result['words']), expected_count)

    def test_punctuation_hyphens_and_apostrophes(self):
        text = "«Всё-таки, кем-то — нет!» “Didn't ex-girlfriend’s.”"
        words = module.convert(text, alignment(text), 'ru')['words']
        self.assertEqual([w['display'] for w in words],
                         ['ВСЁ-ТАКИ', 'КЕМ-ТО', 'НЕТ', "DIDN'T", 'EX-GIRLFRIEND’S'])
        self.assertEqual(words[0]['start_seconds'], .1)
        self.assertEqual(words[0]['end_seconds'], 0.9)

    def test_unicode_composition_across_alignment_entries(self):
        source = 'Ёлка'
        data = alignment('Е\u0308лка')
        word = module.convert(source, data, 'ru')['words'][0]
        self.assertEqual(word['display'], 'ЁЛКА')
        self.assertEqual(word['end_seconds'], .5)

    def test_mismatch_does_not_use_normalized_as_a_silent_fallback(self):
        data = alignment('двадцать')
        data['normalized_alignment'] = alignment('20')['alignment']
        with self.assertRaisesRegex(module.AlignmentError, 'не совпадает'):
            module.convert('20', data, 'ru')
        self.assertEqual(module.convert('20', data, 'ru', 'normalized_alignment')['words'][0]['text'], '20')

    def test_bad_alignment_is_rejected(self):
        for mutate in (
            lambda d: d['alignment']['characters'].pop(),
            lambda d: d['alignment']['character_start_times_seconds'].__setitem__(1, float('nan')),
            lambda d: d['alignment']['character_end_times_seconds'].__setitem__(1, -1),
            lambda d: d.update(alignment=None),
        ):
            with self.subTest(mutate=mutate):
                data = alignment('abc')
                mutate(data)
                with self.assertRaises(module.AlignmentError):
                    module.convert('abc', data, 'en')

    def test_cli_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'text.txt').write_text('Hello', encoding='utf-8')
            (tmp / 'alignment.json').write_text(json.dumps(alignment('Hello')), encoding='utf-8')
            out = tmp / 'words.json'
            out.write_text('existing', encoding='utf-8')
            result = module.main(['--text', str(tmp / 'text.txt'), '--alignment', str(tmp / 'alignment.json'),
                                  '--language', 'en', '--output', str(out)])
            self.assertEqual(result, 1)
            self.assertEqual(out.read_text(), 'existing')


if __name__ == '__main__':
    unittest.main()
