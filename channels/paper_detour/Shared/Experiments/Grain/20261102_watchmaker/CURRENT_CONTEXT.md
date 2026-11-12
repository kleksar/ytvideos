# Paper Detour — ten grain presets with identical camera/parallax

**G08_ACCEPTED_COMMON_PRESET** (2026-11-02). Пользователь выбрал №8 Short Persistence для общего применения вместе с анимацией и параллаксом. [Принятие](Edit/G08_ACCEPTANCE_20261102.md), [машинный пресет](/Users/diplomat/ytvideos/automation/image_motion/grain_presets.json). Общая автоматизация: `automation/image_motion/run.py apply --config /absolute/episode/Edit/ImageMotion/motion.json`; default `grain:g08`, явный `grain:none` оставляет camera/parallax-only. Порядок parallax→camera→grain; camera запечена в finished derivative, target transform identity. [Контракт](/Users/diplomat/ytvideos/.agents/skills/ytv-image-motion/references/grain.md). Реализация выполнена после прямого task-specific разрешения пользователя продолжить без Extra High: [запись](/Users/diplomat/ytvideos/.agent/consultations/2026-11-02-g08-integration.md). Технические проверки: `Edit/CommonG08/`; live Palmier применение нового пути к фильмам не выполнялось.

**PRIVATE_YOUTUBE_COMPARISON_READY**. [CurrentYouTubev02](https://www.youtube.com/watch?v=W1ap6Q8Otuo),ID`W1ap6Q8Otuo`,PaperDetour`UCMVfdfaNxV3ZkI3_J3Eejzw`. APIprivate/processed/succeededandmetadatareadbackPASS. Playeractual2560×1440@30/VP9(271)/BT709verified.

User explicitly requested the same animation/parallax throughout,subtleleft-to-rightmovement,1secondsettingcardsandnewupload. Tenunchangedgrainpresets;each30framecardthen120framemovingimage=1500frames/50seconds,2560×1440/30p,silent. Settingsalsoremainvisiblebelowimage.

Canonical`gentle-aligned`:offset0.165,height0.26,steady0,stickytrue;pan-rightcamera_factor0.75,scale1.10,centreX0.4775→0.5225(+115.2outputpx),depth_zoom1.00,finalsign−1. Sharedhelperdepth/cacheandcamera_keysreused,nostandalonereimplementationofparallax. Onecommon120framecolour-convertedcamera/depthsequencerepeatedidenticallyinall10variants.15/10Hzgrainholdsonlynoisefield,notvideo;all120decodedmotionframesineachvariantdistinct.

Source:[preservedPNG](Source/watchmaker_user.png),SHA256`151cb0e796053eccd9726099c8feabd7ac1dbc4d302cb1e63cc27612a643e733`. [Presetmatrix](Edit/Matrix10_v02/presets.json),[frozenexportcontract](Edit/Matrix10_v02/EXPORT_CONTRACT_v02.json),[motionreceipt](Edit/Matrix10_v02/motion_receipt.json),[directionproof](Edit/Matrix10_v02/MOTION_DIRECTION.json),[renderreceipt](Edit/Matrix10_v02/render_receipt.json),[QA](Edit/Matrix10_v02/QA/REPORT.json),[YouTubereceipt](Edit/Matrix10_v02/youtube_receipt.json).

[CurrentlocalMP4](Work/matrix10-v02-motion/previews/PAPER_DETOUR_GRAIN_10_PRESETS_MOTION_1440P_v02.mp4),SHA256`eb644c11bb3f91e8b9ed71fc9085f674b3508f82670e90e747ccad4cda6d80f2`,347737252bytes. Pending/pinnedcomparison;runmatrix10-v02-motion,codex-grain-matrix-v02finished.

ScopedlocaltechnicalQApassed:1500decoded/hashcountedframes,packetPTS30fps/zero-start,50seconds,H264High,YUV420p,BT709limited,SAR1:1,FastStart. Authorinspected70actualfinalfileframescoveringall10cardbeginnings/endingsandall10imageholdsbegin/quarter/mid/quarter/end,10labelstrips,plus13preflightmotionpositions. Normalizedfeaturematchingconfirmedrightwardmovementonface,hands,watch,cupandbackground;foregroundmovesmorethanbackground. Noemptyedgesorcriticalface/hand/watchcroppingobservedinsamples;existingtophaircropretained. Self-review,notindependentreview;continuoussubjectivecomparisonnotperformed;userselectedG08on2026-11-02.

[Previousstaticv01comparison](https://www.youtube.com/watch?v=OFqQ5PQwyMI)retained/pinnedascontrol,notdeletedlocallyorYouTube;[previouscontext](Edit/Matrix10_v02/CONTEXT_BEFORE_MOTION.md). Nosource/Palmierproject/productionepisodechanged;commonG08presetacceptedon2026-11-02;existingproductionfilmsunchanged.

Storagefollow-up:11registeredownedrawscratchfilesremovedafterQA,logical60825600bytes,physicalAPFSreclaimunknown. OriginalPNG,shareddepth/motioncache,allQAandbothprivatecomparisonMP4sretained/pinned. [Post-uploadaudit](Edit/MediaLifecycle/v02-postupload-audit/audit.json) / [plan](Edit/MediaLifecycle/v02-postupload-plan/plan.json).


## Общий G08: результат автоматизации

[Implementation](Edit/CommonG08/IMPLEMENTATION.md), [QA](Edit/CommonG08/QA.json), [cache repeat](Edit/CommonG08/cache_repeat.json). 15 tests PASS; wide1440p/portrait1080p full decode PASS; actual sampled author review wide0/60/119. Completed repeat reused clean and finished caches in 0.294 seconds for this local pipeline check; not a whole-timeline performance guarantee. Live Palmier grain apply NOT_PERFORMED. Ни один производственный timeline или YouTube upload не изменён.

Storage: owned run `common-g08-v01` complete, writer finished; synthetic portrait preview registered pending. Bounded post-QA audit `Edit/MediaLifecycle/common-g08-postqa/audit.json` reported zero coverage errors; plan at `Edit/MediaLifecycle/common-g08-plan/plan.json`. No shared cache, source, comparison or external asset was deleted.
