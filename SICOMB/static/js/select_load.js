
// var insert_btn = document.getElementById("insert_btn");
var table_itens = document.getElementById('body_table_itens'); // tabela de itens do html
var plate; // variável auxiliar para armazenar a matrícula para requisitar do django
var list_awate_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var list_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var turn_type;
var square_on;
var obs_seted = false;
var interval_get_login;
var stop_fetching_police = false;

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
    document.getElementById('turn_type').innerText = turn_type;

    document.getElementById("cancel_btn").disabled = false;
    document.getElementById("cancel_btn").classList.remove("btn_disabled");
    document.getElementById("cancel_btn").classList.add("btn_cancel");
}

// responsável por mudar a tabela da sala de meios de acordo com a requisição
function changeTemplate(template) {
    if (template == "loads_police") {
        document.getElementById("means_room_content").innerHTML = '';
        fetch("/carga/get/cargas_policial/" + plate + "/", {
            method: 'POST', // Método HTTP POST para enviar dados
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass,
            })})
            .then(response => response.json())
            .then(data => {
                turn_type = "Descarga";

                var table_element = document.createElement('table');
                table_element.className = 'table_itens';

                var tabel = `
                <thead>
                    <tr>
                        <th colspan="100%" class="cargo_title"><h3>TABELA DE CARGAS<h3></th>
                    </tr>
                    <tr class="col-itens">
                        <th>ID DE CARGA</th>
                        <th>TIPO</th>
                        <th>QNT. DE ITENS</th>
                        <th>DATA</th>
                        <th>PREVISÃO DE DESCARGA</th>
                        <th>STATUS</th>
                    </tr>
                    
                </thead>
                <tbody>
                    <tr>
                        <td colspan="100%">Escolha qual carga deseja descarregar</td>
                     </tr>
                    `;
                for (i in data.loads_police) {
                    tabel +=
                    `<tr class="tr_cargos row-tbody" onclick="selectCargo(` + data.loads_police[i].id + `)">
                        <td>` + 
                            data.loads_police[i].id
                        + `</td> 
                        <td>` + 
                            data.loads_police[i].turn_type
                        + `</td> 
                        <td>` + 
                            data.loads_police[i].itens_amount
                        + `</td> 
                        <td>` + 
                            data.loads_police[i].date_load.replace(/(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2}):\d{2}/, '$1/$2 - $4:$5')
                        + `</td> 
                        <td>` + 
                            (data.loads_police[i].expected_load_return_date ?? "-").replace(/(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2}):\d{2}/, '$1/$2 - $4:$5')
                        + `</td>
                        <td>` +
                            data.loads_police[i].status
                        + `</td>
                    </tr>`;
                }
                
                tabel += '</tbody>';
                table_element.innerHTML = tabel;

                var unload_div = document.createElement('div');
                unload_div.className = 'unload_itens';
                unload_div.appendChild(table_element);

                // Adicione o elemento cargo_div onde desejar
                document.getElementById("means_room_content").appendChild(unload_div);
            })
            .catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
    } else {
        fetch("/static/html/" + template + ".html")
            .then(response => response.text())
            .then(data => {
                document.getElementById("means_room_content").innerHTML = data;
            })
            .catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
        if (template == "load") {
            setTimeout(() => {
                var script = document.createElement('script');
                script.src = '/static/js/fetch_load.js';
                script.id = 'fetch_load.js';
                document.head.appendChild(script);

                $(document).ready(function() {
                    $("#search-btn").on("click", () => {
                        let search = $("#search-camp");
                        fetchEquipmentData(search.val(), "search");
                        search.value = '';
                    });
                    $(".search-bullet").on("click", (e) => {
                        fetchEquipmentData("bullet::" + e.target.value, "search");
                    });
                });
            }, 500)
        } 
    }
}


function selectCargo(id) {
    fetch("/static/html/load.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("means_room_content").innerHTML = data;
            set_date();
            
            var script = document.createElement('script');
            script.src = '/static/js/fetch_unload.js';
            script.id = 'fetch_load.js';
            document.head.appendChild(script);
            
            setTimeout(() => {
                set_carga_id(id);
            }, 500);
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}


// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
function insertLine(line, x) {
    x = x ?? true;

    table_itens.innerHTML += // Insere efetivamente na lista => {
        '<tr>' +
        '<td></td>' +
        '<td>' + (line.equipment.serial_number == null || line.equipment.serial_number == undefined ? "-" : line.equipment.serial_number) + '</td>' +
        '<td>' + (line.model.model == null || line.model.model == undefined ? "-" : line.model.model) + '</td>' +
        '<td>' + (line.campo == null || line.campo == undefined ? "-" : line.campo) + '</td>' +
        '<td>' + (line.model.caliber == null || line.model.caliber == undefined ? "-" : line.model.caliber) + '</td>' +
        '<td>' + (line.amount == null || line.amount == undefined || line.amount == '' ? "1" : line.amount) + '</td>' +
        '<td>' + (line.registred == 'wearable' ? line.model.size : "-") + '</td>' +
        '<td>' + ((line.observation && line.observation.length > 15) ? line.observation.slice(0, 15) + "..." : (line.observation || "-")) + '</td>' +
        '<td></td>' +
        '</tr>' // => }

    // renumera e adiciona o botão de deletar
    updateRowNumbers(x);
}

// Básicamente checa o numero que foi retirado e renumera as linha de acordo e coloca o botão de excluir linha
function updateRowNumbers(x) {
    x = x ?? true;
    var rows = table_itens.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        cells[0].innerHTML = i + 1; // primeira coluna, a do numero de série da tabela
        if(x){
            cells[cells.length - 1].innerHTML = '<a onclick="checkRemoveRow(' + i + ')"><svg fill="red" height="24" viewBox="0 -960 960 960" width="24"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg></a>'; // ultima coluna, o botão de remover
        } else if (cells[cells.length - 1].innerHTML != "<svg fill=\"green\" height=\"24\" viewBox=\"0 -960 960 960\" width=\"24\"><path d=\"M382-240 154-468l57-57 171 171 367-367 57 57-424 424Z\"></path></svg>"){
            if (cells[1].innerHTML == '-') {
                var key = "bullet::" + cells[4].innerHTML;
            } else {
                var key = cells[1].innerHTML;
            }

            cells[cells.length - 1].innerHTML = '<a id="edit" onclick="addObs(' + i + ', \'' + key +'\')"><svg fill="brown" height="24" viewBox="0 -960 960 960" width="24"><path d="M200-200h56l345-345-56-56-345 345v56Zm572-403L602-771l56-56q23-23 56.5-23t56.5 23l56 56q23 23 24 55.5T829-660l-57 57Zm-58 59L290-120H120v-170l424-424 170 170Zm-141-29-28-28 56 56-28-28Z"/></svg></a>'; // ultima coluna, o botão de remover
        }
    }
}

function setObservation(serial_number, row, observation) {
    $.ajax({
        url: "/carga/lista_equipamentos/add/observation/",
        type: "POST",
        dataType: "json",
        data: {
            serialNumber: serial_number,
            observation: observation,
            id_cargo: id_cargo,
            user: user,
            pass: pass,
        },
        success: function (data) {
            row[7].innerHTML = observation.slice(0, 15) + (observation.length > 15 ? "..." : "");
            row[8].innerHTML += (!row[8].innerHTML.includes("|") ? "| " + done_svg : "");

            for (var i = 0; i < list_equipment.length; i++) {
                console.log(i);
                console.log(list_equipment[i]);
                if (list_equipment[i].equipment.serial_number == serial_number) {
                    list_equipment[i].observation = observation;
                    console.log("Obs: " + list_equipment[i].observation);
                }
            }

            popUp("Observação adicionada com sucesso!", {timer: 2000, overlay: false});
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

function addObs(i, id_cargo) {
    var rows = table_itens.getElementsByTagName("tr");
    let row = rows[i].getElementsByTagName("td");
    window.obs_seted = true;

    popUp("Adicione a observação: ", {
        textArea: true,
        function_textarea: setObservation,
        parm1: id_cargo,
        parm2: row,
        contentTextarea: (list_equipment[i] && list_equipment[i].observation) ?? ""
    });
}

function setTurnType() {
    var radioSelecionado = document.querySelector('input[name="options_load"]:checked');

    if (radioSelecionado && radioSelecionado.value) {
        var inputElement = document.createElement("input");
        inputElement.type = "hidden";
        inputElement.name = "turn_type";
        inputElement.value = radioSelecionado.value;
        document.getElementById("form-equipment").appendChild(inputElement);

        turn_type = radioSelecionado.value;
        changeTemplate("load");
    } else {
        popUp("Selecione uma das opções!");
    }
}

function fetch_police(){
    if (stop_fetching_police) return;

    let url = '/police/get_login/';
    fetch(url, {
        method: 'POST', // Método HTTP POST para enviar dados
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user': user,
            'pass': pass,
        })})
        .then(response => response.json())
        .then(policial => {
            if (policial && Object.keys(policial).length !== 0) {
                clearInterval(interval_get_login);
                stop_fetching_police = true;

                let table = `
                    <table class="police_officer_table">
                        <thead>
                            <tr>
                                <th class="cargo_title">POLICIAL</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <a href="#"><img class="shadow perfil" src="` + policial.foto + `" alt=""></a>
                                </td>
                            </tr>
                            <tr>
                                <td>` + policial.nome + `</td>
                            </tr>
                            <tr>
                                <td>` + policial.matricula + `</td>
                            </tr>
                            <tr>
                                <td>` + policial.telefone + `</td>
                            </tr>
                            <tr>
                                <td>` + policial.lotacao + `</td>
                            </tr>
                            <tr>
                                <td>` + policial.posto + `</td>
                            </tr>
                            <tr>
                                <td>` + policial.email + `</td>
                            </tr>
                        </tbody>
                    </table>
                    `;

                var inputElement = document.createElement("input");
                inputElement.type = "hidden";
                inputElement.name = "plate";
                inputElement.value = policial.matricula;
                plate = policial.matricula;
                document.getElementById("form-equipment").appendChild(inputElement);

                document.getElementById("police_officer_field").innerHTML = table;

                changeTemplate("select_load");
            }
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}

interval_get_login = setInterval(fetch_police, 1000);

function edit(i) {
    if (square_on){
        popUp("Quadro já em uso!", {timer: 2000, overlay: false});
    } else {
        var rows = table_itens.getElementsByTagName("tr"); // pega os tr da tabela
        serialNum = rows[i].getElementsByTagName("td")[1].innerHTML;
        equipmentData = list_equipment[serialNum];
        clearInterval(interval);
        addToSquare(list_equipment[serialNum]);
        removeRow(i);
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

function clearSquare() {
    square_on = false;

    var serialNumberInput = document.getElementById("serial_number");
    var description = document.getElementById("description");
    // var observation = document.getElementById("note_equipment");
    var type = document.getElementById("type");
    var amount = document.getElementById("amount");
    let amount_input = document.getElementById("amount_input");
    
    document.getElementById("means_room_product").src = "/static/img/default.png";
    serialNumberInput.innerText = ' ';
    description.innerText = ' ';
    // observation.innerHTML = ' ';
    type.innerText = ' ';
    amount.innerText = ' ';
    amount_input.value = '1';
    amount_input.disabled = true;
}


// Adiciona o equipamento ao quadro da sala de meios
function addToSquare(data) {
    square_on = true;

    var serialNumberInput = document.getElementById("serial_number");
    var description = document.getElementById("description");
    // var observation = document.getElementById("note_equipment");
    var type = document.getElementById("type");
    var amount = document.getElementById("amount");
    let amount_input = document.getElementById("amount_input");

    tipo_model = {
        'wearable' : 'Vestimento',
        'accessory' : 'Acessório',
        'armament' : 'Armamento',
        'grenada' : 'Granada',
        'bullet' : 'Munição',
        'equipment' : '-',
    }



    data['campo'] = tipo_model[data.registred];
    document.getElementById("means_room_product").src = data.model.image_path; // Muda a imagem

    if (!data.equipment.serial_number) {
        document.getElementById("amount_input").disabled = false;
    }

    // Seta o resto => {
    data.model.description = data.model.description ?? "-";
    serialNumberInput.innerText = data.equipment.serial_number ?? "-";
    description.innerText = data.model.description;
    // observation.innerText = data.equipment.observation == null || data.equipment.observation == undefined ? "" : data.equipment.observation;
    console.log(data.registred);
    console.log(data);
    type.innerText = data["campo"];
    amount.innerText = data.amount == null || data.amount == undefined || data.amount == '' ? "1" : data.amount;
    amount_input.value = amount.innerText;
}