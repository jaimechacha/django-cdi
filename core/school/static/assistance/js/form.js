var tblAssistance = null;
var input_datejoined;
var fv;
var select_period;
console.log('check point');
function generate_assistance() {
    var parameters = {
        'action': 'generate_assistance',
        'period': select_period.val(),
        'date_joined': input_datejoined.val()
    };

    if (parameters.period === '') {
        if (tblAssistance !== null) {
            tblAssistance.clear().draw();
        }
        return false;
    }

    tblAssistance = $('#tblAssistance').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        ordering: false,
        lengthChange: false,
        paging: false,
        columns: [
            {data: "user.full_name"},
            {data: "user.dni"},
            {data: "user.email"},
            {data: "desc"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
                data: null,
                class: 'text-center',
                render: function (data, type, row) {
                    return '<input type="text" name="desc" style="width: 100%;" class="form-control form-control-sm" placeholder="Ingrese una descripción" value="' + data + '" autocomplete="off">';
                }
            },
            {
                targets: [-1],
                data: null,
                class: 'text-center',
                render: function (data, type, row) {
                    var attr = row.state === 1 ? ' checked' : '';
                    return '<input type="checkbox" name="chkstate" class="check" ' + attr + '>';
                }
            },
        ],
        rowCallback: function (row, data, index) {
            var tr = $(row).closest('tr');
            var background = data.state === 0 ? '#fff' : '#fff0d7';
            $(tr).css('background', background);
        },
        initComplete: function (settings, json) {

        },

    });
}

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmAssistance');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="date_joined"]').value,
                                    action: 'validate_data'
                                };
                            },
                            message: 'La fecha de asistencia ya esta registrada',
                            method: 'POST'
                        }
                    }
                },
                period: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un periodo'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {

            var assistance = tblAssistance.rows().data().toArray();
            console.log(assistance);
            console.log('check point');
            //var yt = 'yyyyyy';
            if (assistance.length === 0) {
                message_error('Debe tener al menos un empleado en el listado de asistencias');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de guardar el siguiente registro?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'date_joined': input_datejoined.val(),
                    'items': JSON.stringify(assistance)
                    //'yest' : yt
                },
                function () {
                    location.href = fv.form.getAttribute('data-url');
                }
            );
        });
});

$(function () {

    select_period = $('select[name="period"]');

    $('#tblAssistance tbody')
        .on('change', 'input[name="chkstate"]', function () {
            var tr = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(tr.row).data();
            row.state = this.checked ? 1 : 0;
            var background = !this.checked ? '#fff' : '#fff0d7';
            $(tblAssistance.row(tr.row).node()).css('background', background);
        })
        .on('keyup', 'input[name="desc"]', function () {
            var tr = tblAssistance.cell($(this).closest('td, li')).index(),
                row = tblAssistance.row(tr.row).data();
            row.desc = $(this).val();
        });

    $('input[type="checkbox"][name="chkstateall"]').on('change', function () {
        var state = this.checked;
        if (tblAssistance !== null) {
            var cells = tblAssistance.cells().nodes();
            $(cells).find('input[type="checkbox"][name="chkstate"]').prop('checked', state).change();
        }
    });

    input_datejoined = $('input[name="date_joined"]');

    input_datejoined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        //minDate: new moment().format("YYYY-MM-DD")
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        fv.validateField('date_joined').then(function (status) {
            if (status === 'Valid') {
                generate_assistance();
            } else if (tblAssistance !== null) {
                tblAssistance.clear().draw();
            }
        });
    });

    input_datejoined.trigger('change');

    //generate_assistance();

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period
        .on('change.select2', function () {
            generate_assistance();
            fv.revalidateField('period');
        });
});