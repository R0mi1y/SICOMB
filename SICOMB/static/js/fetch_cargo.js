var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
var imageEquipment = document.getElementById("means_room_product");
var observation = document.getElementById("note_equipment");
var insert_bttn = document.getElementById("insert_btn");
var list_equipment = {}; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
//tem uma array de equipamentos igual no django para caso de refresh e essa se perca
var equipmentData = null; // Equipamento atual só que de forma global, pra acessar depois, será setada depois

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

// busca se já tem uma lista no sistema 
//(serve para caso a página de refresh, tá salvo no sistema desde q ele não rreinicie o sistema)
fetch("http://localhost:8000/cargo/list_equipment/get") // faz uma requisição da lista
    .then(response => response.json())
    .then(data => {
        if (data !== {}) {
            console.log(data);
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
                for (let key in list_equipment) {
                    console.log(key);
                    if (key == data.equipment.serial_number) {
                        popUp('Equipamento já na lista!');
                        return;
                    }
                }

                //se não tiver cadastrado
                if (data.registred !== false) {
                    // Armazena os dados do equipamento em uma variável para uso posterior
                    equipmentData = data;
                    // Para de ficar requisitando
                    clearInterval(interval);
                    // variável auxiliar, o equipmentData['campo'] vai ter o nome em português
                    equipmentData['campo'] = data.registred == 'wearable' ? 'Vestível' : equipmentData['campo'];
                    equipmentData['campo'] = data.registred == 'accessory' ? 'Acessório' : equipmentData['campo'];
                    equipmentData['campo'] = data.registred == 'armament' ? 'Armamento' : equipmentData['campo'];
                    equipmentData['campo'] = data.registred == 'grenada' ? 'Granada' : equipmentData['campo'];

                    imageEquipment.src = "/static/" + data.model.image_path; // Muda a imagem

                    // Seta o resto => {
                    if (data.equipment.serial_number != null) serialNumberInput.innerText = data.equipment.serial_number;
                    if (data.model.description != null) description.innerText = data.model.description;
                    observation.innerText = data.equipment.observation == null || data.equipment.observation == undefined ? "" : data.equipment.observation;
                    type.innerText = equipmentData.campo;
                    amount.innerText = '1';
                    // => }
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
        '<td>' + (line.equipment.serial_number == null ? "-" : line.equipment.serial_number) + '</td>' +
        '<td>' + (line.model.description == null ? "-" : line.model.description) + '</td>' +
        '<td>' + (line.campo == null ? "-" : line.campo) + '</td>' +
        '<td>' + (line.model.caliber == null ? "-" : line.model.caliber) + '</td>' +
        '<td>' + (line.equipment.amount == null ? "1" : line.equipment.amount) + '</td>' +
        '<td>' + (line.registred == 'wearable' ? line.model.size : "-") + '</td>' +
        '<td>' + (line.equipment.observation == null ? "-" : line.equipment.observation) + '</td>' +
        '<td></td>' +
        '</tr>' // => }

    // renumera e adiciona o botão de deletar
    updateRowNumbers(table_itens);
}

// Insere com o clicar do botão inserir
insert_bttn.addEventListener('click', () => {
    if (equipmentData != null) { // se tiver um equipamento no quadro
        equipmentData.equipment['amount'] = amount.innerText;

        insertLine(equipmentData); // insere a linha

        list_equipment[equipmentData.equipment.serial_number] = { // adiciona no array de equipamentos o numero de série e a observação
            'serial_number': equipmentData.equipment.serial_number,
            'observation': observation.innerText
        };

        // adiciona no array de equipamentos do django => {
        fetch("http://localhost:8000/cargo/list_equipment/add/" +
            equipmentData.equipment.serial_number + "/" +
            (observation.value != '' ? observation.value : null) + "/", {
                method: 'POST',
            });
        // => }

        equipmentData = null; // reseta os equipamentos atuais
        // Reseta o quadro do equipamento => {
        interval = setInterval(fetchEquipmentData, 1000);
        imageEquipment.src = "/static/img/default.png";
        serialNumberInput.innerText = '';
        description.innerText = '';
        observation.innerHTML = '';
        type.innerText = '';
        amount.innerText = '';
        // => }
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
                                fetch("http://localhost:8000/cargo/list_equipment/remove/" + serialNum + "/" + (obs != '' ? obs : null) + "/", {
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