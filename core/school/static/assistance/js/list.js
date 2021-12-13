var btnRemoveAssist;
var current_date;
var tblAssistance = null;
var input_daterange;

function getAssists() {
    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    tblAssistance = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "date_joined"},
            {data: "user.full_name"},
            {data: "user.dni"},
            {data: "state"},
            {data: "desc"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    if (!$.isEmptyObject(row.desc)) {
                        return row.desc;
                    }
                    return 'Sin detalles';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.state) {
                        return 'Si';
                    }
                    return 'No';
                }
            },
        ],
        initComplete: function (settings, json) {
            btnRemoveAssist.prop('disabled', $.isEmptyObject(json));
        }
    });
}

$(function () {

    input_daterange = $('input[name="date_range"]');
    current_date = new moment().format('YYYY-MM-DD');
    btnRemoveAssist = $('.btnRemoveAssist');

    btnRemoveAssist.prop('disabled', true);

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getAssists();
        });

    //$('.applyBtn').hide();

    $('.btnSearchAssist').on('click', function () {
        getAssists();
    });

    btnRemoveAssist.on('click', function () {
        var start_date = input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD');
        var end_date = input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD');
        location.href = pathname + 'delete/' + start_date + '/' + end_date + '/';
    });

    getAssists();
});
