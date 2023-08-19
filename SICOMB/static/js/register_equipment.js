var choicesTypes = document.getElementById("type-choices");
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
    for (let i = 0; i < choices.length; i++) {
        choices[i].disabled = true; // Desabilitar o elemento durante o processamento
        choices[i].style.display = 'none'; // Desabilitar o elemento durante o processamento
        choices[i].value = '';
    }

    if (selectedValue != '') { // se tiver selecionado algo
        choiceModels.style.display = 'block'; // revela o select certo
        choiceModels.disabled = false; // Habilita o select pra poder mudar
    }
}

// change_field(); // executa uma vez inicial para caso recarregue com algo selecionado
choicesTypes.addEventListener('change', change_field); // executa toda vez q mudar o campo choicesTypes

// requisita e valida o uid pra cadastrar
var fetchUid = () => {
    fetch('http://localhost:8000/equipamento/valid_uid')
        .then(response => response.json())
        .then(data => {
            let input_uid = document.getElementById('input-uid'); // o input que fica escondido
            let text_uid = document.getElementById("text-uid"); // o paragrafo que diz qual o uid

            if (data.msm != null) { // se vier uma msm do django
                popUp(data.msm);
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

interval = setInterval(fetchUid, 1000);

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

    console.log(serial_num);

    if (serial_num == '') { // checa se tem um numero de série inserido
        popUp("Por favor insira o número de série.");
        return;
    }
    // requisita ao sjango se o numero se série é válido, se já tá cadastrado no caso
    async () => fetch("http://localhost:8000/equipamento/valid_serial_number/" + serial_num + '/')
        .then(response => response.json())
        .then((data) => {
            if (data.exists) { // checa se existe ou não um num de série igual já cadastrado
                popUp("Numero de série já cadastrado!");
                return;
            }
        });
    if (document.getElementById('input-uid').value == '') { // checa se tem uid setado
        popUp("Por favor passe uma tag no sensor.");
        return;
    }
    if (selectedIndex == 0) { // checa caso não tenha nenhum modelo selecionado
        popUp("Por favor selecione uma opção de modelo.");
        return;
    }
    if (selectedIndex == 1) { // se passou por tudo e tem apenas um modelo selecionado ele confirma a ação e da o submit
        document.getElementById('form-equipment').submit();
    }
});

function register_bullet() {
    fetch("http://localhost:8000/equipamento/bullets/get/")
        .then(response => response.json())
        .then(bullets => {
            var bullet_options = '';
            bullets ?? '';
                for (i in bullets) {
                    bullet_options += '\n<option value="' + bullets[i]['id'] + '">' + bullets[i]['description'] + '</option>';
                }

            var csrf = document.querySelector('input[type="hidden"][name="csrfmiddlewaretoken"]');
            var bullet_html =
            `
            <form method="post" action="." class="form-element" style="min-height:220px;min-whidth:300px;">
            <div style="background-color: rgb(91,73,57, 0.9); whidth: 100%; border-radius: 20px; text-align:center; color: #fff; padding:5px;">
            <h3>
            CADASTRAR MUNIÇÃO
            </h3>
            </div>
                <div class="input-div">
                ` + csrf.outerHTML + `
                <div class="input-box">
                    <h4 class="input-title">MUNIÇÕES</h4>
                    <div class="select">
                        <select name="bullet" class="select-field" id="dropdown_bullets" required>
                ` +
                    bullet_options
                + `
                        </select>
                    </div>
                </div>
                <div class="input-box">
                    <h4 class="input-title" for="input_amount">QUANTIDADE:</h4>
                    <input name="amount" class="input-data" type="number" id="input_amount" required>
                </div>
                <div class="finalize-registration" style="padding-bottom: 0px;">
                    <label><input type="submit" id="submit-btn" class="box-shadow-registration" value="Adicionar"></label>
                </div>
            </form>
            `;

            popUp("", true, false, bullet_html);
        });
}