document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    let botId = urlParams.get('id');

    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const saveBtn = document.getElementById('save-config');
    const uploadBtn = document.querySelector('.upload-btn');

    console.log("Studio JS 로드 완료. 현재 BotID:", botId);

    // 1. 기존 데이터 로드
    if (botId) {
        fetch(`/api/chatbots/`).then(res => res.json()).then(bots => {
            const bot = bots.find(b => b.id == botId);
            if (bot) {
                document.getElementById('name').value = bot.name;
                document.getElementById('features').value = bot.description;
                document.getElementById('prompt').value = bot.prompt;
                document.querySelector('input[type=range]').value = bot.temperature;
                document.getElementById('temp-val').innerText = bot.temperature;
            }
        }).catch(err => console.error("데이터 로드 실패:", err));
    }

    // 2. 파일 선택 시 시각적 변화 부여
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            console.log("파일 선택됨:", file.name);
            fileStatus.innerText = `선택된 파일: ${file.name}`;
            fileStatus.style.color = "#007bff";
            fileStatus.style.fontWeight = "bold";
            uploadBtn.style.backgroundColor = "#e7f3ff"; // 버튼 색상 변경
            uploadBtn.style.border = "1px solid #007bff";
        }
    });

    // 3. 통합 저장 버튼 클릭
    saveBtn.onclick = async () => {
        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('features').value.trim();
        const prompt = document.getElementById('prompt').value.trim();
        const hasFile = fileInput.files.length > 0;

        // 필수값 체크
        if (!name || !description || !prompt) {
            alert("이름, 주요 특징, 프롬프트는 필수 항목입니다.");
            return;
        }

        // 문서 체크
        if (!hasFile && !botId) {
            if (!confirm("학습 문서를 선택하지 않았습니다. 이대로 생성할까요?")) return;
        }

        // 버튼 비활성화 (중복 클릭 방지)
        saveBtn.disabled = true;
        saveBtn.innerText = "처리 중...";
        console.log("저장 프로세스 시작...");

        try {
            // [A] 챗봇 설정 저장
            const configData = {
                name: name,
                description: description,
                prompt: prompt,
                temperature: parseFloat(document.querySelector('input[type=range]').value),
                top_p: 1.0
            };

            const configUrl = botId ? `/api/studio/${botId}/settings` : '/api/chatbots/';
            const configMethod = botId ? 'PUT' : 'POST';

            const configRes = await fetch(configUrl, {
                method: configMethod,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(configData)
            });

            if (!configRes.ok) throw new Error("설정 저장에 실패했습니다.");
            
            const result = await configRes.json();
            const currentBotId = botId || result.id; // 신규 생성 시 생성된 ID 사용
            console.log("설정 저장 완료. BotID:", currentBotId);

            // [B] 파일 업로드 (있을 때만)
            if (hasFile) {
                console.log("파일 업로드 시작...");
                fileStatus.innerText = "AI가 문서를 읽고 학습하는 중입니다 (약 10~30초 소요)...";
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                const uploadRes = await fetch(`/api/studio/${currentBotId}/learn`, {
                    method: 'POST',
                    body: formData
                });

                if (!uploadRes.ok) throw new Error("문서 학습 중 오류 발생");
                console.log("파일 업로드 및 임베딩 완료");
            }

            alert("성공적으로 저장 및 학습되었습니다!");
            
            // 페이지 이동 또는 갱신
            if (!botId) {
                location.href = `/studio?id=${currentBotId}`;
            } else {
                location.reload();
            }

        } catch (err) {
            console.error("오류 발생:", err);
            alert("처리 중 에러가 발생했습니다: " + err.message);
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerText = "저장 및 학습 시작";
        }
    };
});