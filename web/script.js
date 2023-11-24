document.getElementById('addTask').addEventListener('click', function () {
    var taskName = document.getElementById('taskName').value;
    var taskTime = document.getElementById('taskTime').value;
    addTask(taskName, taskTime);
});

function addTask(name, time) {
    var list = document.getElementById('taskList');
    var task = document.createElement('li');
    task.innerHTML = `${name} - 残り時間: <span id='time-${name}'>${formatTime(time)}</span> <button onclick="toggleTimer(this, '${name}', ${time})">スタート</button> <button onclick="deleteTask(this, '${name}')">削除</button>`;
    list.appendChild(task);
}

var timers = {};

function toggleTimer(btn, taskId, time) {
    if (timers[taskId]) {
        clearInterval(timers[taskId].interval);
        delete timers[taskId];
        btn.innerText = 'スタート';
    } else {
        timers[taskId] = {
            remaining: time * 60, interval: setInterval(function () {
                updateTimer(taskId);
            }, 1000)
        };
        btn.innerText = '停止';
    }
}

function updateTimer(taskId) {
    var timer = timers[taskId];
    if (--timer.remaining <= 0) {
        clearInterval(timer.interval);
        alert(taskId + 'の時間です！');
    } else {
        document.getElementById('time-' + taskId).innerText = formatTime(timer.remaining / 60);
    }
}

function formatTime(minutes) {
    var h = Math.floor(minutes / 60);
    var m = Math.floor(minutes % 60);
    var s = Math.floor((minutes - Math.floor(minutes)) * 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function deleteTask(btn, taskId) {
    var li = btn.parentNode;
    if (timers[taskId]) {
        clearInterval(timers[taskId].interval);
    }
    li.parentNode.removeChild(li);
}
