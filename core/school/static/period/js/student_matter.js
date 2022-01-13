let select_period;
let tblMatter;

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
            {data: "matter.level.name"},
            {data: "matter.name"},
        ],
        columnDefs: [],
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
});