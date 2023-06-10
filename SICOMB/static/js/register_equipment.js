var choicesTypes = document.getElementById("type-choices");
var fetchData;
var id_overlay = 0; // serve para contar e separar se tiver mais de um alerta
choicesTypes.value = ""; // zera por causa do form, se deixar sem ele vem direto no q foi 
// selecionado antes e ele tem q mudar pra aparecer o próximo

// ele libera o campo certo pois tem 4 campos escondidos por causa do form do django
function change_field() {
    let selectedValue = choicesTypes.value; // checa o tipo do equipamento (acessorio, armamento, granada ou vestível)
    let choiceModels = document.getElementById("type-choices-" + selectedValue); // seleciona o select certo de acordo com o tipo selecionado
    let choices = document.getElementsByClassName("type-choices-type"); // seleciona todos os 4 campos sem exeção
    let labelClass = document.getElementById("lable-type-input");

    if (labelClass) labelClass.remove(); // remove a lable pra por a outra

    // reseta todos os 4 campos
    for (let i = 0; i < 4; i++) {
        choices[i].disabled = true; // Desabilitar o elemento durante o processamento
        choices[i].style.display = 'none'; // Desabilitar o elemento durante o processamento
        choices[i].value = '';
    }

    // nova label
    var label = "<label id='lable-type-input' for='type-choices-" +
        selectedValue + "'>Modelo de " +
        choicesTypes.options[choicesTypes.selectedIndex].text + "</label>";

    if (selectedValue != '') { // se tiver selecionado algo
        choicesTypes.insertAdjacentHTML('afterend', label);

        choiceModels.style.display = 'block'; // revela o select certo
        choiceModels.disabled = false; // Habilita o select pra poder mudar
    }
}

change_field(); // executa uma vez inicial para caso recarregue com algo selecionado
choicesTypes.addEventListener('change', change_field); // executa toda vez q mudar o campo choicesTypes

// requisita e valida o uid pra cadastrar
var fetchUid = () => {
    fetch('http://localhost:8000/equipment/valid_uid')
        .then(response => response.json())
        .then(data => {
            let input_uid = document.getElementById('input-uid'); // o input que fica escondido
            let text_uid = document.getElementById("text-uid"); // o paragrafo que diz qual o uid

            if (data.msm != null) { // se vier uma msm do django
                alert(data.msm);
            }
            if (data.uid !== '') { // seta o uid
                input_uid.value = data.uid;
                text_uid.innerText = "UID : " + data.uid;

                clearInterval(interval); // para de ficar requisitando
            } else if (input_uid.value != '') { // para caso o input venha preenchido por causa do django
                text_uid.innerText = "UID : " + input_uid.value;
                clearInterval(interval);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}

let interval = setInterval(fetchUid, 1000);

// Cria um popup como um alerta
function alert(message) {
    var overlayHTML = `
    <div id="overlay` + id_overlay + `" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;">
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #fff; padding: 20px;padding-top: 20px; border-radius: 5px; z-index: 10000;">
            <button onclick="removerAlert()" style="position: absolute; top: -15px; right: 10px; background-color: red; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 50%; cursor: pointer;">
                x
            </button>
            <p style="margin: 0;">` + message + `</p>
        </div>
    </div>
        `;
    id_overlay++; // // serve para contar e separar se tiver mais de um alerta

    document.body.insertAdjacentHTML('beforeend', overlayHTML);
}

// remove o popup, o alerta
function removerAlert() {
    id_overlay--;
    const overlay = document.getElementById('overlay' + id_overlay);
    if (overlay) {
        overlay.remove();
    }
}

// Faz a função de limpar o uid setado
document.getElementById("clear-btn").addEventListener('click', () => {
    let input_uid = document.getElementById('input-uid');
    let text_uid = document.getElementById("text-uid");

    setInterval(fetchUid, 1000);

    input_uid.value = '';
    text_uid.innerText = "Passe a tag no sensor";
});

// Checa tudo antes de dar o submit
document.getElementById("submit-btn").addEventListener('click', () => {
    // checa se tem mais de uma escolha de modelo escolhida => { 
    let choices = document.getElementsByClassName("type-choices-type");
    let selectedIndex = 0;

    for (let i = 0; i < 4; i++) {
        if (choices[i].value != '') { 
            selectedIndex++;
        }
    }
    // => }
    serial_num = document.getElementById('serial-number-input').value; // numero de série do input

    // requisita ao sjango se o numero se série é válido, se já tá cadastrado no caso
    fetch("http://localhost:8000/equipment/valid_serial_number/" + serial_num + '/') 
        .then(response => response.json())
        .then((data) => {
            if (document.getElementById('input-uid').value == '') { // checa se tem uid setado
                alert("Por favor passe uma tag no sensor.");
                return;
            }
            if (serial_num == '') { // checa se tem um numero de série inserido
                alert("Por favor insira o número de série.");
                return;
            }
            if (data.exists) { // checa se existe ou não um num de série igual já cadastrado
                alert("Numero de série já cadastrado!");
                return;
            }
            if (selectedIndex == 0) { // checa caso não tenha nenhum modelo selecionado
                alert("Por favor selecione uma opção de modelo.");
                return;
            }
            if (selectedIndex == 1) { // se passou por tudo e tem apenas um modelo selecionado ele confirma a ação e da o submit
                document.getElementById('form-equipment').submit();
            }
        });
});