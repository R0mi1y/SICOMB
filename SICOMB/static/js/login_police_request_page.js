var reg_fingerprints_assets = {};

function fetchList() {
    $.ajax({
        url: '/police/get_fingerprint/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function(data) {
            console.log(data);
            if (data.status) {
                $('input[name="type_login"]').val("fingerprint");
                $('input[name="token"]').val(data.token);

                $('#form_login').submit();
            } else if (data.type) {
                if (data.type == "USERMESSAGE" || data.type == "ERROR" || data.type == "SUCCESS") {
                    if (!(data.message)) return;

                    if (reg_fingerprints_assets["popUp"]) {
                        reg_fingerprints_assets["popUp"]["close_function"]()
                    }

                    if (data.type == "SUCCESS") {
                        reg_fingerprints_assets["popUp"] = popUp(data.message, { timer: 2000 });
                    } else if (data.type == "ERROR") {
                        reg_fingerprints_assets["popUp"] = popUp(data.message);
                    } else {
                        reg_fingerprints_assets["popUp"] = popUp(data.message, { closeBtn: false });
                    }
                } else {
                    if (data.message)
                        popUp(data.message, { timer: 2000, overlay: false });
                }
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}
var interval = setInterval(fetchList, 1000);

$(document).ready(function() {

    $("#request_fingerprint").on("click", function () {
        $.ajax({
            url: '/police/request/fingerprint/',
            type: 'POST',
            dataType: 'json',
            data: {
                user: user,
                pass: pass
            },
            success: function(data) {
                popUp("Requisitando impressão digital...", { overlay: false, timer: 2000 })
            },
            error: function (error) {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            }
        });
    });

    
});