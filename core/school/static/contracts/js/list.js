var tblContracts;

function getData() {
    tblContracts = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search',
            },
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "teacher.user.full_name"},
            {data: "job.name"},
            //{data: "start_date"},
           // {data: "end_date"},
            //{data: "base_salary"},
            {data: "state"},
            {data: "id"},
        ],
        columnDefs: [
            /*
            {
                targets: [3, 4],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-3],
                class: 'text-left',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            }, */
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.state) {
                        return '<span class="badge badge-success">Activo</span>';
                    }
                    return '<span class="badge badge-danger">Inactivo</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    if (row.state) {
                        buttons += '<a href="/school/contracts/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" title="Editar"><i class="fas fa-edit"></i></a> ';
                    }
                    buttons += '<a href="/school/contracts/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" title="Eliminar"><i class="fas fa-trash"></i></a> ';
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