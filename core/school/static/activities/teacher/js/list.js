var tblActivities;
var select_period;

function getData() {
    tblActivities = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search',
                'period': select_period.val()
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "typeactivity.name"},
            {"data": "perioddetail.period.name"},
            {"data": "perioddetail.matter.name"},
            {"data": "perioddetail.matter.level.name"},
            {"data": "start_date"},
            {"data": "end_date"},
            {"data": "id"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-folder-open"></i></a> ';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/school/activities/teacher/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/school/activities/teacher/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a rel="notes" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-word"></i></a> ';
                    buttons += '<a href="/school/activities/teacher/qualify/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-sticky-note"></i></a> ';
                    return buttons;
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

    select_period.on('change', function () {
        getData();
    });

    getData();

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            $('.tooltip').remove();
            var tr = tblActivities.cell($(this).closest('td, li')).index(),
                rows = tblActivities.row(tr.row).data();
            $('.desc').html('<b>Descripción:</b><br>' + rows.desc);
            $('.link-desc').attr('href', rows.web_address);
            $('.link-rubric').attr('href', rows.rubric);
            $('#myModalDetails').modal('show');
        })
        .on('click', 'a[rel="notes"]', function () {
            $('.tooltip').remove();
            var tr = tblActivities.cell($(this).closest('td, li')).index(),
                rows = tblActivities.row(tr.row).data();
            $('#tblNotes').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_notes',
                        'id': rows.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "student.user.full_name"},
                    {data: "archive"},
                    {data: "comment"},
                    {data: "note"},
                ],
                columnDefs: [
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<a target="_blank" href="' + row.archive + '" class="btn btn-primary btn-xs"><i class="fas fa-file-word"></i></a>';
                        }
                    },
                ]
            });
            $('#myModalNotes').modal('show');
        });
});