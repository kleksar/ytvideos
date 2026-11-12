# Nuviko storage inventory — consultation

Mode visibly checked before request: `Extra High, 4 из 5`. Chrome project chat: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aea17e9-ed78-83ed-899b-a9e5accc7a57

Prompt: Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора уже выполнено этим обращением; дай ответ здесь, не открывай другой ChatGPT. Одна узкая задача: как корректно сопоставить локальные папки проектов с фактическим каталогом YouTube для отчёта о занимаемом месте, избегая двойного счёта общих файлов и ошибочной трактовки доступности? Дай краткие критерии без удаления файлов.

Completed response: Build separate local and remote inventories; link using channel/video IDs and upload receipts, with title/duration as candidates only. Record privacy and processing independently. Count symlinks and hard links carefully and shared assets only once; equal hashes alone do not establish saved disk space. Distinguish logical and allocated sizes and acknowledge APFS clones/snapshots. API errors or missing access mean unknown. Track evidence and time. Work read-only.

Accepted: apply ID/receipt matching, separate channels and statuses, report directory measurements with APFS and shared-resource limitations; do not infer deletability. Consultant is not evidence for actual inventories.
