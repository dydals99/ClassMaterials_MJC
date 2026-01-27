document.addEventListener('DOMContentLoaded', async () => {
    const listContainer = document.getElementById('chatbot-list');

    try {
        const response = await fetch('/api/chatbots/');
        const chatbots = await response.json();

        listContainer.innerHTML = chatbots.map(bot => `
            <div class="bot-card">
                <div class="card-left" onclick="location.href='/studio?id=${bot.id}'">
                    <div class="icon-circle gray-bg">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <div class="card-text">
                        <h3 class="title">${bot.name}</h3>
                        <p class="desc">${bot.description || '설명 없음'}</p>
                    </div>
                </div>
                <div class="card-right">
                    <button class="chat-btn" onclick="location.href='/chat?id=${bot.id}'">
                        <i class="fa-regular fa-comments"></i> 채팅하기
                    </button>
                    <button class="more-btn" onclick="deleteBot(${bot.id})"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error("목록 로드 실패:", err);
    }
});

async function deleteBot(id) {
    if(confirm("이 챗봇을 삭제하시겠습니까?")) {
        await fetch(`/api/chatbots/${id}`, { method: 'DELETE' });
        location.reload();
    }
}