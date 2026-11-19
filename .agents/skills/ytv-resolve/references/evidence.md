# Проверенная база и границы

Skill revision: **1**, 2026-11-19. Это перенос проверенного опыта в общий будущий workflow, не заявление о проверке всех каналов/версий Resolve.

## Локальные проверки производства

Передано выполнявшим Mac-проверки production worker: Studio **21**, package bundle **21.2.0**. Проверены project manager Create/Load, SetSetting, SaveProject, `MediaPool.ImportTimelineFromFile`, native H.264/AAC Deliver queue, editable cuts/overlays и export decode для 1920×1080/30 и 1080×1920/30. При ошибочном sequence inference numbered PNG проверено исправление exact-length uniquely named ProRes carriers, 4444 для alpha, с read-back концов клипов. Проверены отдельные authored SFX clips на нескольких lanes; legacy audio underlay оставался baked. SRT в Media Pool не проверяет его применение к subtitle track. Эта запись основана на отчёте worker, не на повторном live-тесте при создании skill.

В существующем repo episode Work остаются builder/manifest/QA, включая `channels/scenes_on_repeat/videos/ybw06_fix_anything/Work/resolve-v02`; это локальные production evidence, не обещание наличия тяжёлых файлов в Git или полный универсальный renderer. Точные scene/track/frame counts отдельных тестов не являются правилом будущего выпуска. Проверять фактическую установленную версию/API и требуемый режим перед работой.

## Платформа и источники

- [Blackmagic Resolve 21.1 Reference Manual](https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21.1_Reference_Manual.pdf): System Preferences → Internet Accounts; Deliver. Документирует social account integration; это не receipt успешного upload из текущей установки 21.2.0.
- [YouTube: Related video](https://support.google.com/youtube/answer/14075157): advanced feature access, public/unlisted цель собственного канала.
- [YouTube: thumbnails](https://support.google.com/youtube/answer/72431): проверка аккаунта/доступность функции. При выпуске сверить актуальный Help и реальный Studio, не фиксировать навсегда ограничения конкретного UI.

По состоянию этой записи Resolve YouTube upload **не выполнен end-to-end**. Поля Deliver подтверждены screenshot владельца, не automation API. Успешный upload через Chrome/Studio не является проверкой Resolve upload. При первой фактической проверке обновить этот reference точной версией, scope и результатом без credentials/private links; не расширять гарантию на непроверенные controls.
