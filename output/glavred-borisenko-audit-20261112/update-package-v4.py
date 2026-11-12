from pathlib import Path
import re

root = Path(__file__).parent
text = (root / 'metadata-package-v3-first-person.md').read_text(encoding='utf-8')
text = text.replace('Для всех семи роликов рекламная ссылка на свободный доступ к интернету размещена в начале по поручению пользователя. В двух выпусках, где ранее этой ссылки не было, она добавлена в предлагаемый текст; прежние ссылки этих выпусков сохранены. Далее — описание от лица Дмитрия, главы и хэштеги; Tags указаны отдельно. На YouTube изменения не внесены.', 'Все семь описаний начинаются с указанного пользователем блока из трёх ссылок. Ссылка на резервный канал удалена по поручению пользователя; сайт Московского экономического форума сохранён в соответствующем выпуске. Далее идут текст от первого лица, главы и хэштеги; Tags указаны отдельно. На YouTube изменения не внесены.')
ad = '🌐 Свободный доступ к интернету: https://telegram.me/maksconektbot?start=1D4CF2B7'
locked = '🔒 Расследования, инсайды, общение: https://t.me/lavka_glavreda_bot?start=1'
news = '💬 Следить за новостями: https://t.me/borisenkoD'
text = text.replace('\n' + locked + '\n' + news + '\n🎬 Резервный канал на YouTube: https://www.youtube.com/channel/UCbyLx6Rf3iWww4bPZJ2oo2A', '')
text = text.replace(ad, ad + '\n' + locked + '\n' + news)
text = text.replace('\n\nДрузья, ', '\n\n')
for old, new in {'разбираю слова':'Разбираю слова', 'не могу пройти':'Не могу пройти', 'хочу показать':'Хочу показать', 'каким может быть':'Каким может быть', 'в этом разговоре':'В этом разговоре', 'предлагаю вам':'Предлагаю вам', 'почему в России':'Почему в России'}.items():
    text = text.replace('\n\n' + old, '\n\n' + new)

blocks = re.split(r'(?=^## \d+\. )', text, flags=re.M)[1:]
assert len(blocks) == 7
expected = '\n'.join((ad, locked, news))
for n, block in enumerate(blocks, 1):
    desc = block.split('\n', 2)[2].lstrip().split('\n\n**Отдельное поле Tags:**')[0].strip()
    assert desc.startswith(expected), n
    assert 'Резервный канал' not in desc and '@nuviko_history' not in desc and 'Друзья,' not in desc, n
    assert len(desc.encode('utf-8')) < 5000, n
    print(n, 'OK', len(desc.encode('utf-8')), 'bytes')
(root / 'metadata-package-v4-first-person.md').write_text(text, encoding='utf-8')
