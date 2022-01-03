let tblReport = null;
let columns = [];
let select_period;
let select_course;
let select_matter;

let matter_activities = [];

function get_number_activities() {
    $.ajax({
        url: pathname,
        type: 'POST',
        data: {
            'action': 'search_activities',
            'matter': select_matter.val(),
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
            // console.log(result)
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

function generateGradeReport() {
    let parameters = {
        'action': 'search_students',
        'period': select_period.val(),
        'course': select_course.val(),
        'matter': select_matter.val(),
    };

    if (parameters.matter === '' || parameters.course === '' || parameters.period === '') {
        if (tblReport !== null) {
            tblReport.clear().draw();
        }
        return false;
    }

    let data_grades = null
    let columns_table = []

    $.ajax({
        url: pathname,
        type: 'POST',
        data: parameters,
        success: function (result) {
            data_grades = result
            const columnNames = Object.keys(data_grades[0]);
            columnNames.forEach(e => columns_table.push({data: e}))

            $('#tblReport').DataTable({
                destroy: true,
                responsive: true,
                autoWidth: false,
                data: data_grades,
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
                columns: columns_table,
                columnDefs: [
                    {
                        targets: '_all',
                        class: 'text-center',
                    },
                ],
                rowCallback: function (row, data, index) {

                },
                initComplete: function (settings, json) {

                },
            });
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
    select_matter = $('select[name="matter"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period.on('change', function () {
        // generateReport();
    });

    select_course.on('change', function () {
        // generateReport();
    });

    select_matter.on('change', function () {
        get_number_activities();
        generateGradeReport();
        // generateReport()
    });

    $('.drp-buttons').hide();


    initTable();


    // $('#tblReport tr').each(function () {
    //     $(this).append('<th>A7</th>');
    // });
});