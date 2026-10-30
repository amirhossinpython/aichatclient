document.addEventListener('DOMContentLoaded', function () {
    const messagesDiv = document.getElementById('messages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const clearBtn = document.getElementById('clearChat');

    const STORAGE_KEY = 'chat_messages';

    // بررسی وجود عناصر ضروری صفحه
    if (!messagesDiv || !userInput || !sendBtn || !clearBtn) {
        console.error('خطا: عناصر موردنیاز چت در HTML پیدا نشدند.');
        return;
    }

    // بازیابی پیام‌های قبلی مرورگر
    loadMessages();

    // ارسال پیام با Shift + Enter
    userInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // تنظیم خودکار ارتفاع کادر پیام
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // رویداد دکمه‌ها
    sendBtn.addEventListener('click', sendMessage);
    clearBtn.addEventListener('click', clearChat);

    // خواندن پیام‌ها از localStorage
    function loadMessages() {
        const saved = localStorage.getItem(STORAGE_KEY);

        if (!saved) return;

        try {
            const messages = JSON.parse(saved);

            if (!Array.isArray(messages)) return;

            messagesDiv.innerHTML = '';

            messages.forEach(function (msg) {
                if (
                    msg &&
                    typeof msg.text === 'string' &&
                    (msg.type === 'user' || msg.type === 'bot')
                ) {
                    addMessageToUI(msg.text, msg.type);
                }
            });

            scrollToBottom();
        } catch (error) {
            console.error('خطا در بازیابی پیام‌ها:', error);
        }
    }

    // ذخیره پیام‌ها در localStorage
    function saveMessages() {
        const messages = [];

        messagesDiv.querySelectorAll('.message').forEach(function (msg) {
            // پیام موقت تایپ ذخیره نشود
            if (msg.id === 'typing-indicator') return;

            const textElement = msg.querySelector('.text');
            if (!textElement) return;

            const type = msg.classList.contains('user') ? 'user' : 'bot';

            messages.push({
                type: type,
                text: textElement.textContent
            });
        });

        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
        } catch (error) {
            console.error('خطا در ذخیره پیام‌ها:', error);
        }
    }

    // ارسال پیام به سرور Flask و دریافت پاسخ مدل
    async function sendMessage() {
        const message = userInput.value.trim();

        if (!message || sendBtn.disabled) return;

        sendBtn.disabled = true;

        addMessageToUI(message, 'user');

        userInput.value = '';
        userInput.style.height = 'auto';

        saveMessages();

        // نمایش نشانگر انتظار
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'message bot';

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = '🤖';

        const content = document.createElement('div');
        content.className = 'content';

        const name = document.createElement('div');
        name.className = 'name';
        name.textContent = 'دستیار هوشمند';

        const text = document.createElement('div');
        text.className = 'text';
        text.textContent = 'در حال دریافت پاسخ...';

        content.appendChild(name);
        content.appendChild(text);

        typingDiv.appendChild(avatar);
        typingDiv.appendChild(content);

        messagesDiv.appendChild(typingDiv);
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || 'دریافت پاسخ از سرور ناموفق بود.'
                );
            }

            if (typeof data.response !== 'string') {
                throw new Error('پاسخ سرور معتبر نیست.');
            }

            addMessageToUI(data.response, 'bot');
            saveMessages();

        } catch (error) {
            console.error('خطا در ارسال پیام:', error);

            addMessageToUI(
                'خطا: ' + (error.message || 'ارتباط با سرور برقرار نشد.'),
                'bot'
            );

            saveMessages();

        } finally {
            // حذف نشانگر انتظار در تمام حالت‌ها
            const indicator = document.getElementById('typing-indicator');

            if (indicator) {
                indicator.remove();
            }

            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    // افزودن پیام به رابط کاربری
    function addMessageToUI(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + type;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = type === 'user' ? '👤' : '🤖';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';

        const nameDiv = document.createElement('div');
        nameDiv.className = 'name';
        nameDiv.textContent = type === 'user' ? 'شما' : 'دستیار هوشمند';

        const textDiv = document.createElement('div');
        textDiv.className = 'text';

        // نمایش امن متن، بدون اجرای HTML دریافتی
        textDiv.textContent = String(text);

        contentDiv.appendChild(nameDiv);
        contentDiv.appendChild(textDiv);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);

        messagesDiv.appendChild(messageDiv);
        scrollToBottom();
    }

    // پاک کردن پیام‌های نمایشی و حافظه محلی مرورگر
    function clearChat() {
        const confirmed = confirm(
            'پیام‌های نمایش‌داده‌شده پاک شوند؟ تاریخچه ذخیره‌شده مدل حذف نمی‌شود.'
        );

        if (!confirmed) return;

        messagesDiv.innerHTML = '';

        addMessageToUI(
            'چت پاک شد. چطور می‌توانم کمک کنم؟',
            'bot'
        );

        localStorage.removeItem(STORAGE_KEY);
        saveMessages();
    }

    // رفتن به انتهای فهرست پیام‌ها
    function scrollToBottom() {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
