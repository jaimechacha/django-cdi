var tblPsychologicalOrientation;

function getData() {
    tblPsychologicalOrientation = $('#data').DataTable({
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
            {"data": "date_joined"},
            {"data": "matriculation.student.user.full_name"},
            {"data": "matriculation.period.name"},
            {"data": "id"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '';
                    buttons += '<a rel="desc" class="btn btn-info btn-xs btn-flat"><i class="fas fa-pen-alt"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/school/psychological/orientation/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/school/psychological/orientation/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    getData();

    $('#data tbody').on('click', 'a[rel="desc"]', function () {
        $('.tooltip').remove();
        var tr = tblPsychologicalOrientation.cell($(this).closest('td, li')).index(),
            rows = tblPsychologicalOrientation.row(tr.row).data();
        $('.desc').html(rows.desc);
        $('#myModalDesc').modal('show');
    });
});