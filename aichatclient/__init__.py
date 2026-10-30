"""
aichatclient
============

Build and manage AI assistants your own way, on top of any OpenAI-compatible
chat API.  ساخت و مدیریت دستیار هوش مصنوعی روی هر API سازگار با OpenAI.

Public API
----------
``AICustom``
    Configuration + chat + memory + datasets + model management.
    Use this class for everything.
``AiClient``
    Thin wrapper: load a saved model, chat, read history.
``ChatApp``
    Flask-based web chat around an ``AICustom`` instance.

Quick tutorial
--------------
1. Set your API key (never hard-code it)::

       export AICUSTOM_API_KEY="your-api-key"

2. Create and save an assistant::

       import os
       from aichatclient import AICustom

       assistant = AICustom(
           api_key=os.environ["AICUSTOM_API_KEY"],
           base_url="https://api.example.com/v1",
           model_name="provider/model-name",
           nickname="my_assistant",
           system_prompt="You are a helpful programming assistant.",
           memory=True,
       )
       assistant.create_model()      # saves the config; the API key is NOT saved

3. Chat::

       print(assistant.chat("Hello!"))
       print(assistant.chat("Short answer please.", short=True))

4. Load it later (key is read from ``AICUSTOM_API_KEY``)::

       assistant = AICustom.load_model("my_assistant")

5. Inspect or clear history::

       assistant.get_history(limit=20)
       assistant.clear_history()

6. Use the lightweight wrapper::

       from aichatclient import AiClient

       client = AiClient.load_model(name="my_assistant")
       client.chat("Hi!")

7. Launch the web interface::

       from aichatclient import AICustom, ChatApp

       ai = AICustom.load_model("my_assistant")
       ChatApp(ai=ai).run(host="127.0.0.1", port=5000, debug=False)

راهنمای سریع (فارسی)
--------------------
1. کلید را در متغیر محیطی ``AICUSTOM_API_KEY`` بگذار، نه داخل کد.
2. با ``AICustom(...)`` دستیار را بساز و با ``create_model()`` ذخیره کن
   (کلید API هرگز ذخیره نمی‌شود).
3. با ``chat("...")`` گفتگو کن؛ ``short=True`` پاسخ کوتاه می‌دهد.
4. بعداً با ``AICustom.load_model("my_assistant")`` بارگذاری کن.
5. با ``get_history()`` تاریخچه را ببین و با ``clear_history()`` پاک کن.
6. برای رابط وب: ``ChatApp(ai=ai).run(host="127.0.0.1", port=5000)``.

Notes
-----
* ``ChatApp`` (and therefore Flask) is imported lazily, only when first used,
  so ``import aichatclient`` stays fast and works in non-web environments.
* Storage root defaults to ``.ai_custom`` in the working directory; override
  with ``storage_dir=...`` or the ``AICUSTOM_HOME`` environment variable.
* Persona fields (``personality``, ``expertise``, ``limitations``) guide the
  model but do not replace validation or authorization in your application.

Full documentation: https://github.com/amirhossinpython/aichatclient
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # for IDEs and type checkers only; no runtime cost
    from .aiclient import AiClient
    from .aicustom import AICustom
    from .app import ChatApp

__version__ = "4.1.0"

__all__ = ["AICustom", "AiClient", "ChatApp", "__version__"]

# Public name -> submodule that defines it (resolved on first access).
_LAZY_IMPORTS = {
    "AICustom": ".aicustom",
    "AiClient": ".aiclient",
    "ChatApp": ".app",
}


def __getattr__(name: str) -> Any:
    """Import public classes lazily (PEP 562)."""
    module_path = _LAZY_IMPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module_path, __name__), name)
    globals()[name] = value  # cache so later lookups skip __getattr__
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))


