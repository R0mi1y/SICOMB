var list_equipment = [];

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

function selectCargo(id) {

    fetch("/static/html/cargo.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("means_room_content").innerHTML = data;
            set_date();

            fetch('http://localhost:8000/carga/get/' + id + '/')
                .then(response => response.json())
                .then(data_cargo => {
                    for (cargo in data_cargo.equipment_loads) {
                        console.log(data_cargo.equipment_loads[cargo]['Equipment&model']);
                        insertLine(data_cargo.equipment_loads[cargo]['Equipment&model'], false);
                        list_equipment.push(data_cargo.equipment_loads[cargo]['Equipment&model']);
                    }
                });
        })
}



interval = setInterval(() => { // começa a requisitar mas mudando as verificações
    fetch('http://localhost:8000/equipamento/get_indisponivel') // requisita o equipamento
        .then(response => response.json())
        .then(data => {
            if (data.uid !== '') {
                // percorre procurando o equipamento correspondente na tabela
                for (let i in list_equipment) {
                    if (list_equipment[i]['equipment']['serial_number'] === data.equipment.serial_number) { // verifica se tá na lista
                        return;
                    } // a partir daqui é se o equipamento não é o certo
                }
                // exibe a msm q veio do django (se houver)
            }
            if ('msm' in data) {
                popUp(data.msm);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}, 1000);



function fetchEquipmentData (serial_number) {
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
        // Armazena os dados do equipamento em uma variável para uso posterior
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();
        // Para de ficar requisitando
        clearInterval(interval);
        // variável auxiliar, o equipmentData['campo'] vai ter o nome em português
        addToSquare(data);
        // => }
        if (semaphore) {
            semaphore = false;
        }
    }
}

// var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
// serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série
// obs = rows[rowNumber].getElementsByTagName("td")[7].innerHTML; // 7 É A POSIÇÃO DA OBSERVAÇÃO, ou seja ele pega a observação
// // clearInterval(interval); // Para de ficar requisitando