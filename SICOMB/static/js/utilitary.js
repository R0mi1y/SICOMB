var id_overlay = 0;
var aux = {};

function popUp(message, close_btn, yn) {
    close_btn = close_btn ?? true;
    yn = yn ?? false;

    var overlayHTML = `
    <div id="overlay` + id_overlay + `" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;">
    <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #fff; padding: 20px;padding-top: 20px; border-radius: 5px; z-index: 10000;">
    `;
    if (close_btn) { // se quer q tenha botão de fechar
        overlayHTML += `
        <button onclick="removerpopUp()" style="position: absolute; top: -15px; right: 10px; background-color: red; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 50%; cursor: pointer;">
        x
        </button>`;
    }
    overlayHTML += '<p style="margin: 0;">' + message + "</p>"
    if (yn) { // se quer q tenha os botões de sim ou não
        overlayHTML += `
        <button onclick="answerY()" style="background-color: green; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-right: 10px;">
            Sim
        </button>
        <button onclick="answerN()" style="background-color: red; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 5px; cursor: pointer;">
            Não
        </button>
        `;

    }
    overlayHTML += "</div></div>";
    id_overlay++; // serve para contar e separar se tiver mais de um popUpa

    document.body.insertAdjacentHTML('beforeend', overlayHTML);
}

// remove o popUpa
function removerpopUp() {
    id_overlay--;
    const overlay = document.getElementById('overlay' + id_overlay);
    if (overlay) {
        overlay.remove();
    }
}

// checa se a lista tá vazia
function confirmCargo() {
    var rows = table_itens.getElementsByTagName("tr");
    if (rows.length > 0) window.location.href = './confirm'; // se tiver certo redireciona pra confirmar a carga
    else popUp("Lista vazia!");
}

function answerN() {
    eval(aux["funN"]);
    removerpopUp();
}

function answerY() {
    eval(aux["funY"]);
    removerpopUp();
}