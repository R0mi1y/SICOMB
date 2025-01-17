var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
// var observation = document.getElementById("note_equipment");
var insert_bttn = document.getElementById("insert_btn");
let amount_input = document.getElementById("amount_input");
var list_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var semaphore = true; 
var square = false; 
//tem uma array de equipamentos igual no django para caso de refresh e essa se perca
var equipmentData = null; // Equipamento atual só que de forma global, pra acessar depois, será setada depois

// seta a data e a hora atual => {
set_date();
// => }

// busca se já tem uma lista no sistema 
//(serve para caso a página de refresh, tá salvo no sistema desde q ele não rreinicie o sistema)
fetch("/carga/lista_equipamentos/get", {
    method: 'POST', // Método HTTP POST para enviar dados
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
        'user': user,
        'pass': pass,
    })}) // faz uma requisição da lista
    .then(response => response.json())
    .then(data => {
        list_equipment = data;
        for (let key in list_equipment) { // percorre a lista se existir
            console.log(list_equipment[key]);
            insertLine(list_equipment[key]); // insere cada objeto novamente na tabela
        }
    })
    .catch(error => {
        console.log("Erro de requisição: " + error);
        popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
    });

    
function fetchEquipmentData(serial_number, type='none') {
    // Caso a função receba o parâmetro serial_number, ela requisita o equipamento correspondente.
    // Caso contrário, ela requisita o equipamento passado no sensor.
    let url = (serial_number == null || serial_number == undefined ?
        '/equipamento/get_disponivel' :
        '/equipamento/get/' + serial_number);

    // Faz a requisição para a URL especificada
    fetch(url, {
            method: 'POST', // Método HTTP POST para enviar dados
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.uid !== '' && semaphore) {
                // Verifica se o equipamento já está na lista
                if (data.equipment.serial_number != null && data.equipment.serial_number != undefined) {
                    for (let key in list_equipment) {
                        if (key == data.equipment.serial_number) {
                            // popUp('Equipamento já na lista!');
                            return;
                        }
                    }
                }

                // Se o equipamento não estiver cadastrado, adiciona-o à lista de equipamentos em espera
                if (data.registred !== false) {
                    list_awate_equipment.push(data);
                    checkAwateList(type);
                }
            } else if (data.confirmCargo) {
                document.getElementById("submit_btn").disabled = false;
                document.getElementById("submit_btn").classList.remove("btn_disabled");
                document.getElementById("submit_btn").classList.add("btn_confirm");

                semaphore = false;
                clearInterval(interval);
            }

            // Se houver uma mensagem de erro na resposta, exibe-a
            if (data.msm != null) {
                popUp(data.msm);
            }
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}

// Cria um intervalo para chamar a função a cada 1 segundo
var interval = setInterval(fetchEquipmentData, 1000);

// Insere com o clicar do botão inserir
function check_cargo_square() {
    if (equipmentData != null) { // se tiver um equipamento no quadro
        equipmentData['amount'] = amount_input.value;
        
        let eq = equipmentData

        let serial_number = eq.equipment.serial_number ?? "bullet::" + eq.model.caliber;
        
        // adiciona no array de equipamentos do django => {
        fetch('/carga/lista_equipamentos/add/', {
            method: 'POST',
            headers: {
                'Content-Type': "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            'serialNumber': serial_number,
            // 'observation': observation.value ?? "-",
            'observation': "-",
            'amount': eq.amount,
            'user': user,
            'pass': pass
        }).toString()
        })
        .then(response => response.json())
        .then(data => {

            if(data.status == "error") {
                popUp(data.message);
                return;
            }

            list_equipment[eq.equipment.serial_number ?? 'ac' + eq.equipment.id] = { // adiciona no array de equipamentos o numero de série e a observação
                'serial_number': eq.equipment.serial_number,
                // 'observation': observation.innerText ?? "-",
                'observation': "-",
                'amount': amount_input.value,
                'model': {
                    'image_path': document.getElementById('means_room_product').src,
                }
            };

            insertLine(eq); // insere a linha
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
        // => }

        equipmentData = null; // reseta os equipamentos atuais
        // Reseta o quadro do equipamento => {
            
        clearSquare();
        clearInterval(interval);
        interval = setInterval(fetchEquipmentData, 1000);
        checkAwateList();
        // => }
    }
}

// Requisita passar o equipamento de novo no sensor pra remover
function checkRemoveRow(rowNumber) {
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    var col = rows[rowNumber].getElementsByTagName("td"); // pega os td da tr

    obs = col[7].innerHTML;
    amount = col[5].innerHTML;

    if (col[3].innerHTML != 'Munição') {
        serialNum = col[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série

        popUp("Tem certeza que deseja remover esse equipamento?", {yn: true, closeBtn: false, yesFunction: () => {
            fetch("/carga/lista_equipamentos/remover/", {
                method: 'POST', // Método HTTP POST para enviar dados
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'user': user,
                    'pass': pass,
                    'serial_number': serialNum,
                    'obs': obs
                })
            })
            .then(response => {
                removeRow(rowNumber); // remove a linha da tabela do html
            }).catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
        }});
    } else {
        caliber = col[4].innerHTML;
        popUp("Tem certeza que deseja remover esse equipamento?", {yn: true, closeBtn: false, yesFunction: () => {
            fetch("/carga/lista_equipamentos/remover/", {
                method: 'POST', // Método HTTP POST para enviar dados
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'user': user,
                    'pass': pass,
                    'serial_number': caliber,
                    'obs': obs
                })
            })
            .then(response => {
                removeRow(rowNumber); // remove a linha da tabela do html
            })
            .catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
        }});
    }
}


// Remove a linha da tabela
function removeRow(rowNumber) {
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série
    delete list_equipment[serialNum]; // deleta o equipamento da lista efetica da carga

    table_itens.deleteRow(rowNumber);
    updateRowNumbers();
}

function edit(i) {
    var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
    serialNum = rows[i].getElementsByTagName("td")[1].innerHTML;
    console.log(rows);
    addToSquare(list_equipment[serialNum]);
    removeRow(i);
}

// checa se a lista tá vazia
function confirmCargo() {
    var rows = table_itens.getElementsByTagName("tr");
    if (rows.length > 0) document.getElementById("form-equipment").submit(); // se tiver certo redireciona pra confirmar a carga
    else popUp("Lista vazia!");
}

function checkAwateList(type='none') {
    console.log(type);
    if (list_awate_equipment.length > 0) {
        equipmentData = list_awate_equipment[list_awate_equipment.length - 1];
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();
        // clearInterval(interval);
        addToSquare(data);
        
        if (type != "search") {
            check_cargo_square();
        }
    }
}

function searchWatingList() {
    fetch("/equipamento/lista_espera/get/", {
            method: 'POST', // Método HTTP POST para enviar dados
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass
            })
        })
        .then(response => response)
        .then(response => response.json())
        .then(data => {
            let wating_list = "";
            for (i in data) {
                wating_list += "<tr>" + data[i] + "</tr>";
            }
            document.getElementById("wating_list").innerHTML = wating_list;
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}
searchWatingList();
// var intervalWatingList = setInterval(searchWatingList, 1000);