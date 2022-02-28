function getData() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "user.full_name"},
            {"data": "user.dni"},
            {"data": "mobile"},
            {"data": "user.email"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/school/student/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" title="Editar Registro"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/school/student/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" title="Eliminar Registro"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/school/student/detail/' + row.id + '/" class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Perfil"><i class="fas fa-portrait"></i></a>';
                    return buttons;
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