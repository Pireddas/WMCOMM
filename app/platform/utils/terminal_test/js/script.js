async function carregar() {
  try {
    const response = await fetch('http://127.0.0.1:8001/view/screen-update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'vibe_6706c7e5b610b6a0887590a782db0583'
      },
      body: JSON.stringify({})
    });

    const data = await response.json();
    document.getElementById('screen').innerHTML = '<p></p>' + data.screen;

  } catch (erro) {
    document.getElementById('screen').textContent = "Erro ao carregar.";
    console.error(erro);
  }
}

const COLS = 84;

function pad80(text) {
  return text.padEnd(COLS, " ");
}

function renderMenu() {

  const linha1 = pad80("<br><span style='color: #00ff00;'>............................. MAINFRAME ENGINE CONTROL .............................</span>");
  const linha2 = pad80("");
  const linha3 = pad80(" 1 - CONNECT");
  const linha4 = pad80(" 2 - LOGON");
  const linha5 = pad80(" 3 - LOGOFF(BACK)");
  const linha6 = pad80(" 4 - DISCONNECT");
  const linha7 = pad80("<span style='font-size:18px; color: #00ff00; align: left; background: #000000;'>Command ===>   </span><input type='text' size=30>                                ");

  const html =
    linha1 + "\n" +
    linha2 + "\n" +
    wrapMenuItem(linha3, "connect") + "\n" +
    wrapMenuItem(linha4, "logon") + "\n" +
    wrapMenuItem(linha5, "logoff") + "\n" +
    wrapMenuItem(linha6, "disconnect") + "\n\n" +
    MenuItemPre(linha7) + "\n";

  document.getElementById("menu").innerHTML = html;
}

function wrapMenuItem(line, action) {
  return `<span class="menu-item" onclick="handleAction('${action}')">${line}</span>`;
}

function MenuItem(line) {
  return `<span class="menu-item">${line}</span>`;
}

function MenuItemPre(line) {
  return `${line}`;
}

const API_KEY = "vibe_6706c7e5b610b6a0887590a782db0583";
const BASE_URL = "http://127.0.0.1:8001";

async function handleAction(action) {

  let url = "";
  let body = null;

  const hostValue = document.getElementById("host").value.trim();
  const portValue = document.getElementById("port").value.trim();

  if (action === "connect") {
    url = "/engine/connect";
    body = {
      host: `${hostValue}:${portValue}`,
      model: "3279-2-E"
    };
  }

  const userValue = document.getElementById("user").value.trim();
  const pwdValue = document.getElementById("pwd").value.trim();
  if (action === "logon") {
    url = "/engine/logon";
    body = {
      user_id: `${userValue}`,
      password: `${pwdValue}`
    };
  }

  if (action === "logoff") {
    url = "/engine/logoff";
  }

  if (action === "disconnect") {
    url = "/engine/disconnect";
  }

  try {
    const response = await fetch(BASE_URL + url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
      },
      body: body ? JSON.stringify(body) : null
    });

    if (!response.ok) {
      throw new Error("Erro HTTP: " + response.status);
    }

    let data = null;

    if (response.headers.get("content-type")?.includes("application/json")) {
      data = await response.json();
    }

    if (data?.screen) {
      document.getElementById("screen").innerHTML = data.screen;
    } else {
      await carregar();
    }

  } catch (err) {
    alert("Erro ao enviar comando");
    console.error(err);
  }
}

renderMenu();
