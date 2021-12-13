var fv;
var select_contract;
var select_typeevent;
var input_datepermit;
var form_group;

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
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
                contract: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un contrato'
                        },
                    }
                },
                typeevent: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de permiso'
                        },
                    }
                },
                date_permit: {
                    validators: {
                        notEmpty: {},
                    }
                },
                desc: {
                    validators: {}
                },
                valor: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
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
            var parameters = {};
            $.each($(form).serializeArray(), function () {
                parameters[this.name] = this.value;
            });

            parameters['start_date'] = input_datepermit.data('daterangepicker').startDate.format('YYYY-MM-DD');
            parameters['end_date'] = input_datepermit.data('daterangepicker').endDate.format('YYYY-MM-DD');
            parameters['start_time'] = input_datepermit.data('daterangepicker').startDate.format('HH:mm');
            parameters['end_time'] = input_datepermit.data('daterangepicker').endDate.format('HH:mm');

            submit_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {

    select_contract = $('select[name="contract"]');
    select_typeevent = $('select[name="typeevent"]');
    input_datepermit = $('input[name="date_permit"]');
    form_group = document.getElementsByClassName('form-group');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_contract.on('change', function () {
        fv.revalidateField('contract');
    });

    select_typeevent.on('change', function () {
        fv.revalidateField('typeevent');

        var id = $(this).val();
        if (id === '') {
            return false;
        }

        $.ajax({
            url: pathname,
            data: {
                'action': 'search_typeevent',
                'id': id
            },
            method: 'POST',
            dataType: 'json',
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    console.log(request);
                    $(form_group[4]).show();
                    if (!request.economic_sanction) {
                        $(form_group[4]).hide();
                    }
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    });

    $('.applyBtn').hide();

    input_datepermit
        .daterangepicker({
            language: 'auto',
            //startDate: new Date(),
            timePicker: true,
            timePicker24Hour: true,
            timePickerIncrement: 30,
            locale: {
                format: 'YYYY-MM-DD HH:mm',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            fv.revalidateField('date_permit');
        });

    $('input[name="valor"]')
        .TouchSpin({
            min: 0.01,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: '$'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('valor');
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    if ($('input[name="action"]').val() === 'add') {
        $(form_group[4]).hide();
    } else {
        select_typeevent.trigger('change');
    }
});
