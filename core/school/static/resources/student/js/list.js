var tblResources;
var select_period;

function getData() {
    tblResources = $('#data').DataTable({
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
            {"data": "typeresource.name"},
            {"data": "perioddetail.period.name"},
            {"data": "perioddetail.matter.name"},
            {"data": "perioddetail.matter.level.name"},
            {"data": "start_date"},
            {"data": "end_date"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-folder-open"></i></a> ';
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

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var tr = tblResources.cell($(this).closest('td, li')).index(),
            rows = tblResources.row(tr.row).data();
        $('.desc').html('<b>Descripción:</b><br>' + rows.desc);
        $('.link-desc').attr('href', rows.web_address);
        $('#myModalDetails').modal('show');
    });
});