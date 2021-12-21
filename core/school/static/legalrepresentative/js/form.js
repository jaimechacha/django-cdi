let fv;

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
                student: {
                    validators: {
                        notEmpty: {message: "Seleccione un estudiante"},
                    }
                },
                first_name: {
                    validators: {
                        notEmpty: {},
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                    }
                },
                ci: {
                    validators: {
                        notEmpty: {},
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
            $.confirm({
                theme: 'material',
                title: 'Confirmación',
                icon: 'fas fa-info-circle',
                content: '¿Esta seguro de realizar la siguiente acción?',
                columnClass: 'small',
                typeAnimated: true,
                cancelButtonClass: 'btn-primary',
                draggable: true,
                dragWindowBorder: false,
                buttons: {
                    info: {
                        text: "Si",
                        btnClass: 'btn-primary',
                        action: function () {
                            $('#frmForm').submit()
                        }
                    },
                    danger: {
                        text: "No",
                        btnClass: 'btn-red',
                    },
                }
            });
        });
});

$(function () {
    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_student = $('select[name="student"]');
    select_student.on('change', function () {
        fv.revalidateField('student');
    });
});