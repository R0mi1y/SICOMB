var plate; // variável auxiliar para armazenar a matrícula para requisitar do django
var list_awate_equipment = []; // array de equipamentos com os equipamentos a serem cadastrados em formato de dicionário
var turn_type;

// responsável por mudar a tabela da sala de meios de acordo com a requisição
function changeTemplate(template) {
    if (template == "loads_police") {
        document.getElementById("means_room_content").innerHTML = '';
        fetch("http://localhost:8000/carga/get/cargas_policial/" + plate + "/")
            .then(response => response.json())
            .then(data => {
                var table_element = document.createElement('table');

                table_element.innerHTML = `
                <thead>
                    <tr>
                        <th colspan="100%">TABELA DE CARGAS</th>
                    </tr>
                    <tr>
                        <th>ID DE CARGA</th>
                        <th>TIPO</th>
                        <th>QNT. DE ITENS</th>
                        <th>DATA</th>
                        <th>PREVISÃO DE DESCARGA</th>
                    </tr>
                </thead>
                <tbody>
                    `;
                console.log(data.loads_police);

                for (i in data.loads_police) {
                    table_element.innerHTML += 
                    `<tr>
                        <td><button onclick="selectCargo(` + data.loads_police[i].id + `)">` + 
                            data.loads_police[i].id
                        + `</button></td>  
                        <td>` + 
                            data.loads_police[i].turn_type
                        + `</td>  
                        <td>` + 
                            data.loads_police[i].itens_amount
                        + `</td>  
                        <td>` + 
                            data.loads_police[i].date_load
                        + `</td>  
                        <td>` + 
                            data.loads_police[i].expected_load_return_date
                        + `</td>  
                    </tr>`;
                }
                table_element.innerHTML += '</tbody>';

                document.getElementById("means_room_content").appendChild(table_element);
                setTimeout(() => {
                    var script = document.createElement('script');
                    script.src = '/static/js/fetch_unload.js';
                    script.id = 'fetch_load.js';
                    document.head.appendChild(script);

                    document.getElementById("search-btn").addEventListener("click", () => {
                        let search = document.getElementById("search-camp");
                        fetchEquipmentData(search.value);
                        search.value = '';
                    });
            }, 1000);
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


// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
var table_itens = document.getElementById('body_table_itens'); // tabela de itens do html
function insertLine(line, x) {
    // console.log(line);
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
    fetch(url)
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
                        <a href="#"><img class="shadow" src="/media/` + policial.foto + `" alt=""></a>
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
                document.getElementById("submit_btn").disabled = false;

                changeTemplate("select_load");
            }
        });
}, 1000);

// Adiciona o equipamento ao quadro da sala de meios
function addToSquare(data) {
    data['campo'] = data.registred == 'wearable' ? 'Vestmento' : data['campo'];
    data['campo'] = data.registred == 'accessory' ? 'Acessório' : data['campo'];
    data['campo'] = data.registred == 'armament' ? 'Armamento' : data['campo'];
    data['campo'] = data.registred == 'grenada' ? 'Granada' : data['campo'];
    data['campo'] = data.registred == 'bullet' ? 'Munição' : data['campo'];

    // console.log(document.getElementById("means_room_product"));
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
}