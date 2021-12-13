var tblActivities;
var select_period;
var activities;

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
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (!$.isEmptyObject(row.calif)) {
                        return parseFloat(row.calif.note).toFixed(2);
                    }
                    return 'Sin calificar';
                }
            },
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
                    var buttons = '';
                    if ($.isEmptyObject(row.calif)) {
                        buttons = '<a class="btn btn-warning btn-xs btn-flat" rel="upload"><i class="fas fa-file-upload"></i></a> ';
                    } else {
                        buttons += '<a class="btn btn-info btn-xs btn-flat" target="_blank" href="' + row.calif.archive + '"><i class="fas fa-file-word"></i></a>';
                    }
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
        .on('click', 'a[rel="upload"]', function () {
            $('.tooltip').remove();
            var tr = tblActivities.cell($(this).closest('td, li')).index();
            activities = tblActivities.row(tr.row).data();
            $('#myModalUpload').modal('show');
        })
        .on('click', 'a[rel="details"]', function () {
            $('.tooltip').remove();
            var tr = tblActivities.cell($(this).closest('td, li')).index(),
                rows = tblActivities.row(tr.row).data();
            $('.desc').html('<b>Descripción:</b><br>' + rows.desc);
            $('.link-desc').attr('href', rows.web_address);
            $('.link-rubric').attr('href', rows.rubric);
            $('#myModalDetails').modal('show');
        });
});