const typeDropdown = document.getElementById("type");
// const typeIdDropdown = document.getElementById("type_id");
const serialNumberInput = document.getElementById("serial_number");
let equipmentData;

var dataAtual = new Date();
var dia = dataAtual.getDate();
var mes = dataAtual.getMonth() + 1; // Lembrando que os meses começam em 0
var ano = dataAtual.getFullYear();

if (dia < 10) {
    dia = '0' + dia;
}

if (mes < 10) {
    mes = '0' + mes;
}

var time = dataAtual.getHours() + ':' + dataAtual.getMinutes();
var data =  dia + '/' + mes + '/' + ano;

document.getElementById('date').innerText = data;
document.getElementById("time").innerText = time;


fetchEquipmentData = () => {
    fetch('http://localhost:8000/equipment/get')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            // Armazena os dados do equipamento em uma variável pra usar depois
            equipmentData = data;

            // Atualiza os campos com as respectivas opções
            if (data.uid !== '') {
                // Para de ficar requisitando
                clearInterval(interval);

                if (data.registred !== false) {
                    // Muda a imagem
                    let campo;
                    var model;

                    if (data.registred == 'wearable') {
                        campo = 'Vestível';
                    } else if (data.registred == 'acessory') {
                        campo = 'Acessorio';
                    } else if (data.registred == 'armament') {
                        campo = 'Armamento';
                    }
                    // Seta a imagem
                    document.getElementById("means_room_product").src = "/static/" + data['model'].image_path;
                    // Seta o numero de série
                    serialNumberInput.innerText = data['equipment'].serial_number;
                    document.getElementById("description").innerText = data.equipment.observation;
                    document.getElementById("type").innerText = campo;
                    document.getElementById("amount").innerText = '1';
                }
            }
        })
        .catch();
}

// cria um intervalo pra chamar a função a cada 1 segundo
const interval = setInterval(fetchEquipmentData, 1000);