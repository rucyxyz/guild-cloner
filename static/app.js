let guilds = [];
let ws = null;

async function login() {
  const token = document.getElementById("token").value.trim();
  if (!token) return alert("トークンを入力してください");

  const btn = document.getElementById("btn-login");
  btn.disabled = true;
  btn.textContent = "認証中...";

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });
    const data = await res.json();

    if (!data.ok) throw new Error(data.error);

    guilds = data.guilds;
    populateGuilds();

    document.getElementById("step2").style.display = "block";
    document.getElementById("step3").style.display = "block";
    document.getElementById("step4").style.display = "block";

    log(guilds.length + " 個のサーバーに接続しました");
  } catch (e) {
    alert("認証失敗: " + e.message);
    log("認証失敗: " + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "認証";
  }
}

function populateGuilds() {
  const src = document.getElementById("src-select");
  const dst = document.getElementById("dst-select");
  src.innerHTML = '<option value="">-- 選択 --</option>';
  dst.innerHTML = '<option value="">-- 選択 --</option>';

  guilds.forEach(function(g) {
    const label = g.name + " (" + g.id + ")";
    src.insertAdjacentHTML("beforeend", '<option value="' + g.id + '">' + label + '</option>');
    dst.insertAdjacentHTML("beforeend", '<option value="' + g.id + '">' + label + '</option>');
  });
}

async function startClone() {
  const token = document.getElementById("token").value.trim();
  const srcId = document.getElementById("src-select").value;
  const dstId = document.getElementById("dst-select").value;

  if (!srcId || !dstId) return alert("サーバーを選択してください");
  if (srcId === dstId) return alert("複製元と複製先が同じです");

  const options = {
    roles: document.getElementById("opt-roles").checked,
    categories: document.getElementById("opt-categories").checked,
    text_channels: document.getElementById("opt-text").checked,
    voice_channels: document.getElementById("opt-voice").checked,
    messages: document.getElementById("opt-messages").checked,
    message_limit: parseInt(document.getElementById("msg-limit").value) || 100,
  };

  connectWS();

  document.getElementById("btn-clone").disabled = true;
  document.getElementById("log").textContent = "";
  setProgress(0);

  try {
    const res = await fetch("/api/clone", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: token, src_id: srcId, dst_id: dstId, options: options }),
    });
    const data = await res.json();
    if (!data.ok) throw new Error(data.error);
    log("複製を開始しました...");
  } catch (e) {
    log("開始失敗: " + e.message);
    document.getElementById("btn-clone").disabled = false;
  }
}

function connectWS() {
  if (ws) ws.close();
  ws = new WebSocket("ws://" + location.host + "/ws");
  ws.onmessage = function(ev) {
    const data = JSON.parse(ev.data);
    log(data.message);
    setProgress(data.percent);

    if (data.percent >= 100) {
      document.getElementById("btn-clone").disabled = false;
    }
  };
  ws.onclose = function() { ws = null; };
}

function log(msg) {
  const el = document.getElementById("log");
  const time = new Date().toLocaleTimeString("ja-JP");
  el.textContent += "[" + time + "] " + msg + "\n";
  el.scrollTop = el.scrollHeight;
}

function setProgress(p) {
  document.getElementById("progress").style.width = p + "%";
  document.getElementById("percent").textContent = p + "%";
}
