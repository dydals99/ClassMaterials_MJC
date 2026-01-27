document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    let botId = urlParams.get('id');

    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const fileListContainer = document.getElementById('file-list');
    const saveBtn = document.getElementById('save-config');
    const uploadBtn = document.querySelector('.upload-btn');

    const loadFileList = async (id) => {
        if (!id) return;
        try {
            const response = await fetch(`/api/studio/${id}/files`); 
            if (response.ok) {
                const files = await response.json();
                fileListContainer.innerHTML = files.length > 0 
                    ? files.map(f => `<span class="file-tag"><i class="fa-regular fa-file-lines"></i> ${f.file_name}</span>`).join('')
                    : "<small>학습된 문서가 없습니다.</small>";
            }
        } catch (err) { console.error("파일 목록 로드 실패:", err); }
    };

    if (botId) {
        fetch(`/api/chatbots/`).then(res => res.json()).then(bots => {
            const bot = bots.find(b => b.id == botId);
            if (bot) {
                document.getElementById('name').value = bot.name;
                document.getElementById('features').value = bot.description;
                document.getElementById('prompt').value = bot.prompt;
                document.querySelector('input[type=range]').value = bot.temperature;
                document.getElementById('temp-val').innerText = bot.temperature;
                loadFileList(botId); 
            }
        });
    }

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileStatus.innerText = `선택됨: ${file.name}`;
            fileStatus.style.color = "#1a73e8";
            uploadBtn.style.border = "1px solid #1a73e8";
        }
    });

    saveBtn.onclick = async () => {
        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('features').value.trim();
        const prompt = document.getElementById('prompt').value.trim();
        const hasFile = fileInput.files.length > 0;

        if (!name || !description || !prompt) return alert("필수 항목을 입력해주세요.");
        if (!hasFile && !botId && !confirm("문서 없이 생성할까요?")) return;

        saveBtn.disabled = true;
        saveBtn.innerText = "처리 중...";

        try {
            const configData = {
                name, description, prompt,
                temperature: parseFloat(document.querySelector('input[type=range]').value),
                top_p: 1.0
            };

            const url = botId ? `/api/studio/${botId}/settings` : '/api/studio/';
            const method = botId ? 'PUT' : 'POST';

            const res = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(configData)
            });

            if (!res.ok) throw new Error("설정 저장 실패");
            
            const result = await res.json();
            const currentBotId = botId || result.id;

            if (hasFile) {
                fileStatus.innerText = "학습 중...";
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                const uploadRes = await fetch(`/api/studio/${currentBotId}/learn`, {
                    method: 'POST',
                    body: formData
                });
                if (!uploadRes.ok) throw new Error("문서 학습 실패");
            }

            alert("성공적으로 저장 및 학습되었습니다.");
            location.href = `/studio?id=${currentBotId}`;

        } catch (err) {
            alert("에러: " + err.message);
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerText = "저장";
        }
    };
});