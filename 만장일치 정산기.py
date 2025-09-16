<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>만장일치 뒷풀이 정산기</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans KR', sans-serif;
        }
        .card {
            background-color: white;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease-in-out;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }
        .btn-primary {
            background-color: #4f46e5;
            color: white;
        }
        .btn-primary:hover {
            background-color: #4338ca;
        }
        .btn-secondary {
            background-color: #e5e7eb;
            color: #374151;
        }
        .btn-secondary:hover {
            background-color: #d1d5db;
        }
        .btn-danger {
            background-color: #ef4444;
            color: white;
        }
         .btn-danger:hover {
            background-color: #dc2626;
        }
        .input-field {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            border: 1px solid #d1d5db;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .input-field:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 2px #c7d2fe;
        }
        .participant-tag {
            display: inline-flex;
            align-items: center;
            background-color: #e0e7ff;
            color: #4338ca;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }
        .result-table th, .result-table td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">

    <div class="container mx-auto p-4 md:p-8 max-w-4xl">
        <header class="text-center mb-8">
            <div class="flex justify-center items-center gap-4">
                <img src="logo.jpg" alt="만장일치 로고" class="h-16 w-auto">
                <h1 class="text-4xl font-bold text-gray-900">만장일치 뒷풀이 정산기</h1>
            </div>
            <p class="text-lg text-gray-600 mt-2">복잡한 회식비 계산, 이제는 간편하게 해결하세요!</p>
        </header>

        <!-- 1. 참가자 관리 -->
        <section id="participant-section" class="card">
            <h2 class="text-2xl font-semibold mb-4 border-b pb-2">1. 참가자 관리</h2>
            <div class="flex flex-col sm:flex-row gap-2 mb-4">
                <input type="text" id="participant-name" placeholder="참가자 이름 입력 (예: 홍길동)" class="input-field flex-grow">
                <button id="add-participant-btn" class="btn btn-primary">추가</button>
            </div>
            <div id="participant-list" class="flex flex-wrap gap-2">
            </div>
        </section>

        <!-- 2. 차수별 비용 입력 -->
        <section id="rounds-section" class="card">
            <div class="flex justify-between items-center mb-4 border-b pb-2">
                <h2 class="text-2xl font-semibold">2. 차수별 비용 입력</h2>
                <button id="add-round-btn" class="btn btn-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" /></svg>
                    차수 추가
                </button>
            </div>
            <div id="round-list" class="space-y-6">
            </div>
        </section>

        <!-- 3. 정산하기 -->
        <section class="text-center my-8">
            <button id="calculate-btn" class="btn btn-primary text-lg px-8 py-3 transform hover:scale-105">정산하기</button>
        </section>

        <!-- 4. 정산 결과 -->
        <section id="result-section" class="card hidden">
            <div class="flex justify-between items-center mb-4 border-b pb-2">
                <h2 class="text-2xl font-semibold">4. 최종 정산 결과</h2>
                <button id="copy-result-btn" class="btn btn-secondary">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM5 11a1 1 0 100 2h4a1 1 0 100-2H5z" /></svg>
                    결과 복사
                </button>
            </div>
            <div id="result-output"></div>
            <div id="copy-feedback" class="text-green-600 font-semibold mt-2 text-center hidden">결과가 클립보드에 복사되었습니다!</div>
        </section>

    </div>

    <script>
        // --- 상태 관리 (State Management) ---
        let participants = [];
        let rounds = [];

        // --- DOM 요소 참조 ---
        const participantNameInput = document.getElementById('participant-name');
        const addParticipantBtn = document.getElementById('add-participant-btn');
        const participantListDiv = document.getElementById('participant-list');
        const addRoundBtn = document.getElementById('add-round-btn');
        const roundListDiv = document.getElementById('round-list');
        const calculateBtn = document.getElementById('calculate-btn');
        const resultSection = document.getElementById('result-section');
        const resultOutputDiv = document.getElementById('result-output');
        const copyResultBtn = document.getElementById('copy-result-btn');

        // --- 렌더링 함수 (Rendering Functions) ---

        function renderParticipants() {
            participantListDiv.innerHTML = '';
            participants.forEach((name, index) => {
                const tag = document.createElement('div');
                tag.className = 'participant-tag';
                tag.innerHTML = `
                    <span>${name}</span>
                    <button data-index="${index}" class="remove-participant-btn ml-2 text-red-500 hover:text-red-700">&times;</button>
                `;
                participantListDiv.appendChild(tag);
            });
            renderRounds();
        }

        function renderRounds() {
            roundListDiv.innerHTML = '';
            rounds.forEach((round, index) => {
                const roundCard = document.createElement('div');
                roundCard.className = 'p-4 border rounded-lg bg-gray-50';
                roundCard.innerHTML = `
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="text-lg font-semibold">${index + 1}차 정산</h3>
                        <button data-index="${index}" class="remove-round-btn btn btn-danger btn-sm text-xs p-1 px-2">삭제</button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                        <input type="text" value="${round.description}" data-index="${index}" class="round-description input-field" placeholder="장소/내용 (예: 닭갈비집)">
                        <input type="number" value="${round.totalCost || ''}" data-index="${index}" class="round-total-cost input-field" placeholder="총액 (원)">
                        <input type="number" value="${round.alcoholCost || ''}" data-index="${index}" class="round-alcohol-cost input-field" placeholder="그 중 술값 (원)">
                    </div>
                    <p class="font-medium text-sm text-gray-700 mb-2">참가자 선택:</p>
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                        ${participants.map(name => `
                            <label class="flex items-center space-x-2 text-sm">
                                <input type="checkbox" data-round-index="${index}" data-name="${name}" class="attendee-checkbox" ${round.attendees.includes(name) ? 'checked' : ''}>
                                <span>${name}</span>
                                <input type="checkbox" data-round-index="${index}" data-name="${name}" class="drinker-checkbox" ${round.drinkers.includes(name) ? 'checked' : ''} ${!round.attendees.includes(name) ? 'disabled' : ''}>
                                <span class="text-xs text-blue-600">(주)</span>
                            </label>
                        `).join('')}
                    </div>
                `;
                roundListDiv.appendChild(roundCard);
            });
        }
        
        function renderResults(results) {
            resultOutputDiv.innerHTML = '';
            
            let individualResultsHtml = '<h3 class="text-xl font-semibold mb-2">👤 개인별 정산 금액</h3><div class="overflow-x-auto"><table class="w-full text-sm result-table"><thead><tr><th class="w-1/3">이름</th><th class="w-1/3">총 금액</th><th class="w-1/3">상세 내역</th></tr></thead><tbody>';
            for (const name in results.individual) {
                const person = results.individual[name];
                individualResultsHtml += `
                    <tr>
                        <td class="font-semibold">${name}</td>
                        <td class="font-semibold text-indigo-600">${Math.round(person.total).toLocaleString()}원</td>
                        <td>${person.breakdown}</td>
                    </tr>
                `;
            }
            individualResultsHtml += '</tbody></table></div>';
            
            let roundSummaryHtml = '<h3 class="text-xl font-semibold mt-6 mb-2">📊 차수별 요약</h3><div class="space-y-2">';
            results.roundSummary.forEach(summary => {
                 roundSummaryHtml += `<div class="p-3 bg-gray-100 rounded-md text-sm">${summary}</div>`
            });
            roundSummaryHtml += '</div>';

            resultOutputDiv.innerHTML = individualResultsHtml + roundSummaryHtml;
            resultSection.classList.remove('hidden');
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }

        function handleAddParticipant() {
            const name = participantNameInput.value.trim();
            if (name && !participants.includes(name)) {
                participants.push(name);
                participantNameInput.value = '';
                renderParticipants();
            } else if (participants.includes(name)) {
                alert('이미 추가된 이름입니다.');
            }
             participantNameInput.focus();
        }
        
        addParticipantBtn.addEventListener('click', handleAddParticipant);
        participantNameInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') handleAddParticipant();
        });

        participantListDiv.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-participant-btn')) {
                const index = e.target.dataset.index;
                const nameToRemove = participants[index];
                participants.splice(index, 1);
                
                rounds.forEach(round => {
                    round.attendees = round.attendees.filter(p => p !== nameToRemove);
                    round.drinkers = round.drinkers.filter(p => p !== nameToRemove);
                });
                
                renderParticipants();
            }
        });

        addRoundBtn.addEventListener('click', () => {
            rounds.push({
                description: '',
                totalCost: 0,
                alcoholCost: 0,
                attendees: [],
                drinkers: []
            });
            renderRounds();
        });

        roundListDiv.addEventListener('input', (e) => {
            const index = e.target.dataset.index || e.target.dataset.roundIndex;
            if (index === undefined) return;
            
            if (e.target.classList.contains('round-description')) {
                rounds[index].description = e.target.value;
            } else if (e.target.classList.contains('round-total-cost')) {
                rounds[index].totalCost = parseFloat(e.target.value) || 0;
            } else if (e.target.classList.contains('round-alcohol-cost')) {
                rounds[index].alcoholCost = parseFloat(e.target.value) || 0;
            }
        });
        
        roundListDiv.addEventListener('change', (e) => {
            if (e.target.type !== 'checkbox') return;
            const roundIndex = e.target.dataset.roundIndex;
            const name = e.target.dataset.name;

            if (e.target.classList.contains('attendee-checkbox')) {
                const drinkerCheckbox = document.querySelector(`.drinker-checkbox[data-round-index="${roundIndex}"][data-name="${name}"]`);
                if (e.target.checked) {
                    rounds[roundIndex].attendees.push(name);
                    drinkerCheckbox.disabled = false;
                } else {
                    rounds[roundIndex].attendees = rounds[roundIndex].attendees.filter(p => p !== name);
                    rounds[roundIndex].drinkers = rounds[roundIndex].drinkers.filter(p => p !== name);
                    drinkerCheckbox.checked = false;
                    drinkerCheckbox.disabled = true;
                }
            } else if (e.target.classList.contains('drinker-checkbox')) {
                if (e.target.checked) {
                    rounds[roundIndex].drinkers.push(name);
                } else {
                    rounds[roundIndex].drinkers = rounds[roundIndex].drinkers.filter(p => p !== name);
                }
            }
        });
        
        roundListDiv.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-round-btn')) {
                const index = e.target.dataset.index;
                rounds.splice(index, 1);
                renderRounds();
            }
        });
        
        calculateBtn.addEventListener('click', () => {
            if (participants.length === 0) {
                alert('참가자를 1명 이상 추가해주세요.'); return;
            }
            if (rounds.length === 0) {
                alert('정산할 차수를 1개 이상 추가해주세요.'); return;
            }
            for(const [i, round] of rounds.entries()) {
                if(!round.totalCost || round.totalCost <= 0) {
                    alert(`${i+1}차의 총액을 올바르게 입력해주세요.`); return;
                }
                if(round.attendees.length === 0) {
                    alert(`${i+1}차의 참가자를 선택해주세요.`); return;
                }
                 if(round.alcoholCost > round.totalCost) {
                    alert(`${i+1}차의 술값이 총액보다 클 수 없습니다.`); return;
                }
                 if(round.alcoholCost > 0 && round.drinkers.length === 0) {
                    alert(`${i+1}차에 술값이 있는데 술 마신 사람이 없습니다. 음주자를 선택해주세요.`); return;
                }
            }

            const individualTotals = {};
            participants.forEach(name => {
                individualTotals[name] = { total: 0, breakdown: [] };
            });

            const roundSummary = [];

            rounds.forEach((round, index) => {
                const foodCost = round.totalCost - round.alcoholCost;
                const alcoholCost = round.alcoholCost;
                
                const foodPerPerson = round.attendees.length > 0 ? foodCost / round.attendees.length : 0;
                const alcoholPerDrinker = round.drinkers.length > 0 ? alcoholCost / round.drinkers.length : 0;
                
                roundSummary.push(
                    `[${index + 1}차: ${round.description || '내용 없음'}] 총액: ${round.totalCost.toLocaleString()}원, 참가자 ${round.attendees.length}명, 음주자 ${round.drinkers.length}명`
                );
                
                round.attendees.forEach(name => {
                    let costForRound = foodPerPerson;
                    if (round.drinkers.includes(name)) {
                        costForRound += alcoholPerDrinker;
                    }
                    individualTotals[name].total += costForRound;
                    if(!individualTotals[name].breakdown.includes(`${index + 1}차`)){
                       individualTotals[name].breakdown.push(`${index + 1}차`);
                    }
                });
            });

            for (const name in individualTotals) {
                 individualTotals[name].breakdown = individualTotals[name].breakdown.join(', ');
            }
            
            renderResults({ individual: individualTotals, roundSummary });
       });
        
        copyResultBtn.addEventListener('click', () => {
            let textToCopy = "--- 최종 정산 결과 ---\n\n";
            const results = resultOutputDiv.querySelectorAll('.result-table tbody tr');
            
            textToCopy += "👤 개인별 정산 금액\n"
            results.forEach(row => {
                const name = row.cells[0].innerText;
                const total = row.cells[1].innerText;
                textToCopy += `${name}: ${total}\n`;
            });
            
            textToCopy += "\n📊 차수별 요약\n";
            resultOutputDiv.querySelectorAll('.space-y-2 > div').forEach(summaryDiv => {
                textToCopy += summaryDiv.innerText + "\n";
            });

            navigator.clipboard.writeText(textToCopy).then(() => {
                const feedback = document.getElementById('copy-feedback');
                feedback.classList.remove('hidden');
                setTimeout(() => feedback.classList.add('hidden'), 2000);
            }).catch(err => {
                alert('결과 복사에 실패했습니다.');
            });
        });
        
        renderParticipants();

    </script>
</body>
</html>
