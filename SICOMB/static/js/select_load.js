
// var insert_btn = document.getElementById("insert_btn");
var table_itens = document.getElementById('body_table_itens'); // tabela de itens do html
var plate; // variável auxiliar para armazenar a matrícula para requisitar do django
var list_awate_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var list_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var turn_type;

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
        fetch("http://localhost:8000/carga/get/cargas_policial/" + plate + "/", {
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
                    `<tr class="tr_cargos" onclick="selectCargo(` + data.loads_police[i].id + `)">
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
            });
    } else {
        fetch("/static/html/" + template + ".html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("means_room_content").innerHTML = data;
        })
        if (template == "load") {
            setTimeout(() => {
                var script = document.createElement('script');
                script.src = '/static/js/fetch_load.js';
                script.id = 'fetch_load.js';
                document.head.appendChild(script);

                document.getElementById("search-btn").addEventListener("click", () => {
                    let search = document.getElementById("search-camp");
                    fetchEquipmentData(search.value);
                    search.value = '';
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
}


// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
function insertLine(line, x) {
    x = x ?? true;
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
            cells[cells.length - 1].innerHTML = '<a href="#" onclick="checkRemoveRow(' + i + ')">| X |</a>'; // ultima coluna, o botão de remover
        } else {
            cells[cells.length - 1].innerHTML = '| X |'; // ultima coluna, o botão de remover
            cells[cells.length - 1].style.color = 'red'; // ultima coluna, o botão de remover
        }
    }
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

var interval = setInterval(() => {
    let url = 'http://localhost:8000/police/get_login/';
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
                clearInterval(interval);

                let table = `<table class="police_officer_table">
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
                    <td>` + policial.email + `</td>
                </tr>
            </tbody>
            </table>`;

                var inputElement = document.createElement("input");
                inputElement.type = "hidden";
                inputElement.name = "plate";
                inputElement.value = policial.matricula;
                plate = policial.matricula;
                document.getElementById("form-equipment").appendChild(inputElement);

                document.getElementById("police_officer_field").innerHTML = table;

                changeTemplate("select_load");
            }
        });
}, 1000);


function clearSquare() {
    var serialNumberInput = document.getElementById("serial_number");
    var description = document.getElementById("description");
    var observation = document.getElementById("note_equipment");
    var type = document.getElementById("type");
    var amount = document.getElementById("amount");
    let amount_input = document.getElementById("amount_input");
    
    document.getElementById("means_room_product").src = "/static/img/default.png";
    serialNumberInput.innerText = ' ';
    description.innerText = ' ';
    observation.innerHTML = ' ';
    type.innerText = ' ';
    amount.innerText = ' ';
    amount_input.value = '1';
    amount_input.disabled = true;
}


// Adiciona o equipamento ao quadro da sala de meios
function addToSquare(data) {
    var serialNumberInput = document.getElementById("serial_number");
    var description = document.getElementById("description");
    var observation = document.getElementById("note_equipment");
    var type = document.getElementById("type");
    var amount = document.getElementById("amount");
    let amount_input = document.getElementById("amount_input");

    tipo_model = {
        'wearable' : 'Vestmento',
        'accessory' : 'Acessório',
        'armament' : 'Armamento',
        'grenada' : 'Granada',
        'bullet' : 'Munição',
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
    observation.innerText = data.equipment.observation == null || data.equipment.observation == undefined ? "" : data.equipment.observation;
    type.innerText = data.campo;
    amount.innerText = data.amount == null || data.amount == undefined || data.amount == '' ? "1" : data.amount;
    amount_input.value = amount.innerText;
}