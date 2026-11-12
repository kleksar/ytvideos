# ChatGPT Extra High — visible result

URL: https://chatgpt.com/c/6ae80c14-a574-83eb-931d-a8c094396de1
Visible effort: Extra High (4 из 5). Separate model name not visible.
Task: one reproducible candidate for a 15-second Paper Detour YouTube grain test; source 1080p/30, upscale before luma-only grain, no 15-minute overlay, distinguish sources and hypotheses. Full prompt remains at the linked conversation.
Visible final response (transcribed; table flattened):

Рекомендуемый кандидат: PD Grain 01
Один тестовый preset. Не утверждённый production-стандарт.
Зерно добавлять после upscale 1920×1080 → 3840×2160, в экранных координатах, непосредственно перед финальным кодированием. Не привязывать к слоям диорамы и движению камеры.
Тип: Monochrome Gaussian luma noise.
Пространственный размер: 1,5–2 UHD px, FWHM ≈ 1,6 px.
Максимальный luma RMS: 1,2 кода из 255.
Chroma noise: 0. Частота: 30 fps.
Temporal correlation: 0,65 между соседними кадрами.
Координаты: Screen-space, без pan/zoom.
Распределение: Изотропное, без направленных частот.
Маска яркости Y' (8-bit): ниже20 выключено;20–64 увеличение от0 до100%;64–208 полная интенсивность RMS1,2;208–244 уменьшение до нуля; выше244 выключено.
Это защищает глубокие тени и почти белые бумажные поверхности от заметных точек. RMS нормализовать после пространственной фильтрации и до применения маски.
Временная динамика: AR(1), коэффициент0,65:65% предыдущего состояния и35% нового независимого шума с нормализацией дисперсии. Зерно меняется во времени, но не создаёт резкого мерцания. Не использовать прокрутку текстуры.

Coordinator corrections: normalized AR innovation coefficient is sqrt(1-rho²), not 0.35; limited-range white is235 so mask endpoint adapted. No primary links were present in the visible final answer; independently checked sources and scope are in RESEARCH_AND_PRESET.md.
