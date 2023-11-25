var timers = {};

document.getElementById('addTask').addEventListener('click', function () {
    var taskName = document.getElementById('taskName').value;
    var taskTime = document.getElementById('taskTime').value;
    if (isRegisteredTask(taskName) === true) {
        alert('すでに登録されているタスクは追加できません。')
        return;
    }
    if (isValidTime(taskTime) === false) {
        alert('タスクの時間は1分以上で設定してください。')
        return;
    }
    addTask(taskName, taskTime);
});

function addTask(name, time) {
    var list = document.getElementById('taskList');
    var task = document.createElement('li');
    task.innerHTML = `${name} - 残り時間: <span id='time-${name}'>${formatTime(time)}</span> <button onclick="toggleTimer(this, '${name}', ${time})">スタート</button> <button onclick="deleteTask(this, '${name}')">削除</button>`;
    list.appendChild(task);
}

function isRegisteredTask(name) {
    if (document.getElementById(`time-${name}`)) {
        return true;
    }
    return false;
}

function isValidTime(time) {
    if (time <= 0) {
        return false;
    }
    return true;
}

function formatTime(minutes) {
    var h = Math.floor(minutes / 60);
    var m = Math.floor(minutes % 60);
    var s = Math.floor((minutes - Math.floor(minutes)) * 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function toggleTimer(btn, name, time) {
    if (timers[name]) {
        clearInterval(timers[name].interval);
        // delete timers[name];
        btn.innerText = 'スタート';
    } else {
        timers[name] = {
            remaining: time * 60, interval: setInterval(function () {
                updateTimer(name);
            }, 1000)
        };
        btn.innerText = '停止';
    }
}

function updateTimer(taskName) {
    var timer = timers[taskName];
    if (--timer.remaining <= 0) {
        clearInterval(timer.interval);
        eel.startSound();
        alert(taskName + 'の終了時間です！');
        eel.stopSound();
    } else {
        document.getElementById('time-' + taskName).innerText = formatTime(timer.remaining / 60);
    }
}

function deleteTask(btn, taskName) {
    var li = btn.parentNode;
    if (timers[taskName]) {
        clearInterval(timers[taskName].interval);
        delete timers[taskName];
    }
    li.parentNode.removeChild(li);
}
