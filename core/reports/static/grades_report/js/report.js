let tblReport = null;
let columns = [];
let select_period;
let select_course;
let input_daterange;

let matter_activities = [];


function get_number_activities(matter_id) {
    $.ajax({
        url: pathname,
        type: 'POST',
        data: {
            'action': 'search_activities',
            'matter': matter_id,
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        },
        success: function (result) {
            matter_activities = result
            let table = $("#tblReport")
            document.getElementById("tblReport").deleteTHead();
            let content = ''
            content += '<thead><tr>';
            content += '<th class="text-center">Estudiante</th>';
            matter_activities.forEach((e, i) => {
                content += `<th class="text-center text-xs">
                                N${i + 1}<br/> <small>${e.name}</small>
                            </th>`;
            })
            content += '</tr></thead>';
            $(table).append(content)
        }
    });
}

function initTable() {
    tblReport = $('#tblReport').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
    });

    // $.each(tblReport.settings()[0].aoColumns, function (key, value) {
    //     columns.push(value.sWidthOrig);
    // });
}

function clearDatatable() {
    $('#tblReport').DataTable().destroy();
    $('#tblReport tbody').empty();
}

function generateGradeReport(matter_id) {

    get_number_activities(matter_id);

    let parameters = {
        'action': 'search_students',
        'period': select_period.val(),
        'course': select_course.val(),
        'matter': matter_id,
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (parameters.matter === '' || parameters.course === '' || parameters.period === '') {
        if (tblReport !== null) {
            tblReport.clear().draw();
        }
        return false;
    }

    let data_grades = []
    let columns_table = []
    let columns_name = []

    $.ajax({
        url: pathname,
        type: 'POST',
        data: parameters,
        success: function (result) {
            if (result.hasOwnProperty('error')) {
                message_error(result.error);
                return false;
            }

            clearDatatable();

            if (result.length > 0) {
                data_grades = result
                columns_name = Object.keys(data_grades[0]);

                columns_table = []
                columns_name.forEach(e => columns_table.push({data: e}))
                tblReport = $('#tblReport').DataTable({
                    destroy: true,
                    responsive: true,
                    autoWidth: false,
                    data: data_grades,
                    paging: false,
                    ordering: true,
                    searching: false,
                    dom: 'Bfrtip',
                    buttons: [
                        {
                            extend: 'excelHtml5',
                            text: 'Descargar excel <i class="fas fa-file-excel"></i>',
                            titleAttr: 'Excel',
                            className: 'btn btn-primary btn-flat btn-xs'
                        },
                        {
                            extend: 'pdfHtml5',
                            text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                            titleAttr: 'Pdf',
                            className: 'btn btn-danger btn-flat btn-xs btnPdf',
                            action: function (e, dt, node, config) {
                                parameters['action'] = 'generate_pdf';
                                $.ajax({
                                    url: pathname,
                                    type: 'POST',
                                    data: parameters,
                                    xhrFields: {
                                        responseType: 'blob'
                                    },
                                    success: function (request) {
                                        console.log(request);
                                        let d = new Date();
                                        let date_now = d.getFullYear() + "_" + d.getMonth() + "_" + d.getDay();
                                        let a = document.createElement("a");
                                        document.body.appendChild(a);
                                        a.style = "display: none";
                                        const blob = new Blob([request], {type: 'application/pdf'});
                                        const url = URL.createObjectURL(blob);
                                        a.href = url;
                                        a.download = "download_pdf_" + date_now + ".pdf";
                                        a.click();
                                        window.URL.revokeObjectURL(url);
                                    },
                                    error: function (jqXHR, textStatus, errorThrown) {
                                        message_error(errorThrown + ' ' + textStatus);
                                    }
                                });
                            }
                        }
                    ],
                    columns: columns_table,
                    columnDefs: [
                        {
                            targets: '_all',
                            class: 'text-center',
                        },
                    ],
                });
            }

        }
    });
}

function generateReport(all) {
    let parameters = {
        'action': 'search_students',
        'period': select_period.val(),
        'course': select_course.val(),
        'matter': select_matter.val(),
    };

    tblReport = $('#tblReport').DataTable({
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
                className: 'btn btn-danger btn-flat btn-xs btnPdf',
                action: function (e, dt, node, config) {
                    parameters['action'] = 'generate_pdf';
                    $.ajax({
                        url: pathname,
                        type: 'POST',
                        data: parameters,
                        xhrFields: {
                            responseType: 'blob'
                        },
                        success: function (request) {
                            console.log(request);
                            let d = new Date();
                            let date_now = d.getFullYear() + "_" + d.getMonth() + "_" + d.getDay();
                            let a = document.createElement("a");
                            document.body.appendChild(a);
                            a.style = "display: none";
                            const blob = new Blob([request], {type: 'application/pdf'});
                            const url = URL.createObjectURL(blob);
                            a.href = url;
                            a.download = "download_pdf_" + date_now + ".pdf";
                            a.click();
                            window.URL.revokeObjectURL(url);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            message_error(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            }
        ],
        columns: [
            {data: "student"},
            {data: "0"},
            {data: "1"},
            {data: "2"},
            {data: "3"},
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

    tblReport = $('#tblReport').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
    });

    select_period = $('select[name="period"]');
    select_course = $('select[name="course"]');
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })

    $("#search_materia").autocomplete({
        source: function (request, response) {
            if (select_course.val() === '') {
                alert('Seleccione un nivel');
                $('#search_materia').val('').focus();
                return false;
            }
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_materia',
                    'level': select_course.val(),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            generateGradeReport(ui.item.id);
            $(this).blur();
            $(this).val('').focus();
        }
    });

    $('#clearSearchMateria').on('click', function () {
        $('#search_materia').val('').focus();
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('.drp-buttons').hide();


    // initTable();

});