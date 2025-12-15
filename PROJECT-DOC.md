# PROJECT-DOC вЂ” Product rules (SSoT after api-contracts.yaml and PROJECT-RULES.md)

## Purpose
This document fixes product/business rules that are NOT represented in OpenAPI contracts.
Goal: avoid repeated clarification and вЂњguessworkвЂќ during backend implementation.

## Core workflow (User в†’ Moderator в†’ Auto-delivery)
### 1) Request creation and keys
- A user creates a Request and provides a list of вЂњkeysвЂќ (positions).
- Keys can be entered manually or produced by file recognition (planned: OpenAI-based parsing that converts a file into keys).
- User reviews the recognized keys and confirms the Request is correct.

### 2) вЂњGet supplier contactsвЂќ action (start matching + create moderator task)
When user triggers вЂњGet supplier contactsвЂќ:
- System performs matching for each key against existing database knowledge.
- In parallel, the system creates a Moderator Task for this Request (Request is split by keys for processing).

### 3) Moderator parsing flow
- Moderator opens the task for the Request and runs a parser (search-engine based).
- The parser runs each key through Google and Yandex and returns a list of URLs per key.

### 4) URL handling and delivery to user
For each URL returned by the parser:
- If the URL is already present in the DB AND is moderated (see definition below),
  then supplier contact info is immediately delivered to the userвЂ™s cabinet
  and linked to this Request + the specific key that produced the URL.
- If the URL is new or not moderated, it goes through moderation.
  As soon as the moderator confirms it and links it to the key, it is delivered to the user.

## What user sees in cabinet (Supplier card)
For each supplier delivered to the user, the UI must provide at least:
- Company name
- INN
- Company URL
- Additional company info fetched from Checko API (when available)
- Ability to send a request to the supplier (messaging flow)

## Definition: вЂњModerated supplier / moderated URLвЂќ (hard requirement)
A company/URL can be stored as a вЂњusable supplierвЂќ only if the moderator linked:
- Company URL
- INN
- Company name
- Sales email (contact email of sales department)
Only after that the supplier is considered moderated and can be delivered to users automatically.

## Matching rules: вЂњsimilar keyвЂќ (MVP в†’ improvements)
### Goal
Matching must return truly relevant suppliers for a key.
Example: key вЂњС„Р»Р°РЅРµС† d100вЂќ should match a DB key like вЂњС„Р»Р°РЅРµС† РїР»РѕСЃРєРёР№ d100вЂќ.

### Recommended MVP approach (deterministic and explainable)
1) Normalize key text:
   - Lowercase, trim spaces, unify symbols (e.g., d/Гё/Рґ), normalize вЂњС‘/РµвЂќ.
   - Keep numeric/size tokens as first-class signals (e.g., 100).
2) Extract вЂњrequired parametersвЂќ:
   - Sizes/diameters (d=100), GOST, steel grade, etc. (pattern-based).
3) Matching decision:
   - Required parameters must match (e.g., d=100).
   - Text similarity must be above a threshold (implementation choice: token overlap or trigram similarity).
4) Explainability:
   - Store why the match happened (matched parameters + matched tokens) to avoid opaque behavior.

### Notes
- Thresholds and exact algorithm are subject to tuning based on real data.
- Avoid ML/black-box matching in MVP; start with deterministic matching.

## Data linking requirements (conceptual)
- Every delivered supplier must be linked to:
  - Request (requestId)
  - Key (keyId/pos) that produced the supplier
  - Source URL (and whether it was DB-known or parser-discovered)

## Open questions (to be decided later, not blocking MVP)
- How Checko API data is cached and refreshed.
- Exact UI layout of supplier card (only minimum fields are fixed above).
- Parser script integration details and operational constraints.

## Поставщики: поиск и доступы

- Поиск поставщиков по строке: модератор использует в админке.
- Модератор может включать/выключать доступность строки поиска для пользователей из своего ЛК (фича-флаг).
- По умолчанию в пользовательском интерфейсе строка поиска скрыта (пока модератор не включил).
- Данные поставщика: ИНН строго один на поставщика.
- Данные поставщика: URL у поставщика может быть несколько (редко, но возможно).
- Уникальность URL: один сайт (URL) не может принадлежать двум поставщикам (глобальная уникальность).

## Дубли по ИНН (ModeratorSuppliers)

Если модератор пытается создать поставщика с ИНН, который уже существует в базе, создание блокируется.

API: POST /apiv1/moderator/suppliers возвращает 409 Duplicate INN с телом DuplicateInnErrorDTO.

UI: открывается экран сравнения дублей:
- Слева: incomingurl (+ введённый ИНН/название если есть)
- Справа: существующая компания (supplierid, name) и все её urls (кликабельные, открываются в новой вкладке)
- Действие: только "перейти в карточку предприятия"
