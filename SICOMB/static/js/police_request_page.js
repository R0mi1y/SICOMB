let table_itens = $("#actually_load");
let list_equipment;

setInterval(() => {
    fetchList();
    getInfoLoad();
}, 1000);

function fetchList() {
    $.ajax({
        url: '/carga/lista_equipamentos_atual/get',
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
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

function getInfoLoad() {
    $.ajax({
        url: '/carga/info/get',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (data) {
            console.log(data);
            if (data.matricula == null) {
                window.location = "/police/login/";
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
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
        url: '/equipamento/allow_cargo',
        type: 'POST',
        data: {
            user: user,
            pass: pass
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
    // location.reload();
}
