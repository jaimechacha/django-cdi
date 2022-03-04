let tblActivities;
let select_period;
let select_matter;
let activities;

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
                'period': select_period.val(),
                'matter': select_matter.val()
            },
            dataSrc: ""
        },
        columns: [
            {"data": "notedetails.id"},
            {"data": "notedetails.name"},
            {"data": "notedetails.typeactivity.name"},
            //{"data": "notedetails.perioddetail.period.name"},
            {"data": "notedetails.start_date"},
            {"data": "notedetails.end_date"},
            {"data": "comment"},
            {"data": "evidence_doc"},
            {"data": "note"},
            {"data": "score.name"},
            {"data": "notedetails.perioddetail.matter.name"},
            {"data": "notedetails.perioddetail.matter.level.name"},
            {"data": "notedetails.perioddetail.contract.teacher.user.first_name"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,

            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.exists_doc) {
                        return `<a href="${row.evidence_doc}" target="_blank">Ver archivo</a>`
                    }
                    return `<span>Archivo no encontrado</span>`
                }
            },

        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    select_period = $('select[name="period"]');
    select_matter = $('select[name="matter"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period.on('change', function () {
        getData();
    });

    select_matter.on('change', function () {
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