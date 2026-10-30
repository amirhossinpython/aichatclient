<div align="center">

# 🤖 AiChatClient

### Build and manage AI assistants your own way
### دستیار هوش مصنوعی خودت را  بساز

[![PyPI](https://img.shields.io/pypi/v/aichatclient?logo=pypi&logoColor=white&color=3775A9)](https://pypi.org/project/aichatclient/)
[![Python](https://img.shields.io/pypi/pyversions/aichatclient?logo=python&logoColor=white)](https://pypi.org/project/aichatclient/)
[![Downloads](https://img.shields.io/pypi/dm/aichatclient?color=success)](https://pypi.org/project/aichatclient/)
![OpenAI Compatible](https://img.shields.io/badge/OpenAI-compatible-412991?logo=openai&logoColor=white)
![Flask](https://img.shields.io/badge/Web%20UI-Flask-000000?logo=flask&logoColor=white)

**🌐 Language / زبان:** &nbsp; [🇬🇧 English](#-english) &nbsp;|&nbsp; [🇮🇷 فارسی](#-فارسی)

```bash
pip install aichatclient
```

</div>

---

# 🇬🇧 English

AiChatClient is a Python toolkit for building custom assistant workflows on top of **OpenAI-compatible chat APIs**. You control the assistant's identity, instructions, reference data, memory, and saved configuration, in plain Python or through the bundled Flask web chat.

## ✨ Features

| | Feature | What you get |
|---|---|---|
| 💾 | Saved configurations | Create, load, list, rename, and delete assistants |
| 🔌 | Any compatible provider | Any OpenAI-compatible `base_url` + model name |
| 🎭 | Assistant behavior | System prompt, personality, expertise, limitations |
| 🧠 | Conversation memory | Messages persisted in SQLite and reused as context |
| 📚 | Reference datasets | `.txt`, `.json`, `.jsonl` with keyword-based matching |
| 🗂️ | Multiple conversations | Separate `conversation_id`, history inspection and cleanup |
| 🌐 | Web interface | Flask-based `ChatApp` |

> **Scope.** AiChatClient is a foundation for assistant workflows. It does **not** include autonomous task execution, built-in external tools, semantic/vector search, or an agent planner. Implement those in your application.

## 📦 Install

```bash
pip install aichatclient
python -m pip install --upgrade aichatclient   # upgrade
```

Requirements: a supported Python version (see package metadata), an API key, an OpenAI-compatible endpoint, and network access to it. The `openai` SDK and Flask are installed automatically.

## 🚀 Quick start

```bash
export AICUSTOM_API_KEY="your-api-key"      # PowerShell: $env:AICUSTOM_API_KEY = "your-api-key"
```

```python
import os
from aichatclient import AICustom

assistant = AICustom(
    api_key=os.environ["AICUSTOM_API_KEY"],
    base_url="https://api.example.com/v1",
    model_name="provider/model-name",
    nickname="my_assistant",
    system_prompt="You are a helpful programming assistant.",
)
assistant.create_model()        # saves the config (the API key is NEVER saved)

print(assistant.chat("Hello! What can you help me with?"))

for m in assistant.get_history(limit=10):
    print(m["role"], m["content"])
```

Next time, just load it:

```python
assistant = AICustom.load_model("my_assistant")   # key from AICUSTOM_API_KEY
```

## 🧩 Core classes

| Class | Role |
|---|---|
| `AICustom` | Configuration, chat, memory, datasets, model management. Use it for everything. |
| `AiClient` | Thin wrapper: load a saved model, chat, read history. Underlying model: `client.ai`. |
| `ChatApp` | Flask web chat around an `AICustom` instance. |

## 🛠️ Create an assistant

```python
assistant = AICustom(
    api_key=api_key,
    base_url="https://api.example.com/v1",
    model_name="provider/model-name",
    nickname="python_mentor",
    system_prompt="You are a Python mentor. Explain accurately with small examples.",
    personality="Patient, clear, and practical",
    expertise="Python programming",
    limitations="If uncertain, say so.",
    memory=True,
    conversation_id="learning-session-1",
)
assistant.create_model()
```

| Parameter | Default | Description |
|---|---|---|
| `api_key` | required | Provider key, used at runtime, **never saved** |
| `base_url` | required | OpenAI-compatible API base URL |
| `model_name` | required | Model identifier sent to the provider |
| `nickname` | required | Local name (letters, digits, `_`, `-`, `.`) |
| `system_prompt` | `""` | Role and response instructions |
| `model_provider` / `model_version` / `author` | `""` | Descriptive metadata |
| `personality` / `expertise` / `limitations` | `None` | Merged into the system message |
| `dataset` | `None` | Path to `.txt` / `.json` / `.jsonl` |
| `memory` | `True` | Store messages and reuse recent history |
| `conversation_id` | `"default"` | Keeps conversations separate |
| `storage_dir` | `None` | Storage root |
| `timeout` | `60.0` | Seconds (> 0) |
| `max_retries` | `2` | SDK retries (≥ 0) |
| `history_limit` | `40` | Max recent messages used as context (≥ 1) |
| `extra_model_params` | `None` | e.g. `{"temperature": 0.4}`; cannot override `model`/`messages` |
| `model_id` | auto UUID | Stable instance identifier |

## 💬 Load and chat

```python
assistant = AICustom.load_model(
    "my_assistant",
    api_key=api_key,                       # optional if AICUSTOM_API_KEY is set
    conversation_id="support-session-42",  # overrides apply to this instance only
    timeout=90,
)

assistant.chat("Explain Python decorators.")
assistant.chat("What is a decorator?", short=True)   # brief, direct reply
```

Overrides don't change the saved file; call `create_model()` to persist them. Lightweight wrapper:

```python
from aichatclient.aiclient import AiClient

client = AiClient.load_model(name="my_assistant", api_key=api_key)
client.chat("Lists vs tuples?")
client.get_history(limit=25)
```

## 🧠 Memory & history

```python
assistant.get_history(limit=20)                         # current model + conversation
AICustom.list_history(nickname="my_assistant",
                      conversation_id="default", limit=100)
assistant.clear_history()                               # returns deleted row count
AICustom.clear_all_history(nickname="my_assistant",
                           conversation_id="support-session-42")
```

> ⚠️ `AICustom.clear_all_history()` with no filters deletes **every** message in the database. Config files are not affected.

- **Separate conversations:** use a different `conversation_id` per user/session. IDs are labels, not access control.
- **Disable memory:** `memory=False`. Nothing is sent from history or saved; existing history stays.

## 📚 Reference datasets

```python
assistant = AICustom(
    api_key=api_key,
    base_url="https://api.example.com/v1",
    model_name="provider/model-name",
    nickname="product_helper",
    system_prompt="Answer using the supplied product data.",
    dataset="data/products.jsonl",
)
```

Simple **token-overlap matching** adds up to five matching lines (within a context-size limit) to the system message. It is *not* embedding search, a vector DB, or fine-tuning.

## 🗃️ Manage saved models

```python
assistant.create_model()                              # save non-secret config
AICustom.list_models(storage_dir="./assistant_data")  # sorted names
AICustom.delete_model("my_assistant")                 # config only; history is kept
assistant.rename_model("support_assistant")           # FileExistsError if taken
```

## 🌐 Web chat

```python
from aichatclient import AICustom, ChatApp

ai = AICustom.load_model("my_assistant")
ChatApp(ai=ai).run(host="127.0.0.1", port=5000, debug=False)
```

Open `http://127.0.0.1:5000`. Keep `host="127.0.0.1"` and `debug=False` unless you have deliberately secured the deployment.

## 📁 Storage & environment variables

```text
.ai_custom/
├── configs/<nickname>.json      # non-secret configuration
├── databases/history.sqlite3    # conversation history
├── datasets/
└── logs/
```

| Variable | Purpose |
|---|---|
| `AICUSTOM_HOME` | Default storage root (`storage_dir` takes precedence) |
| `AICUSTOM_API_KEY` | Default key for `AICustom.load_model()` |

## 🧯 Errors & troubleshooting

| Exception | Typical cause |
|---|---|
| `ValueError` | Empty required text, invalid options, missing API key, bad dataset |
| `TypeError` | Wrong parameter type (e.g. non-boolean `memory`) |
| `FileNotFoundError` | Saved model or dataset not found |
| `FileExistsError` | Rename target already exists |
| `RuntimeError` | API returned no choices or text |

- **Missing API key:** pass `api_key=` or set `AICUSTOM_API_KEY`. Keys are never stored, so each process needs one.
- **Model not found:** check `AICustom.list_models()` and the same `storage_dir` / `AICUSTOM_HOME`.
- **Empty history:** history is per model *and* `conversation_id`; check `memory=True`.
- **Provider rejects a request:** remove unsupported `extra_model_params`; verify `base_url` and `model_name`.

## 🔐 Security

1. Never hard-code or commit API keys. If a key was ever exposed, **revoke it and create a new one**.
2. Don't commit `.ai_custom/`, history databases, or private datasets.
3. Protect the storage directory; history may contain sensitive data.
4. Authenticate and authorize users in your own app.
5. Treat dataset files as untrusted input.
6. Use HTTPS endpoints.
7. Double-check the scope before `clear_all_history()`.

---

# 🇮🇷 فارسی

<div dir="rtl" align="right">

**AiChatClient** یک ابزار پایتونی برای ساخت دستیارهای هوش مصنوعی سفارشی روی **APIهای چت سازگار با OpenAI** است. هویت دستیار، دستورالعمل‌ها، داده‌های مرجع، حافظه و تنظیمات ذخیره‌شده دست خودت است. هم در کد پایتون کار می‌کند و هم با رابط وب Flask که همراه بسته است.

## ✨ ویژگی‌ها

| | ویژگی | توضیح |
|---|---|---|
| 💾 | تنظیمات ذخیره‌شده | ساخت، بارگذاری، فهرست، تغییر نام و حذف دستیار |
| 🔌 | هر سرویس‌دهنده سازگار | هر `base_url` سازگار با OpenAI به‌همراه نام مدل |
| 🎭 | رفتار دستیار | پرامپت سیستمی، شخصیت، تخصص و محدودیت‌ها |
| 🧠 | حافظه گفتگو | ذخیره پیام‌ها در SQLite و استفاده مجدد به‌عنوان زمینه |
| 📚 | دیتاست مرجع | فایل‌های `.txt` و `.json` و `.jsonl` با تطبیق کلیدواژه‌ای |
| 🗂️ | چند گفتگوی مستقل | `conversation_id` جدا، مشاهده و پاک‌سازی تاریخچه |
| 🌐 | رابط وب | `ChatApp` مبتنی بر Flask |

> **دامنه کار:** AiChatClient پایه‌ای برای ساخت دستیار است. اجرای خودکار کارها، ابزارهای بیرونی داخلی، جست‌وجوی معنایی (برداری) و برنامه‌ریز عامل (Agent) **ندارد**. این‌ها را باید در برنامه‌ی خودت پیاده کنی.

## 📦 نصب

</div>

```bash
pip install aichatclient
python -m pip install --upgrade aichatclient   # به‌روزرسانی
```

<div dir="rtl" align="right">

پیش‌نیازها: نسخه‌ی پشتیبانی‌شده‌ی پایتون (در متادیتای بسته ببین)، یک کلید API، یک endpoint سازگار با OpenAI و دسترسی شبکه به آن. کتابخانه‌ی `openai` و Flask خودکار نصب می‌شوند.

## 🚀 شروع سریع

ابتدا کلید را در متغیر محیطی بگذار (نه داخل کد):

</div>

```bash
export AICUSTOM_API_KEY="your-api-key"      # PowerShell: $env:AICUSTOM_API_KEY = "your-api-key"
```

```python
import os
from aichatclient import AICustom

assistant = AICustom(
    api_key=os.environ["AICUSTOM_API_KEY"],
    base_url="https://api.example.com/v1",
    model_name="provider/model-name",
    nickname="my_assistant",
    system_prompt="تو یک دستیار برنامه‌نویسی مفید هستی.",
)
assistant.create_model()        # تنظیمات ذخیره می‌شود (کلید API هرگز ذخیره نمی‌شود)

print(assistant.chat("سلام! چه کمکی از تو برمی‌آید؟"))

for m in assistant.get_history(limit=10):
    print(m["role"], m["content"])
```

<div dir="rtl" align="right">

دفعه‌ی بعد فقط بارگذاری کن:

</div>

```python
assistant = AICustom.load_model("my_assistant")   # کلید از AICUSTOM_API_KEY خوانده می‌شود
```

<div dir="rtl" align="right">

## 🧩 کلاس‌های اصلی

| کلاس | نقش |
|---|---|
| `AICustom` | تنظیمات، چت، حافظه، دیتاست و مدیریت مدل‌ها. برای همه‌چیز از همین استفاده کن. |
| `AiClient` | پوشش سبک: بارگذاری مدل ذخیره‌شده، چت و خواندن تاریخچه. مدل اصلی: `client.ai` |
| `ChatApp` | چت وب مبتنی بر Flask روی یک نمونه‌ی `AICustom` |

## 🛠️ ساخت دستیار

| پارامتر | پیش‌فرض | توضیح |
|---|---|---|
| `api_key` | الزامی | کلید سرویس‌دهنده؛ فقط هنگام اجرا استفاده می‌شود و **ذخیره نمی‌شود** |
| `base_url` | الزامی | آدرس پایه‌ی API سازگار با OpenAI |
| `model_name` | الزامی | شناسه‌ی مدل |
| `nickname` | الزامی | نام محلی (حروف، عدد، `_` و `-` و `.`) |
| `system_prompt` | `""` | نقش و دستورالعمل پاسخ‌گویی |
| `model_provider` / `model_version` / `author` | `""` | اطلاعات توصیفی |
| `personality` / `expertise` / `limitations` | `None` | به پیام سیستمی اضافه می‌شوند |
| `dataset` | `None` | مسیر فایل `.txt` یا `.json` یا `.jsonl` |
| `memory` | `True` | ذخیره‌ی پیام‌ها و استفاده از تاریخچه‌ی اخیر |
| `conversation_id` | `"default"` | جداسازی گفتگوها |
| `storage_dir` | `None` | پوشه‌ی ریشه‌ی ذخیره‌سازی |
| `timeout` | `60.0` | ثانیه (بزرگ‌تر از صفر) |
| `max_retries` | `2` | تعداد تلاش مجدد (≥ ۰) |
| `history_limit` | `40` | حداکثر پیام اخیر در زمینه (≥ ۱) |
| `extra_model_params` | `None` | مثلاً `{"temperature": 0.4}`؛ نمی‌تواند `model` و `messages` را بازنویسی کند |
| `model_id` | UUID خودکار | شناسه‌ی پایدار نمونه |

فیلدهای شخصیت و تخصص مدل را راهنمایی می‌کنند، اما جایگزین اعتبارسنجی، احراز هویت و کنترل‌های ایمنی در برنامه‌ی تو نیستند.

## 💬 بارگذاری و چت

</div>

```python
assistant = AICustom.load_model(
    "my_assistant",
    api_key=api_key,                       # اگر AICUSTOM_API_KEY تنظیم باشد اختیاری است
    conversation_id="support-session-42",  # فقط روی همین نمونه اعمال می‌شود
    timeout=90,
)

assistant.chat("دکوراتور در پایتون چیست؟")
assistant.chat("دکوراتور چیست؟", short=True)   # پاسخ کوتاه و مستقیم
```

<div dir="rtl" align="right">

مقادیر override فایل ذخیره‌شده را تغییر نمی‌دهند؛ برای ماندگار کردن آن‌ها `create_model()` را صدا بزن. نسخه‌ی سبک:

</div>

```python
from aichatclient import AiClient

client = AiClient.load_model(name="my_assistant", api_key=api_key)
client.chat("تفاوت list و tuple چیست؟")
client.get_history(limit=25)
```

<div dir="rtl" align="right">

## 🧠 حافظه و تاریخچه

</div>

```python
assistant.get_history(limit=20)                         # مدل و گفتگوی فعلی
AICustom.list_history(nickname="my_assistant",
                      conversation_id="default", limit=100)
assistant.clear_history()                               # تعداد ردیف‌های حذف‌شده را برمی‌گرداند
AICustom.clear_all_history(nickname="my_assistant",
                           conversation_id="support-session-42")
```

<div dir="rtl" align="right">

> ⚠️ **هشدار:** `AICustom.clear_all_history()` بدون فیلتر، **همه‌ی** پیام‌های دیتابیس را پاک می‌کند. فایل‌های تنظیمات دست‌نخورده می‌مانند.

- **گفتگوهای جدا:** برای هر کاربر یا نشست یک `conversation_id` متفاوت بده. این شناسه فقط برچسب است، نه کنترل دسترسی.
- **خاموش کردن حافظه:** با `memory=False` نه تاریخچه به مدل می‌رسد و نه پیام جدیدی ذخیره می‌شود. تاریخچه‌ی قبلی حذف نمی‌شود.

## 📚 دیتاست مرجع

</div>

```python
assistant = AICustom(
    api_key=api_key,
    base_url="https://api.example.com/v1",
    model_name="provider/model-name",
    nickname="product_helper",
    system_prompt="فقط بر اساس داده‌های محصول پاسخ بده.",
    dataset="data/products.jsonl",
)
```

<div dir="rtl" align="right">

با یک **تطبیق ساده‌ی هم‌پوشانی کلمات**، حداکثر پنج خط مرتبط (در محدوده‌ی اندازه‌ی زمینه) به پیام سیستمی اضافه می‌شود. این روش جست‌وجوی معنایی، دیتابیس برداری یا فاین‌تیون **نیست**.

## 🗃️ مدیریت مدل‌های ذخیره‌شده

</div>

```python
assistant.create_model()                              # ذخیره‌ی تنظیمات غیرمحرمانه
AICustom.list_models(storage_dir="./assistant_data")  # فهرست مرتب‌شده‌ی نام‌ها
AICustom.delete_model("my_assistant")                 # فقط تنظیمات؛ تاریخچه می‌ماند
assistant.rename_model("support_assistant")           # اگر نام تکراری باشد FileExistsError
```

<div dir="rtl" align="right">

## 🌐 چت وب

</div>

```python
from aichatclient import AICustom, ChatApp

ai = AICustom.load_model("my_assistant")
ChatApp(ai=ai).run(host="127.0.0.1", port=5000, debug=False)
```

<div dir="rtl" align="right">

آدرس `http://127.0.0.1:5000` را باز کن. مگر اینکه استقرار را عمداً امن کرده باشی، `host="127.0.0.1"` و `debug=False` را نگه دار.

## 📁 ذخیره‌سازی و متغیرهای محیطی

</div>

```text
.ai_custom/
├── configs/<nickname>.json      # تنظیمات غیرمحرمانه
├── databases/history.sqlite3    # تاریخچه‌ی گفتگو
├── datasets/
└── logs/
```

<div dir="rtl" align="right">

| متغیر | کاربرد |
|---|---|
| `AICUSTOM_HOME` | پوشه‌ی پیش‌فرض ذخیره‌سازی (آرگومان `storage_dir` اولویت دارد) |
| `AICUSTOM_API_KEY` | کلید پیش‌فرض برای `AICustom.load_model()` |

## 🧯 خطاها و رفع اشکال

| استثنا | علت معمول |
|---|---|
| `ValueError` | متن الزامی خالی، گزینه‌ی نامعتبر، نبود کلید API، دیتاست نامعتبر |
| `TypeError` | نوع پارامتر اشتباه (مثلاً `memory` غیر بولی) |
| `FileNotFoundError` | مدل ذخیره‌شده یا فایل دیتاست پیدا نشد |
| `FileExistsError` | نام مقصد در تغییر نام از قبل وجود دارد |
| `RuntimeError` | API پاسخ یا متنی برنگرداند |

- **کلید API پیدا نشد:** `api_key=` بده یا `AICUSTOM_API_KEY` را تنظیم کن. کلید هرگز ذخیره نمی‌شود، پس هر پردازش جدید به آن نیاز دارد.
- **مدل پیدا نشد:** `AICustom.list_models()` را بررسی کن و مطمئن شو `storage_dir` یا `AICUSTOM_HOME` همان است که هنگام ذخیره بود.
- **تاریخچه خالی است:** تاریخچه به مدل **و** `conversation_id` وابسته است؛ `memory=True` را هم چک کن.
- **سرویس‌دهنده درخواست را رد می‌کند:** پارامترهای پشتیبانی‌نشده را از `extra_model_params` حذف کن و `base_url` و `model_name` را بررسی کن.

## 🔐 امنیت

1. کلید API را هرگز در کد نگذار و commit نکن. اگر کلیدی لو رفته، **همان لحظه آن را باطل (revoke) و کلید جدید بساز**.
2. پوشه‌ی `.ai_custom/`، دیتابیس تاریخچه و دیتاست‌های خصوصی را commit نکن.
3. پوشه‌ی ذخیره‌سازی را محافظت کن؛ تاریخچه ممکن است اطلاعات حساس داشته باشد.
4. احراز هویت و سطح دسترسی کاربران را در برنامه‌ی خودت پیاده کن.
5. فایل‌های دیتاست را ورودی غیرقابل‌اعتماد در نظر بگیر.
6. از endpointهای HTTPS استفاده کن.
7. پیش از `clear_all_history()` دامنه‌ی حذف را دوباره بررسی کن.

</div>

---

<div align="center">

📄 License: see the [GitHub repository](https://github.com/amirhossinpython/aichatclient) &nbsp;|&nbsp; مجوز: به مخزن گیت‌هاب مراجعه کنید

</div>
