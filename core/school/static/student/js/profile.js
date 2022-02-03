var fv;
var input_birthdate;
var select_parish;
var current_date;
let fvFamily;

let tblFamily;
let family;


let student = {
    details: {
        family: [],
    },
    add_family: function (item) {
        if ($.isEmptyObject(family)) {
            this.details.family.push(item);
        } else {
            this.details.family[family.pos] = item;
        }
        this.list_family();
    },
    list_family: function () {
        $.each(this.details.family, function (i, item) {
            item.pos = i;
        });
        tblFamily = $('#tblFamily').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.family,
            //ordering: false,
            lengthChange: false,
            //searching: false,
            paginate: false,
            columns: [
                {data: "first_name"},
                {data: "last_name"},
                {data: "ci"},
                {data: "relationship"},
                {data: "first_name"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a rel="edit" class="btn btn-warning btn-flat btn-xs"><i class="fa fa-edit fa-1x"></i></a> ';
                        buttons += '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {

            },
        });
    },
}

function validateDate() {
    var now = new Date();
    var input = input_birthdate.val().split('-');
    var birthdate = new Date(input[0], input[1], input[2]);
    return birthdate < now;
}

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
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        // regexp: {
                        //     regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                        //     message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
                        // },
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        // regexp: {
                        //     regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                        //     message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
                        // },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        callback: {
                            message: 'Introduce un número de cédula válido',
                            callback: function (input) {
                                return validate_dni_ruc(input.value) || input.value === '9999999999';
                            }
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de cédula ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="mobile"]').value,
                                    type: 'mobile',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                phone: {
                    validators: {
                        // notEmpty: {},
                        stringLength: {
                            min: 7
                        },
                        digits: {},
                    }
                },
                email: {
                    validators: {
                        // notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El formato email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="email"]').value,
                                    type: 'email',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                address: {
                    validators: {
                        stringLength: {
                            min: 4,
                        },
                        notEmpty: {
                            message: 'Ingrese una dirección',
                        }
                    }
                },
                birthdate: {
                    validators: {
                        callback: {
                            message: 'La fecha de nacimiento debe ser menor a la fecha actual',
                            callback: function (input) {
                                return validateDate();
                            }
                        },
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un genero',
                        },
                    }
                },
                parish: {},
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
            let parameters = new FormData($(fv.form)[0]);

            parameters.append('action', $('input[name="action"]').val());
            parameters.append('family', JSON.stringify(student.details.family));
            parameters['birth_country'] = {
                'id': select_birth_country.val(),
                'name': $("#id_birth_country option:selected").text()
            };
            parameters['birth_province'] = {
                'id': select_birth_province.val(),
                'name': $("#id_birth_province option:selected").text()
            };

            submit_formdata_with_ajax('Alerta',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname, parameters, function () {
                    location.href = fv.form.getAttribute('data-url');
                });
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const frmFamily = document.getElementById('frmFamily');
    fvFamily = FormValidation.formValidation(frmFamily, {
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
                        notEmpty: {
                            message: 'La cédula es obligatoria'
                        },
                        stringLength: {
                            min: 10
                        }
                    }
                },
                age: {},
                relationship: {},
                civil_status: {},
                disability: {},
                disability_type: {},
                cat_illnesses: {},
                cat_illnesses_desc: {},
                academic_training: {},
                occupation: {},
                economic_income: {},
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
            const iconPlugin = fvFamily.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmFamily.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            let parameters = {};
            $.each($(fvFamily.form).serializeArray(), function () {
                parameters[this.name] = this.value;
            });
            parameters['disability'] = (parameters['disability'] === 'True');
            parameters['cat_illnesses'] = (parameters['cat_illnesses'] === 'True');
            student.add_family(parameters);
            $('#myModalFamily').modal('hide');
        });
});

$(function () {

    select_birth_country = $('select[name="birth_country"]');
    select_birth_province = $('select[name="birth_province"]');
    select_civil_status = $('select[name="civil_status"]');
    select_disability_fam = $('#frmFamily select[name="disability"]');
    select_cat_illnesses_fam = $('#frmFamily select[name="cat_illnesses"]');

    current_date = new moment().format("YYYY-MM-DD");
    input_birthdate = $('input[name="birthdate"]');
    select_parish = $('select[name="parish"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="gender"]').on('change.select2', function () {
        fv.revalidateField('gender');
    });

    select_disability_fam.on('change', function () {
        fvFamily.revalidateField('disability');
    });

    $('.btnAddFamily').on('click', function () {
        family = {};
        $('#myModalFamily .modal-title').html('<b><i class="fas fa-plus"></i> Nuevo familiar</b>');
        $('#myModalFamily').modal('show');
    });

    $('#myModalFamily').on('hidden.bs.modal', function () {
        fvFamily.resetForm(true);
        $('input[name="economic_income"]').val(0.00)
    });

    $('#tblFamily tbody')
        .on('click', 'a[rel="remove"]', function () {
            let tr = tblFamily.cell($(this).closest('td, li')).index();
            student.details.family.splice(tr.row, 1);
            student.list_family();
        })
        .on('click', 'a[rel="edit"]', function () {
            let tr = tblFamily.cell($(this).closest('td, li')).index();
            family = tblFamily.row(tr.row).data();
            $(fvFamily.form).find('input[name="first_name"]').val(family.first_name);
            $(fvFamily.form).find('input[name="last_name"]').val(family.last_name);
            $(fvFamily.form).find('input[name="ci"]').val(family.ci);
            $(fvFamily.form).find('input[name="relationship"]').val(family.relationship);
            $(fvFamily.form).find('input[name="age"]').val(family.age);
            $(fvFamily.form).find('input[name="disability_type"]').val(family.disability_type);
            $(fvFamily.form).find('textarea[name="cat_illnesses_desc"]').val(family.cat_illnesses_desc);
            $(fvFamily.form).find('input[name="academic_training"]').val(family.academic_training);
            $(fvFamily.form).find('input[name="occupation"]').val(family.occupation);
            $(fvFamily.form).find('input[name="economic_income"]').val(family.economic_income);
            select_civil_status.val(family.civil_status).trigger('change');
            select_disability_fam.val(family.disability ? "True": "False").trigger('change');
            select_cat_illnesses_fam.val(family.cat_illnesses? "True": "False").trigger('change');
            $('#myModalFamily .modal-title').html('<b><i class="fas fa-edit"></i> Editar datos del familiar</b>');
            $('#myModalFamily').modal('show');
        });

    $('.btnRemoveAllFamily').on('click', function () {
        if (student.details.family.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los familiares asignados?', function () {
            student.details.family = [];
            student.list_family();
        });
    });

    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        maxDate: current_date
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="first_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="last_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="dni"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="phone"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    select_parish.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_parish'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            console.log(e.params.data);
            fv.revalidateField('parish');
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('parish');
        });

});