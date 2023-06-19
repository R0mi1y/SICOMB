var plate; // variável auxiliar para armazenar a matrícula para requisitar do django

// responsável por mudar a tabela da sala de meios de acordo com a requisição
function changeTemplate(template) {
    if (template == "cargos_police") {
        document.getElementById("means_room_content").innerHTML = '';
        fetch("http://localhost:8000/cargo/get/cargos_police/" + plate + "/")
            .then(response => response.json())
            .then(data => {
                var table_element = document.createElement('table');

                table_element.innerHTML = `
                <thead>
                    <tr>
                        <th colspan="100%">TABELA DE CARGOS</th>
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
                console.log(data.cargos_police);

                for (i in data.cargos_police) {
                    table_element.innerHTML += 
                    `<tr>
                        <td><button onclick="selectCargo(` + data.cargos_police[i].id + `)">` + 
                            data.cargos_police[i].id
                        + `</button></td>  
                        <td>` + 
                            data.cargos_police[i].turn_type
                        + `</td>  
                        <td>` + 
                            data.cargos_police[i].itens_amount
                        + `</td>  
                        <td>` + 
                            data.cargos_police[i].date_cargo
                        + `</td>  
                        <td>` + 
                            data.cargos_police[i].expected_cargo_return_date
                        + `</td>  
                    </tr>`;
                }
                table_element.innerHTML += '</tbody>';

                document.getElementById("means_room_content").appendChild(table_element);
                setTimeout(() => {
                    var script = document.createElement('script');
                    script.src = '/static/js/fetch_uncargo.js';
                    script.id = 'fetch_cargo.js';
                    document.head.appendChild(script);
            }, 1000);
            });
    } else {
        fetch("/static/html/" + template + ".html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("means_room_content").innerHTML = data;
        })
        if (template == "cargo") {
            setTimeout(() => {
                var script = document.createElement('script');
                script.src = '/static/js/fetch_cargo.js';
                script.id = 'fetch_cargo.js';
                document.head.appendChild(script);
            }, 500)
        } 
    }
}

// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
var table_itens = document.getElementById('body_table_itens'); // tabela de itens do html

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

// Básicamente checa o numero que foi retirado e renumera as linha de acordo e coloca o botão de excluir linha
function updateRowNumbers() {
    var rows = table_itens.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        cells[0].innerHTML = i + 1; // primeira coluna, a do numero de série da tabela
        cells[cells.length - 1].innerHTML = '<a href="#" onclick="checkRemoveRow(' + i + ')">| X |</a>'; // ultima coluna, o botão de remover
    }
}

var turn_type;

function setTurnType() {
    var radioSelecionado = document.querySelector('input[name="options_load"]:checked');

    if (radioSelecionado && radioSelecionado.value) {
        var inputElement = document.createElement("input");
        inputElement.type = "hidden";
        inputElement.name = "turn_type";
        inputElement.value = radioSelecionado.value;
        document.getElementById("form-equipment").appendChild(inputElement);

        turn_type = radioSelecionado.value;
        changeTemplate("cargo");
    } else {
        popUp("Selecione uma das opções!");
    }
}

var interval = setInterval(() => {
    let url = 'http://localhost:8000/police/get_login/';
    fetch(url)
        .then(response => response.json())
        .then(policial => {
            console.log(policial);
            if (policial && Object.keys(policial).length !== 0) {
                clearInterval(interval);

                let table = `<table class="police_officer_table">
            <thead>
                <tr>
                    <th class="cargo_title">` + policial.lotacao + `</th>
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

                changeTemplate("select_cargo");
            }
        });
}, 1000);