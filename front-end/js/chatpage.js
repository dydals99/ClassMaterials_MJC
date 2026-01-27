const urlParams = new URLSearchParams(window.location.search);
const botId = urlParams.get('id');
const chatWrapper = document.getElementById('chat-wrapper');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const messagesContainer = document.getElementById('messages-container');

const MESSAGE_LIMIT = 10; // 화면에 표시될 최대 메시지 수
let isFirstMessage = true;

/**
 * 1. 초기화 함수: 챗봇 정보 및 이전 대화 내역 로드
 */
async function init() {
    if (!botId) return;

    try {
        // 챗봇 기본 정보 로드
        const botRes = await fetch('/api/chatbots/');
        const bots = await botRes.json();
        const bot = bots.find(b => b.id == botId);
        if (bot) {
            document.getElementById('display-name').innerText = bot.name;
            document.getElementById('display-desc').innerText = bot.description;
        }

        // 이전 대화 내역 로드 (ChatHistoryResponse 리스트 가정)
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

/**
 * 2. 메시지 전송 함수
 */
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

/**
 * 3. 메시지 화면 표시 (10개 제한 및 타임스탬프 포함)
 */
function appendMessage(role, text, timestamp) {
    // 메시지 개수 제한 로직: 10개 이상이면 가장 첫 번째(가장 오래된) 노드 삭제
    while (chatMessages.children.length >= MESSAGE_LIMIT) {
        chatMessages.removeChild(chatMessages.firstChild);
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // 메시지 내용 영역
    const contentDiv = document.createElement('div');
    contentDiv.className = "content";
    if (role === 'bot' && window.marked) {
        contentDiv.innerHTML = marked.parse(text);
    } else {
        contentDiv.innerText = text;
    }

    // 타임스탬프 영역
    const timeSpan = document.createElement('span');
    timeSpan.className = "timestamp";
    timeSpan.innerText = timestamp;

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeSpan);
    chatMessages.appendChild(messageDiv);
    
    // 자동 스크롤
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
}

/**
 * 시간 포맷 헬퍼 (예: 오후 2:30)
 */
function formatTimestamp(date) {
    return date.toLocaleTimeString('ko-KR', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// 이벤트 연결
init();
document.getElementById('send-trigger').onclick = sendMessage;
userInput.onkeypress = (e) => { 
    if(e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
};