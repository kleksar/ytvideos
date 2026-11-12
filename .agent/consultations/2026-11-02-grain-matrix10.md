# Grain matrix10 — completed personal Extra High consultation

- Coordinator: Codex/root, Google Chrome. Date:2026-11-02.
- URL: https://chatgpt.com/c/6ae819c4-39b0-83eb-be49-4786cd819bb9
- Immediately before both requests, visible exact label: `Extra High, 4 из 5. Используйте клавиши со стрелками влево и вправо для настройки мощности.` No distinct model name was shown. Pro not used.
- Scope: ten moderate controlled grain settings on one user-supplied watchmaker still;2560×1440/30p,120-frame holds and8-frame brief cards, silent, no camera/parallax or universal production change.
- Inputs: user request/image; priorTest01 RMS1.2/sigma0.68UHDpx nearly invisible;Test02 RMS4.8/sigma1.0UHDpx;Test03 RMS3.6/sigma1.15UHDpx/rho0.65, selection pending. Prompt describedTest02 as too strong; the exact evidence is that the user requested reducing amplitude, not an explicit universal rejection. Do not treat this wording as a new user verdict.

## Narrow prompt submitted

Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора выполнено этим обращением; дай ответ здесь, не открывай рекурсивно другой ChatGPT. Одна узкая задача: предложи таблицу РОВНО 10 осмысленных умеренных пресетов монохромного film grain для одного статичного бумажного кадра часовщика, чтобы пользователь выбрал визуально после YouTube. Выход2560×1440 30p SDR BT709 limited; каждый пресет4секунды, перед ним карточка8кадров (~267мс), номер/настройки внизу все4секунды. Исходник1672×940, масштабируем один раз. Новый звук и camera/parallax в этом сравнении не нужны. Предыдущие эмпирические тесты: при UHD3840×2160 RMS1.2 кодовых значенийY, Gaussian sigma0.68px, AR rho0.65 зерно было почти невидимо наYouTube. RMS4.8/sigma1.0px было слишком сильно, пользователь попросил×3 вместо×4 и крупнее: тест03 RMS3.6 sigma1.15px приUHD. Победителя пока нет. Не обещать сохранение зернаYouTube. ФормулаAR state=rho*old+sqrt(1-rho²)*innovation, инновации Gaussian-blurred unit std;Ynoise add afterRec709conversion,UVнеизменны. Мягкая маска защищает тени/блики(20/64/208/235limited) одинакова во всех пресетах. НазовиsigmaвПИКСЕЛЯХВЫХОДА1440p(тоесть2/3отUHDдля одинакового размера наэкране). АмплитудаRMSвYcodevalues,НЕнепрозрачность/не количество зерна. Частоту изменяем обновлением случайного поля30/15/10Гц с удержанием2/3кадра, итог30fps. Избегай10случайных комбинаций — предложи логическую матрицу вокруг базового умеренного варианта: отдельные изменения амплитуды/размера/обновления/rho;все10сзерном,без отдельного нулевого. Дай короткую таблицуID,английское имя,RMS,sigma,updateHz,rhoи зачем этот вариант. Без веб-поиска,без сценария и остальногоworkflow;это план контролируемого локального эксперимента,не окончательный стандарт.

First result had only status «Сформировала и уточнила матрицу вариантов и протокол», no substantive final answer. One short retry after recheckingExtraHigh:

> Сейчас виден только статус «Сформировала и уточнила матрицу вариантов и протокол», самой таблицы нет. Дай прямо здесь содержательный итог: ровно10строкID/name/RMS/sigma1440p/updateHz/rho,коротко. Не выполняй другие действия.

## Visible completed answer, read by coordinator

Базовый пресет —G01. G02–G09 изолированно изменяют один параметр. G10 —контрольное воспроизведение прежнегоTest03 с пересчитанным размером зерна для1440p.

|ID|Name|RMS(Ycodes)|sigma(1440ppx)|UpdateHz|rho|
|---|---|---|---|---|---|
|G01|Balanced Base|3.0|0.77|30|0.65|
|G02|Soft Amplitude|2.4|0.77|30|0.65|
|G03|Upper Amplitude|4.0|0.77|30|0.65|
|G04|Fine Grain|3.0|0.60|30|0.65|
|G05|Coarse Grain|3.0|0.95|30|0.65|
|G06|Slow Refresh15|3.0|0.77|15|0.65|
|G07|Slow Refresh10|3.0|0.77|10|0.65|
|G08|Short Persistence|3.0|0.77|30|0.35|
|G09|Long Persistence|3.0|0.77|30|0.85|
|G10|Test03 Reference|3.6|0.77|30|0.65|

Интерпретация различий: G02–G03 интенсивность;G04–G05 пространственный размер;G06–G07 временная частота обновления(удержание2или3кадра);G08–G09 временная устойчивость;G10 сопоставление с прежним тестомRMS3.6/UHDsigma1.15px. Во всех десяти одинаковая мягкая маска,Gaussianinnovation,AR-формула и неизменныеUV. RMSвкодовыхY,неopacity. YouTube может ослабить или полностью удалить различия;победитель только по визуальному сравнению.

## Adopted and checked

Adopted all ten numeric rows. RenamedG10 `Test 03 Scaled` to avoid implying exact reproduction of the old footage/encode.1.15×2/3=0.7667 rounded0.77. All10 have grain; eachG02–G09 differs fromG01 in exactly one parameter. Held-noise fields do not change output30fps. RMS is not opacity. Source is preserved in `new_channel/Shared/Experiments/Grain/20261102_watchmaker/Source/watchmaker_user.png`. Experiment presets/contract in its `Edit/Matrix10_v01/`. No general production acceptance; user picks after upload. Consultation is design advice, not a primary technical source or independentQA.
