# Paper — технический вход

Новый run создаёт общий CLI `python -m ytvideos`; не требуется отсутствующий `init_episode.py` или локальный episode registry. [Workflow](../../../docs/workflow.md) задаёт две контрольные точки, [PROFILE](../PROFILE.md) — Paper recipe.

Технические средства находятся в общем [automation](../../../automation/README.md) и вызываются guarded adapters. Media paths остаются в run/artifact storage. Specific legacy project scripts не являются универсальным entrypoint новых выпусков.
