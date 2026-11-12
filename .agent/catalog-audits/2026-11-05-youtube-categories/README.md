# Аудит категорий YouTube, 5 ноября 2026

[Ведомость по всем 60 видео](categories.csv) · [Машиночитаемый результат](results.json) · [Правило выпуска](../../../.agents/skills/ytv-youtube-release/references/video-categories.md).

| Канал | Покрытие | Проверено | Изменено | Категории после проверки |
|---|---|---:|---:|---|
| Paper Detour | Все видео из авторизованного плейлиста загрузок | 34 | 7 | 30 Education, 3 Entertainment, 1 People & Blogs |
| Nuviko History | Все видео из авторизованного плейлиста загрузок | 9 | 0 | 9 Education |
| Нувико | Полный список в Studio и проверка публичных метаданных по API | 10 | 0 | 10 People & Blogs |
| Nuviko Videos | Публичный каталог архивного англоязычного канала | 7 | 0 | 7 People & Blogs |

Содержание каждого ролика оценено по названию и описанию. Для пограничных случаев дополнительно сверены доступные тексты озвучки, указанные в ведомости. Старый канал с ID `UCqct_dth0WSCwiDZx1WMfgg` API показывает как `Deleted`, с нулём публичных роликов и недоступным плейлистом загрузок.

## Сохранённые правки Paper Detour

| Видео | Было → стало |
|---|---|
| [How a Car Manual Publisher Ended Up Publishing Dune](https://www.youtube.com/watch?v=ba2GMSKTB5g) | Entertainment → Education |
| [Nine Months at Sea. Then Pattaya.](https://www.youtube.com/watch?v=vBJE5kdGE5o) | Entertainment → Education |
| [They Shared a Burrow for 250 Million Years](https://www.youtube.com/watch?v=UkwqGIqvink) | Entertainment → Education |
| [What If Time Stopped for 5 Seconds?](https://www.youtube.com/watch?v=YRnIpr9P3iE) | Entertainment → Education |
| [A Diver Reached for a Hand in a Sunken Tugboat. It Grabbed Back.](https://www.youtube.com/watch?v=zA0kogtqoUs) | Entertainment → Education |
| [A Third Wheel on Every Date](https://www.youtube.com/watch?v=Yz1Fn3GRsrw) | Education → People & Blogs |
| [They Opened Her Coffin. She Sat Up.](https://www.youtube.com/watch?v=pdSgHe6ScTI) | Education → Entertainment |

Каждая правка прошла свежую сверку владельца, `videos.update(part=snippet)` с сохранением остальных редактируемых полей и повторное чтение. Для всех семи роликов прочитанные `snippet`, `status`, `localizations` и `contentDetails` совпали до и после за исключением `categoryId`. В конце все 60 категорий перечитаны через API.

## Границы проверки

- В Studio под ролью менеджера «Нувико» по ID `UCY0Wa9sdQrvFgbv7B-AXCyg` показаны 10 Shorts, диапазон 1–10 из 10. Все ID совпали с API. Вкладки длинных видео и трансляций пусты. Старые OAuth-токены вернули `invalid_grant`.
- В Nuviko Videos по ID `UC4nNJWr_PDL3QCZ76KGHF1g` семь найденных публичных видео совпали со счётчиком канала. Проверка непубличного каталога недоступна. Studio отказала в доступе для текущего аккаунта, старые токены вернули `invalid_grant`.
- Между первоначальным и итоговым чтением ролики о бостонской патоке и Брестской крепости перешли из Private в Public. Их категория совпадала с планом уже на первом чтении. Запросы записи по этим ID в ходе аудита не отправлялись. Прочие наблюдавшиеся изменения перечислены в [журнале](concurrent_differences.json).
