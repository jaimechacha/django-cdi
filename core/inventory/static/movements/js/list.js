let input_daterange;
let tblMovements;

let select_user;
let select_material;

function initTable() {
    tblMovements = $('#tblMovements').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
    });
}

function getMovementsData(all) {
    let parameters = {
        'action': 'get_data',
        'material': select_material.val(),
        'user': select_user.val(),
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    tblMovements = $('#tblMovements').DataTable({
        destroy: true,
        responsive: true,
        autoWidth: false,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''
        },
        order: [[0, 'asc']],
        paging: false,
        ordering: true,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-primary btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'Pdf',
                className: 'btn btn-danger btn-flat btn-xs btnPdf'
            }
        ],
        columns: [
            {data: "id_material"},
            {data: "material"},
            {data: "num_doc"},
            {data: "amount_entry"},
            {data: "amount_output"},
            {data: "employee_teacher"},
        ],
        columnDefs: [
            {
                targets: [0, -2, -3, -4],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            }
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        },
    });
}

$(function () {
    input_daterange = $('input[name="date_range"]');
    select_user = $('select[name="users"]');
    select_material = $('select[name="materials"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getMovementsData();
        });

    // $('.drp-buttons').hide();

    initTable();

    select_material.on('change', function () {
        getMovementsData();
    });

    select_user.on('change', function () {
        getMovementsData();
    });

    getMovementsData(true);

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

});