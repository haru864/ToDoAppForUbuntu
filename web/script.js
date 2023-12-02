class TaskInfo {
    constructor(id, task_name, task_type, difficulty_level, is_completed, estimated_time_seconds, remaining_time_seconds, total_elapsed_time_seconds) {
        this.id = id;
        this.task_name = task_name;
        this.task_type = task_type;
        this.difficulty_level = difficulty_level;
        this.is_completed = is_completed;
        this.estimated_time_seconds = estimated_time_seconds;
        this.remaining_time_seconds = remaining_time_seconds;
        this.total_elapsed_time_seconds = total_elapsed_time_seconds;
    }
}

var timers = {};
listRegisteredTask();

document.getElementById('select_sound').addEventListener('click', function () {
    eel.selectSound();
});

document.getElementById('add_task').addEventListener('click', function () {
    var task_name = document.getElementById('task_name').value;
    var task_type = document.getElementById('task_type').value;
    var difficulty_level = document.getElementById('difficulty_level').value;
    var task_time = document.getElementById('task_time').value;
    if (task_name === '' || task_type === '' || difficulty_level === '' || task_time === '') {
        alert('未入力の項目があります。')
        return;
    }
    if (task_time <= 0) {
        alert('タスクの時間は1分以上で設定してください。')
        return;
    }
    let id = eel.registerTask(task_name, task_type, difficulty_level, 0, task_time, task_time, 0);
    listRegisteredTask();
});

async function listRegisteredTask() {
    let list = document.getElementById('task_list');
    let task_list = await eel.getRegisteredTask()();
    let records = JSON.parse(task_list);
    for (let record of records) {
        let task_info = new TaskInfo(
            record["id"],
            record["task_name"],
            record["task_type"],
            record["difficulty_level"],
            record["is_completed"],
            record["estimated_time_seconds"],
            record["remaining_time_seconds"],
            record["total_elapsed_time_seconds"]
        );
        if (document.getElementById(`${task_info.id}`)) {
            continue;
        }
        let elem = document.createElement('li');
        elem.innerHTML = `${task_info.task_name}(${task_info.task_type},${task_info.difficulty_level}) - 残り時間: <span id='${task_info.id}'>${formatTime(task_info.remaining_time_seconds)}</span> <button onclick="toggleTimer(this, '${task_info.id}', ${task_info.remaining_time_seconds})">スタート</button> <button onclick="completeTask(this, '${task_info.id}')">完了</button> <button onclick="deleteTask(this, '${task_info.id}')">削除</button> `;
        list.appendChild(elem);
    }
}

function formatTime(minutes) {
    let h = Math.floor(minutes / 60);
    let m = Math.floor(minutes % 60);
    let s = Math.floor((minutes - Math.floor(minutes)) * 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function completeTask(task_id) {
    return;
}

function toggleTimer(btn, task_id, time) {
    if (timers[task_id]) {
        clearInterval(timers[task_id].interval);
        // delete timers[task_id];
        btn.innerText = 'スタート';
    } else {
        timers[task_id] = {
            remaining: time * 60, interval: setInterval(function () {
                updateTimer(task_id);
            }, 1000)
        };
        btn.innerText = '停止';
    }
}

function updateTimer(task_id) {
    var timer = timers[task_id];
    if (--timer.remaining <= 0) {
        clearInterval(timer.interval);
        eel.startSound();
        alert(task_id + 'の終了時間です！');
        eel.stopSound();
    } else {
        document.getElementById(task_id).innerText = formatTime(timer.remaining / 60);
    }
}

function deleteTask(btn, task_id) {
    var li = btn.parentNode;
    if (timers[task_id]) {
        clearInterval(timers[task_id].interval);
        delete timers[task_id];
    }
    li.parentNode.removeChild(li);
}
