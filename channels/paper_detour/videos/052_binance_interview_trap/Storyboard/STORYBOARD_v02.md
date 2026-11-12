# 052 — раскадровка v02

Полная длительность: 141.00 с (4230 кадров при 30 fps). Оригинальный storyboard-консультативный черновик давал 169.5 с и отклонён по длительности: фактическая голосовая дорожка — 130.96 с. История занимает кадры 0–3929 (131 с), последние две сцены — тихая end screen от 131 до 141 с. Озвучка не растягивается. Интервалы речи рассчитаны по сохранённому character alignment; это машинная разметка, не подтверждение услышанного синхрона.

Единый холст: 2560×1440, 30 fps, цельные статичные диорамы, прямые склейки; движение цельного изображения по согласованным endpoints. Paper Frame и субтитры остаются отдельными слоями. Субтитры прекращаются на кадре 3930 до начала финальной заставки. Финальные зоны YouTube оставлены свободными; элементы интерфейса не запекаются в MP4.

| ID | Frames | Seconds | Image | Coverage / purpose |
|---|---:|---:|---|---|
| S01 | [0,150) | 0.00–5.00 | S01_v01.png | Interview hook — A Binance engineer interviews for a job at another company. First, he speaks with a |
| S02 | [150,300) | 5.00–10.00 | S02_v01.png | Recruiter call — recruiter. Then he speaks with someone claiming to be the company's manager. He gets |
| S03 | [300,450) | 10.00–15.00 | 24_v01.png | Claimed manager — a test assignment and downloads it to his work computer. But the company doesn't exist. |
| S04 | [450,600) | 15.00–20.00 | S03_v01.png | Test assignment — exist. A few weeks later, his real employer will lose more than six billion dollars. |
| S05 | [600,750) | 20.00–25.00 | S04_v01.png | Fictional employer reveal — dollars. The trap looks convincing: the invitation comes through a real job platform, |
| S06 | [750,900) | 25.00–30.00 | 20_v01.png | Scale of coming loss — platform, the interviews are by video, and the recruiter even shows him her account, with personal |
| S07 | [900,1050) | 30.00–35.00 | S06_v01.png | Real job platform — photos and videos. It all leads to one thing: running the code. |
| S08 | [1050,1200) | 35.00–40.00 | S07_v01.png | Recruiter profile album — code. As he sets up the assignment, malware runs alongside it. Security systems miss |
| S09 | [1200,1350) | 40.00–45.00 | S08_v01.png | The task narrows to code — it, giving the attackers access to a computer inside Binance. According to Binance's |
| S10 | [1350,1500) | 45.00–50.00 | 25_v01.png | Malware alongside setup — Binance's preliminary findings, they use that computer to reach two more engineers' machines. |
| S11 | [1500,1650) | 50.00–55.00 | 16_v01.png | Access inside Binance — machines. Credentials found there give them access to the system that approves transfers from Binance wallets, |
| S12 | [1650,1800) | 55.00–60.00 | 19_v01.png | Missed warning and reset — wallets, allowing them to authorize transfers to addresses they control. On October 29, |
| S13 | [1800,1950) | 60.00–65.00 | 26_v01.png | Two other engineers — 29, crypto assets start moving to those addresses. Security flags the large transfers. |
| S14 | [1950,2100) | 65.00–70.00 | S09_v01.png | Wallet approval system — transfers. Binance halts ordinary withdrawals and, with its partners, tries to |
| S15 | [2100,2250) | 70.00–75.00 | S10_v01.png | Transfers begin — freeze the stolen assets. But that isn't enough. Through the compromised system, |
| S16 | [2250,2400) | 75.00–80.00 | S11_v01.png | Security response — system, the attackers manage to give another program permission to move crypto assets directly from |
| S17 | [2400,2550) | 80.00–85.00 | S12_v01.png | Ordinary withdrawals stop — a wallet on Ethereum. That program no longer needs Binance's ordinary withdrawal system. |
| S18 | [2550,2700) | 85.00–90.00 | 27_v01.png | Direct Ethereum permission — system. Binance has stopped that system, but the permission recorded on Ethereum remains |
| S19 | [2700,2850) | 90.00–95.00 | S13_v01.png | Revocation on-chain — active. Revoking it requires a separate operation on the blockchain itself. Turning |
| S20 | [2850,3000) | 95.00–100.00 | 17_v01.png | Two independent routes — Turning off withdrawals on Binance's website cannot cancel that permission. From the first transfers |
| S21 | [3000,3150) | 100.00–105.00 | 15_v01.png | Almost four hours — transfers to the finalization of the last transaction already sent, almost four hours |
| S22 | [3150,3300) | 105.00–110.00 | 28_v01.png | Final pending transfer and revocation — hours pass. The permission is revoked later, after midnight. The stolen crypto assets |
| S23 | [3300,3450) | 110.00–115.00 | S05_v01.png | $6.34B valuation — assets are valued at about $6.34 billion. About $2.85 |
| S24 | [3450,3600) | 115.00–120.00 | 21_v01.png | Frozen is not returned — $2.85 billion worth of those assets is frozen or intercepted — but that does |
| S25 | [3600,3750) | 120.00–125.00 | 22_v01.png | Binance covers loss — does not mean they have been returned. Binance says it will cover the loss with its own funds. |
| S26 | [3750,3930) | 125.00–131.00 | 23_v01.png | Interview trap callback — funds. The company he interviewed with never existed. His real employer had to face the consequences. |
| S27 | [3930,4080) | 131.00–136.00 | 29_v01.png | End screen 1 —  |
| S28 | [4080,4230) | 136.00–141.00 | 30_v01.png | End screen 2 —  |

Проверка партитуры до генерации/монтажа: последовательность создаёт смену задач и планов, а не повтор одинаковой иллюстрации. Мотивированный возврат к собеседованию в S26 закрывает ловушку из S01–S04. Сцены S27–S28 — конечный фон: 5 секунд каждый, зона подписки слева и две рекомендации справа свободны и постоянны; это не фальшивый интерфейс. Изображения фактически просмотрены контакт-листом; квалифицированный полный размер/phone-size review и итоговый композит остаются открыты до QA.
