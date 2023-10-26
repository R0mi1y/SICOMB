let table_itens = $("#actually_load");
let list_equipment;

setInterval(fetchList, 1000);

function fetchList() {
    $.ajax({
        url: 'http://localhost:8000/carga/lista_equipamentos_atual/get',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (data) {
            table_itens.empty();
            list_equipment = data;
            $.each(data, function (key, line) {
                insertLine(line);
            });
        }
    });
}

function insertLine(line) {
    var newRow = $("<tr>").append(
        $("<td></td>"),
        $("<td>").text(line.equipment.serial_number || "-"),
        $("<td>").text(line.model.description || "-"),
        $("<td>").text(line.campo || "-"),
        $("<td>").text(line.model.caliber || "-"),
        $("<td>").text(line.amount || "1"),
        $("<td>").text(line.registred === 'wearable' ? line.model.size : "-"),
        $("<td>").text(line.equipment.observation || "-"),
        $("<td></td>")
    );
    table_itens.append(newRow);

    updateRowNumbers();
}

function updateRowNumbers() {
    var rows = table_itens.find("tr");
    rows.each(function (index) {
        $(this).find("td:first").text(index + 1);
    });
}

function confirmCargo(self) {
    self.style.backgroundColor = "#9999";
    self.style.color = "black";
    $.ajax({
        url: 'http://localhost:8000/equipamento/allow_cargo',
        type: 'POST',
        data: {
            user: user,
            pass: pass
        }
    });
}
