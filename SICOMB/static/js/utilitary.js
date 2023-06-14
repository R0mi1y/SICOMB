var id_overlay = 0;
var aux = {};

function popUp(message, close_btn, yn, adictional) {
    close_btn = close_btn ? ? true;
    yn = yn ? ? false;
    adictional = adictional ? ? false;

    var overlayHTML = `
    <div id="overlay` + id_overlay + `" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;">
    <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #fff; padding: 20px;padding-top: 20px; border-radius: 5px; z-index: 10000;">
    `;
    if (close_btn) { // se quer q tenha botão de fechar
        overlayHTML += `
        <button onclick="removerpopUp()" style="position: absolute; top: -15px; right: 10px; background-color: red; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 50%; cursor: pointer;">
        x
        </button>`;
    }
    overlayHTML += '<p style="margin: 0;">' + message + "</p>"
    if (adictional) {
        overlayHTML += adictional;
    }
    if (yn) { // se quer q tenha os botões de sim ou não
        overlayHTML += `
        <button onclick="answerY()" style="background-color: green; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-right: 10px;">
            Sim
        </button>
        <button onclick="answerN()" style="background-color: red; color: white; border: none; padding: 5px 10px; font-size: 16px; border-radius: 5px; cursor: pointer;">
            Não
        </button>
        `;

    }
    overlayHTML += "</div></div>";
    id_overlay++; // serve para contar e separar se tiver mais de um popUpa

    document.body.insertAdjacentHTML('beforeend', overlayHTML);
}

// remove o popUpa
function removerpopUp() {
    id_overlay--;
    const overlay = document.getElementById('overlay' + id_overlay);
    if (overlay) {
        overlay.remove();
    }
}

function answerN() {
    eval(aux["funN"]);
    removerpopUp();
}

function answerY() {
    eval(aux["funY"]);
    removerpopUp();
}

var cargo = `
<div class="means_room_table">
    <table>
        <thead>
            <tr>
                <th colspan="5" class="cargo_title">SALA DE MEIOS</th>
            </tr>
        </thead>
        <tbody class="tbody_top_means_room">
            <tr>
                <td>DATA DE SOLICITAÇÃO</td>
                <td>HORA</td>
                <td class="checkbox">
                    <input type="radio" id="six-hours" name="options_load">
                    <label for="six-hours">6H</label>
                </td>
                <td class="checkbox">
                    <input type="radio" id="twenty-four-hours" name="options_load">
                    <label for="twenty-four-hours">24H</label>
                </td>
                <td class="checkbox">
                    <input type="radio" id="court-order" name="options_load">
                    <label for="court-order">REQUISIÇÃO JUDICIAL</label>
                </td>
            </tr>
            <tr>
                <td>
                    <h4 id="date"></h4>
                </td>
                <td>
                    <h4 id="time"></h4>
                </td>
                <td class="checkbox">
                    <input type="radio" id="twelve-hours" name="options_load">
                    <label for="twelve-hours">12H</label>
                </td>
                <td class="checkbox">
                    <input type="radio" id="repair" name="options_load">
                    <label for="repair">CONSERTO</label>
                </td>
                <td class="checkbox">
                    <input type="radio" id="indeterminate" name="options_load">
                    <label for="indeterminate">INDETERMINADO</label>
                </td>
            </tr>
        </tbody>
    </table>

</div>
<div class="row_color"><span>
        <hr>
    </span></div>
<div class="search-info">
    <div class="search-table">
        <table cellspacing="0" cellpadding="0" align="center">
            <thead>
                <tr>
                    <td>NUM. DE SÉRIE/ID</td>
                    <td>QUANTIDADE</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="search-box">
                        <input type="text" id="search-camp" class="search-txt" placeholder="Pesquisar">
                        <a href="#" class="search-btn">
                            <img class="img-search" id="search-btn" src="/static/img/search.png" alt="">
                        </a>
                    </td>
                    <td class="put_qnt"><input type="text" id="amount_input" name="name" disabled required placeholder="1" /></td>
                    <!-- <td rowspan="2">
                                
                    </td> -->
                </tr>
            </tbody>
        </table>
    </div>
    <div class="img_product">
        <img class="means_room_product" id="means_room_product" src="/static/img/default.png" alt="">
    </div>
</div>
<hr>
<div class="info_product">
    <table>
        <thead>
            <tr>
                <th>NUM. DE SÉRIE / ID</th>
                <th colspan="2">DESCRIÇÃO</th>
                <th>TIPO</th>
                <th>QNT</th>
            </tr>
        </thead>
        <tbody>
            <tr class="description_product">
                <td id="serial_number">&nbsp;</td>
                <td id="description" colspan="2">&nbsp;</td>
                <td id="type">&nbsp;</td>
                <td id="amount">&nbsp;</td>
            </tr>
        </tbody>
    </table>
</div>
<hr>
<div class="bottom_means_room">
    <div class="note">
        <h5>OBSERVAÇÃO: </h5>
        <textarea id="note_equipment" name="note" rows="3" cols="60">
        </textarea>
    </div>
    <div class="insert_button">
        <button id="insert_btn" class="btn btn-insert shadow">INSERIR</button>
    </div>
</div>
`

var select_cargo = `
<div class="means_room_content">
                            <div class="means_room">
                                <h1 class="title">Você está fazendo uma carga ou descarga de materiais?</h1>
                                <div class="loading_or_unloading ">
                                    <ul class="choice_loading_unloading ">
                                        <li>
                                            <a onclick="changeTemplate('select_time')" href="#"><span>CARGA</span></a>
                                        </li>
                                        <li>
                                            <a onclick="changeTemplate('select_cargo')" href="#"><span>DESCARGA</span></a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
`

var select_time = ` 
<div class="means_room_content">
<div class="means_room">
    <h1 class="title">Escolha uma das opções que se refere a esta carga</h1>
    <div class="loading_or_unloading ">
        
        <table>
            <thead>
                <tr>
                </tr>
            </thead>
            <tbody class="tbody_top_means_room">
                <tr>
                    <td class="checkbox">
                        <input type="radio" id="six-hours" name="options_load">
                        <label for="six-hours">6H</label>
                    </td>
                    <td class="checkbox">
                        <input type="radio" id="twenty-four-hours" name="options_load">
                        <label for="twenty-four-hours">24H</label>
                    </td>
                    <td class="checkbox">
                        <input type="radio" id="court-order" name="options_load">
                        <label for="court-order">REQUISIÇÃO JUDICIAL</label>
                    </td>
                </tr>
                <tr>
                    <td class="checkbox">
                        <input type="radio" id="twelve-hours" name="options_load">
                        <label for="twelve-hours">12H</label>
                    </td>
                    <td class="checkbox">
                        <input type="radio" id="repair" name="options_load">
                        <label for="repair">CONSERTO</label>
                    </td>
                    <td class="checkbox">
                        <input type="radio" id="indeterminate" name="options_load">
                        <label for="indeterminate">INDETERMINADO</label>
                    </td>
                </tr>
            </tbody>
        </table>
        
    </div>
</div>

<div class="insert_button button_continue">
    <input type="button" onclick="changeTemplate('select_cargo')" value="CONTINUAR" class="btn btn-insert shadow">
</div>
<div class="return_button">
    <a href="#" class="return-btn">
        <img class="img-return" src="img/return-icon2.png" alt="">
    </a>
</div>
`

// var sala_meios = document.getElementById("means_room_content");
// sala_meios.innerHTML = select_cargo;

// function changeTemplate(template) {

//     if (template == "select_time") sala_meios.innerHTML = select_time;
//     else if (template == "select_cargo") {
//         window.location.href = './t';
//     }
// }