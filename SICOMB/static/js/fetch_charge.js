var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
var imageEquipment = document.getElementById("means_room_product");
var observation = document.getElementById("note_equipment");
var equipmentData;

console.log(
    serialNumberInput + ", \n" +
    description + ", \n" +
    type + ", \n" +
    amount + ", \n" +
    imageEquipment + ", \n"
);

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

var fetchEquipmentData = () => {
    fetch('http://localhost:8000/equipment/get')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            // Armazena os dados do equipamento em uma variável para uso posterior
            equipmentData = data;

            // Atualiza os campos com as respectivas opções
            if (data.uid !== '') {
                // Para de ficar requisitando
                clearInterval(interval);

                if (data.registred !== false) {
                    // Muda a imagem
                    let campo;

                    if (data.registred === 'wearable') {
                        campo = 'Vestível';
                    } else if (data.registred === 'accessory') {
                        campo = 'Acessório';
                    } else if (data.registred === 'armament') {
                        campo = 'Armamento';
                    }

                    // Seta a imagem
                    imageEquipment.src = "/static/" + data.model.image_path;

                    // Seta o número de série
                    serialNumberInput.innerText = data.equipment.serial_number;
                    description.innerText = data.model.description;
                    observation.innerText = data.equipment.observation;
                    type.innerText = campo;
                    amount.innerText = '1';
                }
            }
        })
        .catch(error => {
            console.error('Erro ao buscar dados do equipamento:', error);
        });
}

// Cria um intervalo para chamar a função a cada 1 segundo
var interval = setInterval(fetchEquipmentData, 1000);
