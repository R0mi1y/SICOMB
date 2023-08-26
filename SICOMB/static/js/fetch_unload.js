var list_equipment = [];
var square_equipment;
var list_returned_equipment = [];
var id_cargo;

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
// => }

function set_carga_id(id) {
    id_cargo = id;

    var inputHidden = document.createElement('input');
    inputHidden.setAttribute('type', 'hidden');
    inputHidden.setAttribute('name', 'turn_type');
    inputHidden.setAttribute('value', 'descarga');
    document.getElementById('form-equipment').appendChild(inputHidden);

    inputHidden = document.createElement('input');
    inputHidden.setAttribute('type', 'hidden');
    inputHidden.setAttribute('name', 'load_id');
    inputHidden.setAttribute('value', id);
    document.getElementById('form-equipment').appendChild(inputHidden);

    document.getElementById('insert_btn').value = "DEVOLVER";

    fetch('http://localhost:8000/carga/get/' + id_cargo + '/')
        .then(response => response.json())
        .then(data_cargo => {
            for (cargo in data_cargo.equipment_loads) {
                insertLine(data_cargo.equipment_loads[cargo]['Equipment&model'], false);
                list_equipment.push(data_cargo.equipment_loads[cargo]['Equipment&model']);
            }
        });
}

interval = setInterval(fetchUnvalibleEquipmentData, 1000);

function fetchUnvalibleEquipmentData() { // começa a requisitar mas mudando as verificações
    fetch('http://localhost:8000/equipamento/get_indisponivel/' + id_cargo + '/') // requisita o equipamento
        .then(response => response.json())
        .then(data => {
            if (data.uid !== '') {
                console.log(data);
                // percorre procurando o equipamento correspondente na tabela
                for (let i in list_equipment) {
                    if (list_equipment[i]['equipment']['serial_number'] === data.equipment.serial_number) { // verifica se tá na lista
                        addToSquare(data);
                        square_equipment = data;
                        return;
                    } // a partir daqui é se o equipamento não é o certo
                }
            } // exibe a msm q veio do django (se houver)
            if ('msm' in data) {
                popUp(data.msm);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}



function fetchEquipmentData(serial_number) {
    let url = serial_number == null || serial_number == undefined ? 'http://localhost:8000/equipamento/get_disponivel' : 'http://localhost:8000/equipamento/get/' + serial_number;
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

function checkAwateList() {
    if (list_awate_equipment.length > 0) {
        equipmentData = list_awate_equipment[list_awate_equipment.length - 1];
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();

        clearInterval(interval);
        addToSquare(data);

        if (semaphore) {
            semaphore = false;
        }
    }
}

function check_cargo_square() {
    var observation = document.getElementById("note_equipment");
    var serialNumberInput = document.getElementById("serial_number");
    var table_itens = document.getElementById('body_table_itens');
    var amount_input = document.getElementById("amount_input");

    for (i in list_equipment) {
        for (i in table_itens.childNodes) {
            if (table_itens.childNodes[i].childNodes[1] && serialNumberInput.innerHTML == table_itens.childNodes[i].childNodes[1].innerHTML) {
                list_returned_equipment.push(square_equipment);

                table_itens.childNodes[i].childNodes[8].innerHTML = '| V |';
                table_itens.childNodes[i].childNodes[8].style.color = 'green';

                clearSquare();
                interval = setInterval(fetchUnvalibleEquipmentData, 1000);
                // adiciona no array de equipamentos do django => {
                // Montar a URL da solicitação
                const url = `http://localhost:8000/carga/lista_equipamentos/add/${square_equipment.equipment.serial_number}/${
                    observation.value !== '' ? observation.value : '-'
                }/${amount_input.value}/${user}/${pass.replace(/\//g, '%21%')}/`;

                square_equipment = null;

                console.log(url);
                // Fazer a solicitação Fetch
                fetch(url, {
                        method: 'POST', // Método HTTP POST para enviar dados
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Manipular os dados recebidos, por exemplo, mostrar um pop-up
                        // popUp(data["message"]);
                    })
                    .catch(error => {
                        // Lidar com erros de solicitação, se houver
                        console.error(error);
                    });
                return;
            }
        }
    }

}

// checa se a lista tá vazia
function confirmCargo() {
    console.log(list_returned_equipment);
    if (list_returned_equipment.length > 0) document.getElementById("form-equipment").submit(); // se tiver certo redireciona pra confirmar a carga
    else popUp("Lista vazia!");
}