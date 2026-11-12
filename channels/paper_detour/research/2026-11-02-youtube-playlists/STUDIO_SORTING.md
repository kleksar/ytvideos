# Studio-only sorting setting

2026-11-02 Europe/Belgrade. Target channel independently verified in Studio header URL: UCMVfdfaNxV3ZkI3_J3Eejzw. Digital Life playlist: PLCAXo3w7Gths.

API capability gap: the current playlists resource/update schema has no default sorting-mode field. A position-bearing membership insert returned HTTP 400 manualSortRequired: “Playlist should use manual sorting to support position.” The complete read-only AFTER_REJECTED_POSITION.json confirms no new item; the original failure receipt is retained and marked rejected_no_membership_observed.

Studio showed **По дате публикации (сначала новые)**, contradicting the old registry's Manual assumption. Coordinator selected **Как указано вручную на YouTube**. Studio initially showed language **Выбрать**, despite the preceding API description/defaultLanguage update read-back; selected **Английский** in the same form. Before save the actual DOM description was checked against the freshly updated AI-companions text. Public access retained. After Save, both action buttons became disabled and the selected Manual/English/Public values remained visible. [Screenshot](digital_settings_saved.png).

This resolves the concrete API error; it is not a fallback to UI for membership writes. The next insert uses API after fresh deduplication and a separately named receipt. Do not retry the failed request blindly or erase its history. Other playlist sorting settings require their own current check.

The same coordinator then opened Real Stories & Discoveries and Legends & Personal Stories by their explicit IDs. Both currently showed Manual/Public with disabled save buttons, without edits; [Real screenshot](real_settings_checked.png), [Legends screenshot](legends_settings_checked.png). The newly created Reported IQ Estimates (`PLOSBLM3rTTl0`) already showed Manual/Private before its first membership insert; [IQ screenshot](iq_settings_checked.png).

Language evidence is kept distinct: API returns `defaultLanguage=en` for all four. Studio's language chooser still showed `Выбрать` on Real, Legends and IQ; those forms were not changed. Only Digital's English chooser was explicitly saved here. Do not claim all four Studio language controls were verified English. Sorting-mode checks and API content order are separately verified.
