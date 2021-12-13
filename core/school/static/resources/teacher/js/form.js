var fv;
var input_daterange;
var select_perioddetail;

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
                date_range: {
                    validators: {
                        notEmpty: {},
                    }
                },
                period: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un periodo'
                        },
                    }
                },
                typeresource: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de recurso'
                        },
                    }
                },
                perioddetail: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una materia'
                        },
                    }
                },
                desc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                web_address: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {

    select_perioddetail = $('select[name="perioddetail"]');
    input_daterange = $('input[name="date_range"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        }).on('change', function (ev, picker) {
        fv.revalidateField('date_range');
    });

    $('select[name="period"]')
        .on('change.select2', function () {
            var id = $(this).val();
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_matters',
                    'period': id
                },
                method: 'POST',
                dataType: 'json',
                success: function (request) {
                    if (!request.hasOwnProperty('error')) {
                        select_perioddetail.html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: request
                        });
                        return false;
                    }
                    message_error(request.error);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
            fv.revalidateField('period');
        });

    select_perioddetail
        .on('change', function () {
            fv.revalidateField('perioddetail');
        });

    $('select[name="typeresource"]')
        .on('change.select2', function () {
            fv.revalidateField('typeresource');
        });

    $('.drp-buttons').hide();
});
