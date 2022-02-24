var tblPeriod;

function getData() {
    tblPeriod = $('#data').DataTable({
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
            {"data": "name"},
            {"data": "initial_date"},
            {"data": "end_date"},
            {"data": "state"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (data) {
                        return '<span class="badge badge-success">Activo</span>';
                    }
                    return '<span class="badge badge-danger">Inactivo</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    const part_date = row.end_date?.split('-');
                    const e_date = new Date(part_date[0], part_date[1]-1, part_date[2]);
                    const today = new Date()
                    if (e_date.getTime() < today){
                        let buttons = '<a href="/school/period/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                        buttons += '<a class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-chalkboard-teacher"></i></a> ';
                        buttons += '<a rel="matters" class="btn btn-info btn-xs btn-flat"><i class="fas fa-book"></i></a> ';
                        return buttons;
                    }

                    let buttons = '<a href="/school/period/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/school/period/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/school/period/assignment/teacher/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-chalkboard-teacher"></i></a> ';
                    buttons += '<a rel="matters" class="btn btn-info btn-xs btn-flat"><i class="fas fa-book"></i></a> ';
                    var buttons = '<a href="/school/period/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" title="Editar Registro"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/school/period/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" title="Eliminar Registro"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/school/period/assignment/teacher/' + row.id + '/" class="btn btn-success btn-xs btn-flat" data-toggle="tooltip" title="Asignación Docente-Nivel"><i class="fas fa-chalkboard-teacher"></i></a> ';
                    buttons += '<a rel="matters" class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalle Registro" ><i class="fas fa-book"></i></a> ';
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

    $('#data tbody').on('click', 'a[rel="matters"]', function () {
        $('.tooltip').remove();
        var tr = tblPeriod.cell($(this).closest('td, li')).index(),
            rows = tblPeriod.row(tr.row).data();
        $('#tblMatter').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_matters',
                    'id': rows.id
                },
                dataSrc: ""
            },
            columns: [
                {data: "contract.teacher.user.full_name"},
                {data: "contract.job.name"},
                {data: "matter.name"},
                {data: "matter.level.name"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                }
            ]
        });
        $('#myModalMatters').modal('show');
    });
});