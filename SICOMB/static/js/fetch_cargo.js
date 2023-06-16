var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
var observation = document.getElementById("note_equipment");
var insert_bttn = document.getElementById("insert_btn");
var list_equipment = {}; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var list_awate_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
let amount_input = document.getElementById("amount_input");
var semaphore = true;
//tem uma array de equipamentos igual no django para caso de refresh e essa se perca
var equipmentData = null; // Equipamento atual só que de forma global, pra acessar depois, será setada depois

// seta a data e a hora atual => {
function set_date() {
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
}
set_date()
// => }

// busca se já tem uma lista no sistema 
//(serve para caso a página de refresh, tá salvo no sistema desde q ele não rreinicie o sistema)
fetch("http://localhost:8000/cargo/list_equipment/get") // faz uma requisição da lista
    .then(response => response.json())
    .then(data => {
        if (data !== {}) {
            list_equipment = data;
            for (let key in list_equipment) { // percorre a lista se existir
                insertLine(list_equipment[key]); // insere cada objeto novamente na tabela
            }
        }
    });


// faz a requisição dos dados do equipamento atual de forma igual às api's
var fetchEquipmentData = (serial_number) => {
    let url = serial_number == null || serial_number == undefined ? 'http://localhost:8000/equipment/get' : 'http://localhost:8000/equipment/get/' + serial_number;
    fetch(url) // busca o equipamento do uid inserido
        .then(response => response.json())
        .then(data => {
            if (data.uid !== '') {
                // percorre a lista comparando o que já tem com o novo equipamento
                if (data.equipment.serial_number != null && data.equipment.serial_number != undefined) {
                    for (let key in list_equipment) {
                        if (key == data.equipment.serial_number) {
                            popUp('Equipamento já na lista!');
                            return;
                        }
                    }
                }

                //se não tiver cadastrado
                if (data.registred !== false) {
                    list_awate_equipment.push(data);

                    checkAwateList();
                }
            }
            if (data.msm != null) { // se tiver uma mensagem de erro na reguisição
                popUp(data.msm);

            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}


// Cria um intervalo para chamar a função a cada 1 segundo
var interval = setInterval(fetchEquipmentData, 1000);
var table_itens = document.getElementById('body_table_itens'); // tabela de itens do html

// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
function insertLine(line) {
    table_itens.innerHTML += // Insere efetivamente na lista => {
        '<tr>' +
        '<td></td>' +
        '<td>' + (line.equipment.serial_number == null || line.equipment.serial_number == undefined ? "-" : line.equipment.serial_number) + '</td>' +
        '<td>' + (line.model.description == null || line.model.description == undefined ? "-" : line.model.description) + '</td>' +
        '<td>' + (line.campo == null || line.campo == undefined ? "-" : line.campo) + '</td>' +
        '<td>' + (line.model.caliber == null || line.model.caliber == undefined ? "-" : line.model.caliber) + '</td>' +
        '<td>' + (line.amount == null || line.amount == undefined || line.amount == '' ? "1" : line.amount) + '</td>' +
        '<td>' + (line.registred == 'wearable' ? line.model.size : "-") + '</td>' +
        '<td>' + (line.equipment.observation == null || line.equipment.observation == undefined ? "-" : line.equipment.observation) + '</td>' +
        '<td></td>' +
        '</tr>' // => }

    // renumera e adiciona o botão de deletar
    updateRowNumbers(table_itens);
}

// Insere com o clicar do botão inserir
insert_bttn.addEventListener('click', () => {
    if (equipmentData != null) { // se tiver um equipamento no quadro
        equipmentData['amount'] = amount_input.value;

        insertLine(equipmentData); // insere a linha

        list_equipment[equipmentData.equipment.serial_number] = { // adiciona no array de equipamentos o numero de série e a observação
            'serial_number': equipmentData.equipment.serial_number,
            'observation': observation.innerText,
            'amount': amount_input.value
        };

        equipmentData.equipment.serial_number = equipmentData.equipment.serial_number ?? equipmentData.model.caliber;

        // adiciona no array de equipamentos do django => {
        fetch("http://localhost:8000/cargo/list_equipment/add/" +
            equipmentData.equipment.serial_number + "/" +
            (observation.value != '' ? observation.value : '-') + "/" + equipmentData.amount + "/", {
                method: 'POST',
            });
        // => }

        equipmentData = null; // reseta os equipamentos atuais
        // Reseta o quadro do equipamento => {
        interval = setInterval(fetchEquipmentData, 1000);

        document.getElementById("means_room_product").src = "/static/img/default.png";
        serialNumberInput.innerText = '';
        description.innerText = '';
        observation.innerHTML = '';
        type.innerText = '';
        amount.innerText = '';
        amount_input.value = '1';
        amount_input.disabled = true;

        checkAwateList();
        // => }
        semaphore = true;
    }
});

// Requisita passar o equipamento de novo no sensor pra remover
function checkRemoveRow(rowNumber) {
    popUp("Passe de volta o equipamento", false); // o false tira o botão de excluir a notificação
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série
    obs = rows[rowNumber].getElementsByTagName("td")[7].innerHTML; // 7 É A POSIÇÃO DA OBSERVAÇÃO, ou seja ele pega a observação
    clearInterval(interval); // Para de ficar requisitando

    interval = setInterval(() => { // começa a requisitar mas mudando as verificações
        fetch('http://localhost:8000/equipment/get') // requisita o equipamento
            .then(response => response.json())
            .then(data => {
                if (data.uid !== '') {
                    // percorre procurando o equipamento correspondente na tabela
                    for (let key in list_equipment) {
                        if (key === data.equipment.serial_number) { // verifica se tá na lista
                            if (key == serialNum) { // verifica se é o certo pois ele pode passar um q tá na lista mas é outro
                                removeRow(rowNumber); // remove a linha da tabela do html
                                removerpopUp(); // remove o popUpa
                                clearInterval(interval); // Para de ficar requisitando
                                // remove da lista do django
                                console.log(list_equipment);

                                fetch("http://localhost:8000/cargo/list_equipment/remove/" + serialNum + "/" + (obs != '' ? obs : null) + "/" + list_equipment[key]['amount'] ?? "1" + '/', {
                                    method: 'POST',
                                });
                                interval = setInterval(fetchEquipmentData, 1000); // volta a ficar requisitando pra cadastrar outros
                                return;
                            } else {
                                popUp("Equipamento incorreto!");
                                return;
                            }
                        }
                    } // a partir daqui é se o equipamento não é o certo
                    // exibe a msm q veio do django
                    if (data.msm != null) {
                        popUp(data.msm);
                    } else {
                        popUp("O equipamento não está na lista!");
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


// Básicamente checa o numero que foi retirado e renumera as linha de acordo e coloca o botão de excluir linha
function updateRowNumbers() {
    var rows = table_itens.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        cells[0].innerHTML = i + 1; // primeira coluna, a do numero de série da tabela
        cells[cells.length - 1].innerHTML = '<a href="#" onclick="checkRemoveRow(' + i + ')">| X |</a>'; // ultima coluna, o botão de remover
    }
}

document.getElementById("search-btn").addEventListener("click", () => {
    let search = document.getElementById("search-camp");
    fetchEquipmentData(search.value);
    search.value = '';
});

// checa se a lista tá vazia
function confirmCargo() {
    var rows = table_itens.getElementsByTagName("tr");
    if (rows.length > 0) window.location.href = '.'; // se tiver certo redireciona pra confirmar a carga
    else popUp("Lista vazia!");
}

function checkAwateList() {
    if (list_awate_equipment.length > 0) {
        equipmentData = list_awate_equipment[list_awate_equipment.length - 1];
        // Armazena os dados do equipamento em uma variável para uso posterior
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();
        // Para de ficar requisitando
        clearInterval(interval);
        // variável auxiliar, o equipmentData['campo'] vai ter o nome em português
        data['campo'] = data.registred == 'wearable' ? 'Vestmento' : data['campo'];
        data['campo'] = data.registred == 'accessory' ? 'Acessório' : data['campo'];
        data['campo'] = data.registred == 'armament' ? 'Armamento' : data['campo'];
        data['campo'] = data.registred == 'grenada' ? 'Granada' : data['campo'];
        data['campo'] = data.registred == 'bullet' ? 'Munição' : data['campo'];

        console.log(document.getElementById("means_room_product"));
        document.getElementById("means_room_product").src = "/static/" + data.model.image_path; // Muda a imagem

        if (!data.equipment.serial_number) {
            document.getElementById("amount_input").disabled = false;
        }

        // Seta o resto => {
        data.model.description = data.model.description ?? "-";
        serialNumberInput.innerText = data.equipment.serial_number ?? "-";
        description.innerText = data.model.description;
        observation.innerText = data.equipment.observation == null || data.equipment.observation == undefined ? "" : data.equipment.observation;
        type.innerText = data.campo;
        amount.innerText = data.amount == null || data.amount == undefined || data.amount == '' ? "1" : data.amount;
        amount_input.value = amount.innerText;
        // => }
        if (semaphore) {
            semaphore = false;
        }
    }
}
function searchWatingList() {
    fetch("http://localhost:8000/equipment/wating_list/get/").then(response => response)
        .then(response => response.json())
        .then(data => {
            let wating_list = "";
            for (i in data) {
                wating_list += "<tr>" + data[i] + "</tr>";
            }
            document.getElementById("wating_list").innerHTML = wating_list;
        });
}
var intervalWatingList = setInterval(searchWatingList, 1000);
