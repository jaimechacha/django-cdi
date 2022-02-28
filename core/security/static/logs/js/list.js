
function getData() {
    $('#data').DataTable({
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
                extend: 'print',
                text: 'Imprimir listado <i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-success btn-flat btn-xs'
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