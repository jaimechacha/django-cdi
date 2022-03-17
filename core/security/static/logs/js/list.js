
function getData() {
    $('#data').DataTable({
        "order": [[ 0, "desc" ]],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search'
            },
            dataSrc: "",
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-primary btn-flat btn-xs'
            },
            {
                extend: 'print',
                text: 'Imprimir listado <i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-success btn-flat btn-xs',
                messageTop: "<h5>Listado de Actividades de Usuarios</h5>",
                title:  "<h4 style='text-align: center;'>Centro de desarrollo infaltíl 'Pequeños Sabios' </h4>",
                     
            },
        ],
        columns: [
            {data: "date"},
            {data: "user"},
            {data: "object_repr"},
            {data: "action_text"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                     if (row.action_text === 'Creado' ){
                            return `<i class="fas fa-plus mr-2 text-green"></i> ${row.action_text}`;
                     }else if (row.action_text == 'Modificado'){
                        return `<i class="fas fa-pen-square mr-2 text-yellow"></i> ${row.action_text}`;
                     }else {
                        return `<i class="fas fa-minus-circle mr-2 text-red"></i> ${ row.action_text}`;
                     }
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
}

$(function () {
    getData();
});