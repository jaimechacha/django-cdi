var select_period;
var tblMatter;

function getData() {
    tblMatter = $('#tblMatter').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_period',
                'period': select_period.val()
            },
            dataSrc: ""
        },
        columns: [
            {data: "matter.name"},
            {data: "matter.level.name"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="students" class="btn btn-success btn-xs btn-flat"><i class="fas fa-user-friends"></i></a>';
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    select_period = $('select[name="period"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period
        .on('change.select2', function () {
            getData();
        });

    $('#tblMatter tbody').on('click', 'a[rel="students"]', function () {
        $('.tooltip').remove();
        var tr = tblMatter.cell($(this).closest('td, li')).index(),
            rows = tblMatter.row(tr.row).data();
        $('#tblStudents').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_students',
                    'id': rows.id
                },
                dataSrc: ""
            },
            columns: [
                {data: "student.user.full_name"},
                {data: "student.user.dni"},
                {data: "student.mobile"},
                {data: "student.user.email"},
            ],
            columnDefs: []
        });
        $('#myModalStudents').modal('show');
    });
});