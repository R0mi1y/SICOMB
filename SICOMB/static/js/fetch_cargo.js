var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
var imageEquipment = document.getElementById("means_room_product");
var observation = document.getElementById("note_equipment");
var insert_bttn = document.getElementById("insert_btn");
var list_equipment = {}; // lista com os equipamentos a serem cadastrados em formato de dicionário
var equipmentData = null; // Equipamento atual só que de forma global, pra acessar depois, será setada depois
var id_overlay = 0;

// seta a data e a hora atual => {
var dataAtual = new Date();
var dia = dataAtual.getDate();
var mes = dataAtual.getMonth() + 1; // Lembrando que os meses começam em 0
var ano = dataAtual.getFullYear();

let diaFormatado = dia < 10 ? '0' + dia : dia;
let mesFormatado = mes < 10 ? '0' + mes : mes;

var time = dataAtual.getHours() + ':' + dataAtual.getMinutes();
var data = diaFormatado + '/' + mesFormatado + '/' + ano;

document.getElementById('date').innerText = data;
document.getElementById('time').innerText = time;
// => }


fetch("http://localhost:8000/cargo/list_equipment/get")
    .then(response => response.json())
    .then(data => {
        if (data !== {}) {
            console.log(data);
            list_equipment = data;
            for (let key in list_equipment) {
                insertLine(list_equipment[key]);
            }
        }
    });


// faz a requisição dos dados do equipamento atual de forma igual às api's
var fetchEquipmentData = () => {
    fetch('http://localhost:8000/equipment/get')
        .then(response => response.json())
        .then(data => {
            if (data.uid !== '') {
                for (let key in list_equipment) {
                    console.log(key);
                    if (key == data.equipment.serial_number) {
                        alert('Equipamento já na lista!');
                        return;
                    }
                }
                // Armazena os dados do equipamento em uma variável para uso posterior
                equipmentData = data;
                console.log(data);
                // Para de ficar requisitando
                clearInterval(interval);

                if (data.registred !== false) {
                    if (data.registred === 'wearable') {
                        equipmentData['campo'] = 'Vestível'; // variável auxiliar o equipmentData['campo']
                    } else if (data.registred === 'accessory') {
                        equipmentData['campo'] = 'Acessório';
                    } else if (data.registred === 'armament') {
                        equipmentData['campo'] = 'Armamento';
                    } else if (data.registred === 'grenada') {
                        equipmentData['campo'] = 'Granada';
                    }

                    imageEquipment.src = "/static/" + data.model.image_path; // Muda a imagem

                    // Seta o resto => {
                    if (data.equipment.serial_number != null) serialNumberInput.innerText = data.equipment.serial_number;
                    if (data.model.description != null) description.innerText = data.model.description;
                    observation.innerText = data.equipment.observation;
                    type.innerText = equipmentData.campo;
                    amount.innerText = '1';
                    // => }
                }
            }
            if (data.msm != null) {
                alert(data.msm);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}


// Cria um intervalo para chamar a função a cada 1 segundo
var interval = setInterval(fetchEquipmentData, 1000);
var table_itens = document.getElementById('body_table_itens'); // tabela de itens

// Insere na lista no clicar do botão de inserir
function insertLine(line) {
    table_itens.innerHTML += // Insere efetivamente na lista => {
        '<tr>' +
        '<td></td>' +
        '<td>' + line.equipment.serial_number + '</td>' +
        '<td>' + line.model.description + '</td>' +
        '<td>' + line.campo + '</td>' +
        '<td>' + (line.model.caliber == null ? "-" : line.model.caliber) + '</td>' +
        '<td>' + (line.equipment.amount == null ? "1" : line.equipment.observation) + '</td>' +
        '<td>' + (line.registred == 'wearable' ? line.model.size : "-") + '</td>' +
        '<td>' + line.equipment.observation + '</td>' +
        '<td></td>' +
        '</tr>'// => }
    // insere na lista de equipamentos efetiva, em formato de lista, o equipamento atual com o numero de série como chave
    updateRowNumbers(table_itens);
}


insert_bttn.addEventListener('click', () => {
    if (equipmentData != null) {
        equipmentData.equipment.observation = (observation.value != '' ? observation.value : "-");
        equipmentData.equipment['amount'] = amount.innerText;

        insertLine(equipmentData);

        list_equipment[equipmentData.equipment.serial_number] = { 'serial_number': equipmentData.equipment.serial_number, 'observation': observation.innerText };

        fetch("http://localhost:8000/cargo/list_equipment/add/" + equipmentData.equipment.serial_number + "/" + (observation.value != '' ? observation.value : "-") + "/", {
            method: 'POST',
        });

        equipmentData = null; // reseta os equipamentos atuais
        // Reseta o quadro do equipamento => {
        interval = setInterval(fetchEquipmentData, 1000);
        imageEquipment.src = "/static/img/default.png";
        serialNumberInput.innerText = '';
        description.innerText = '';
        observation.innerText = '';
        type.innerText = '';
        amount.innerText = '';
        // => }
    }
});


function checkRemoveRow(rowNumber) {
    alert("Passe de volta o equipamento", false);
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série
    obs = rows[rowNumber].getElementsByTagName("td")[7].innerHTML; // 7 É A POSIÇÃO DA OBSERVAÇÃO, ou seja ele pega a observação
    clearInterval(interval);

    interval = setInterval(() => {
        fetch('http://localhost:8000/equipment/get')
            .then(response => response.json())
            .then(data => {
                if (data.uid !== '') {
                    for (let key in list_equipment) {
                        console.log(key);
                        if (key === data.equipment.serial_number) {
                            if (key == serialNum) {
                                removeRow(rowNumber);
                                removerAlert();
                                clearInterval(interval);
                                fetch("http://localhost:8000/cargo/list_equipment/remove/" + serialNum + "/" + (obs != '' ? obs : "-") + "/", {
                                    method: 'POST',
                                });
                                interval = setInterval(fetchEquipmentData, 1000);
                                return;
                            } else {
                                alert("Equipamento incorreto!");
                                return;
                            }
                        }
                    }
                    if (data.msm != null) {
                        alert(data.msm);
                    } else {
                        alert("O equipamento não está na lista!");
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao buscar dados do equipamento:', error);
            });
    }, 1000);
}


// Remove a linha da tabela
function removeRow(rowNumber) {
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série
    delete list_equipment[serialNum]; // deleta o equipamento da lista efetica da carga

    table_itens.deleteRow(rowNumber);
    updateRowNumbers();
}


// Básicamente checa o numero que foi retirado e renumera as linha de acordo
function updateRowNumbers() {
    var rows = table_itens.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        cells[0].innerHTML = i + 1; // primeira coluna, a do numero de série da tabela
        cells[cells.length - 1].innerHTML = '<a href="#" onclick="checkRemoveRow(' + i + ')">| X |</a>'; // ultima coluna, o botão de remover
    }
}


function alert(message, close_btn) {
    close_btn = close_btn ?? true;
    if (close_btn) {
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
    } else {
        var overlayHTML = `
        <div id="overlay` + id_overlay + `" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;">
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #fff; padding: 20px;padding-top: 20px; border-radius: 5px; z-index: 10000;">
                <p style="margin: 0;">` + message + `</p>
                <textarea id="note_equipment_devolute" name="note" rows="3" cols="60">
                </textarea>
                </div>
        </div>
            `;
    }
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

function confirmCargo() {
    var rows = table_itens.getElementsByTagName("tr");
    if (rows.length > 0) window.location.href = './confirm';
    else alert("Lista vazia!");
}
