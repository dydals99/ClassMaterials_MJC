const urlParams = new URLSearchParams(window.location.search);
const botId = urlParams.get('id');
const chatWrapper = document.getElementById('chat-wrapper');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages-container');

const MESSAGE_LIMIT = 10; 
let isFirstMessage = true;


async function init() {
    if (!botId) return;

    try {
        const botRes = await fetch('/api/chatbots/');
        const bots = await botRes.json();
        const bot = bots.find(b => b.id == botId);
        if (bot) {
            document.getElementById('display-name').innerText = bot.name;
            document.getElementById('display-desc').innerText = bot.description;
        }

        const historyRes = await fetch(`/api/chat/history/${botId}`);
        const history = await historyRes.json();

        if (history && history.length > 0) {
            chatWrapper.classList.add('active');
            isFirstMessage = false;

            // 최근 10개만 슬라이싱하여 표시
            const recentHistory = history.slice(-MESSAGE_LIMIT);
            recentHistory.forEach(msg => {
                // DB 저장 시간 또는 현재 시간으로 타임스탬프 생성
                const time = msg.created_at ? formatTimestamp(new Date(msg.created_at)) : formatTimestamp(new Date());
                appendMessage(msg.role, msg.content, time);
            });
        }
    } catch (e) {
        console.error("초기화 중 오류 발생:", e);
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    if (isFirstMessage) {
        chatWrapper.classList.add('active');
        isFirstMessage = false;
    }

    const currentTime = formatTimestamp(new Date());
    appendMessage('user', text, currentTime);
    userInput.value = '';

    try {
        const res = await fetch('/api/chat/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chatbot_id: botId, message: text })
        });

        const data = await res.json();
        const responseTime = formatTimestamp(new Date());
        appendMessage('bot', data.response, responseTime);
    } catch (e) {
        appendMessage('bot', "오류가 발생했습니다.", formatTimestamp(new Date()));
    }
}


function appendMessage(role, text, timestamp) {
    while (chatMessages.children.length >= MESSAGE_LIMIT) {
        chatMessages.removeChild(chatMessages.firstChild);
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = "content";
    if (role === 'bot' && window.marked) {
        contentDiv.innerHTML = marked.parse(text);
    } else {
        contentDiv.innerText = text;
    }

    const timeSpan = document.createElement('span');
    timeSpan.className = "timestamp";
    timeSpan.innerText = timestamp;

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeSpan);
    chatMessages.appendChild(messageDiv);
    
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
}


function formatTimestamp(date) {
    return date.toLocaleTimeString('ko-KR', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

init();
document.getElementById('send-trigger').onclick = sendMessage;
userInput.onkeypress = (e) => { 
    if(e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
};