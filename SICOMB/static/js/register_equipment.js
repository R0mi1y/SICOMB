var choicesTypes = document.getElementById("type-choices");
var fetchData;
var id_overlay = 0;
choicesTypes.value = "";

function change_field() {
    let selectedValue = choicesTypes.value;
    let choiceModels = document.getElementById("type-choices-" + selectedValue);
    let choices = document.getElementsByClassName("type-choices-type");
    let labelClass = document.getElementById("lable-type-input");

    if (labelClass) labelClass.remove();

    for (let i = 0; i < 4; i++) {
        choices[i].disabled = true; // Desabilitar o elemento durante o processamento
        choices[i].style.display = 'none'; // Desabilitar o elemento durante o processamento
        choices[i].value = '';
    }

    var label = "<label id='lable-type-input' for='type-choices-" + selectedValue + "'>Modelo de " + choicesTypes.options[choicesTypes.selectedIndex].text + "</label>";
    // Limpar as opções existentes e adicionar uma opção padrão
    if (selectedValue != '') {
        choicesTypes.insertAdjacentHTML('afterend', label);

        choiceModels.style.display = 'block'; // Desabilitar o elemento durante o processamento
        choiceModels.disabled = false; // Habilitar o elemento durante o processamento
    }
}

change_field();
choicesTypes.addEventListener('change', change_field);

var fetchUid = () => {
    fetch('http://localhost:8000/equipment/valid_uid')
        .then(response => response.json())
        .then(data => {
            let input_uid = document.getElementById('input-uid');
            let text_Uid = document.getElementById("text-uid");

            if (data.msm != null) {
                alert(data.msm);
            }
            if (data.uid !== '') {
                input_uid.value = data.uid;
                text_Uid.innerText = "UID : " + data.uid;

                clearInterval(interval);
            } else if (input_uid.value != '') {
                text_Uid.innerText = "UID : " + input_uid.value;
                clearInterval(interval);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}

let interval = setInterval(fetchUid, 1000);

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
    id_overlay++;

    document.body.insertAdjacentHTML('beforeend', overlayHTML);
}


function removerAlert() {
    id_overlay--;
    const overlay = document.getElementById('overlay' + id_overlay);
    if (overlay) {
        overlay.remove();
    }
}

document.getElementById("clear-btn").addEventListener('click', () => {
    let input_uid = document.getElementById('input-uid');
    let text_uid = document.getElementById("text-uid");

    setInterval(fetchUid, 1000);

    input_uid.value = '';
    text_uid.innerText = "Passe a tag no sensor";
});

document.getElementById("submit-btn").addEventListener('click', () => {
    let choices = document.getElementsByClassName("type-choices-type");
    let selectedIndex = 0;

    for (let i = 0; i < 4; i++) {
        if (choices[i].value != '') {
            selectedIndex++;
        }
    }
    serial_num = document.getElementById('serial-number-input').value;
    console.log(serial_num);

    fetch("http://localhost:8000/equipment/valid_serial_number/" + serial_num + '/')
        .then(response => response.json())
        .then((data) => {
            if (document.getElementById('input-uid').value == '') {
                alert("Por favor passe uma tag no sensor.");
                return;
            }
            if (data.exists) {
                alert("Numero de série já cadastrado!");
                return;
            }
            if (serial_num == '') {
                alert("Por favor insira o número de série.");
                return;
            }
            if (selectedIndex == 0) {
                alert("Por favor selecione uma opção de modelo.");
                return;
            }
            if (selectedIndex == 1) {
                document.getElementById('form-equipment').submit();
            }
        });
});

