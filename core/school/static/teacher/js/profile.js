let fv;
let input_birthdate;
let select_parish;
let date_current;
let fvCVitae;
let current_date;
let input_enddate;
let input_startdate;

let tblCVitae;
let cvitae;

let teacher = {
    details: {
        cvitae: [],
    },
    add_cvitae: function (item) {
        if ($.isEmptyObject(cvitae)) {
            this.details.cvitae.push(item);
        } else {
            this.details.cvitae[cvitae.pos] = item;
        }
        this.list_cvitae();
    },
    list_cvitae: function () {
        $.each(this.details.cvitae, function (i, item) {
            item.pos = i;
        });

        tblCVitae = $('#tblCVitae').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.cvitae,
            //ordering: false,
            lengthChange: false,
            //searching: false,
            paginate: false,
            columns: [
                {data: "typecvitae.name"},
                {data: "name"},
                {data: "start_date"},
                {data: "end_date"},
                {data: "cv_file.name"},
                {data: "name"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.id && !row.cv_file.file){
                            return `<a target="_blank" href="${row.cv_file.name}">Ver</a>`
                        }
                        return row.cv_file.name
                    }
                },
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
    get_cvitae_ids: function () {
        let ids = [];
        $.each(this.details.cvitae, function (i, item) {
            if (item.id) ids.push(item.id);
        });
        return ids;
    },
}
function validateDate() {r

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
                            message: 'El formato del correo electrónico no es correcto'
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
                            message: 'El correo electrónico ya se encuentra registrado',
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
                            message: 'La dirección es obligatoria'
                        },
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
                profession: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una profesión',
                        },
                    }
                },
                parish: {
                    // validators: {
                    //     notEmpty: {
                    //         message: 'Seleccione una parroquia',
                    //     },
                    // }
                },
                curriculum: {
                    validators: {
                        file: {
                            extension: 'pdf',
                            type: 'application/pdf',
                            message: 'Por favor seleeciona un archivo en formato pdf'
                        }
                    }
                },
            },
        }
    )
        .on('core.form.invalid', function () {
            $('a[href="#home"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
        })
        .on('core.element.validated', function (e) {
            // Validate Tabs
            var tab = e.element.closest('.tab-pane'),
                tabId = tab.getAttribute('id');
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
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
            } else {
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            // Validate Tabs
            var tab = e.element.closest('.tab-pane'),
                tabId = tab.getAttribute('id');
            if (!e.result.valid) {
                // Query all messages
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
                $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
            }
        })
        .on('core.form.valid', function () {
            let parameters = new FormData($(fv.form)[0]);

            parameters.append('action', $('input[name="action"]').val());
            parameters.append('cvitae', JSON.stringify(teacher.details.cvitae));
            parameters.append('cvitae_ids', JSON.stringify(teacher.get_cvitae_ids()));

            teacher.details.cvitae.forEach(e => {
                if (e.cv_file.file){
                    parameters.append(`${ e.pos }`, e.cv_file.file);
                }
            })
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const frmCVitae = document.getElementById('frmCVitae');
    fvCVitae = FormValidation.formValidation(frmCVitae, {
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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        }
                    }
                },
                details: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        }
                    }
                },
                start_date: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                end_date: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                typecvitae: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de vitae'
                        },
                    }
                },
                cv_file: {}
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
            const iconPlugin = fvCVitae.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmCVitae.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            let parameters = {};

            $.each($(fvCVitae.form).serializeArray(), function () {
                parameters[this.name] = this.value;
            });
            parameters['typecvitae'] = {
                'id': select_typecvitae.val(),
                'name': $("#id_typecvitae option:selected").text()
            };
            const cv_file = $('input[name="cv_file"]')[0].files[0];
            if (cv_file) {
                parameters['cv_file'] = { name: cv_file.name, file: cv_file }
            }else {
                if (cvitae.cv_file){
                    parameters['cv_file'] = { name: cvitae.cv_file.name}
                }else {
                    parameters['cv_file'] = { name: 'Vacío'}
                }
            }
            if (cvitae.id) parameters['id'] = cvitae.id
            teacher.add_cvitae(parameters);
            // console.log(teacher.details.cvitae)
            $('#myModalCVitae').modal('hide');
        });
});


$(function () {
    input_birthdate = $('input[name="birthdate"]');
    select_parish = $('select[name="parish"]');

    current_date = new moment().format("YYYY-MM-DD");
    input_enddate = $('input[name="end_date"]');
    input_startdate = $('input[name="start_date"]');
    select_typecvitae = $('select[name="typecvitae"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    input_birthdate.on('change', function () {
        fv.revalidateField('birthdate');
    });

    $('select[name="gender"]').on('change.select2', function () {
        fv.revalidateField('gender');
    });

    $('select[name="profession"]').on('change.select2', function () {
        fv.revalidateField('profession');
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

    /* Curriculum */

    select_typecvitae.on('change', function () {
        fvCVitae.revalidateField('typecvitae');
    });

    input_enddate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        //minDate: current_date
    });

    input_enddate.datetimepicker('date', input_enddate.val());

    input_startdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        //minDate: current_date
    });

    input_startdate.datetimepicker('date', input_startdate.val());

    input_startdate.on('change.datetimepicker', function (e) {
        fvCVitae.revalidateField('start_date');
        input_enddate.datetimepicker('minDate', e.date);
        input_enddate.datetimepicker('date', e.date);
    });

    input_enddate.on('change.datetimepicker', function (e) {
        fvCVitae.revalidateField('end_date');
    });

    $('.btnAddCVitae').on('click', function () {
        input_startdate.datetimepicker('date', current_date);
        input_enddate.datetimepicker('date', current_date);
        cvitae = {};
        $('#myModalCVitae .modal-title').html('<b><i class="fas fa-plus"></i> Nuevo dato de la hoja de vida</b>');
        $('#myModalCVitae').modal('show');
    });

    $('#myModalCVitae').on('hidden.bs.modal', function () {
        fvCVitae.resetForm(true);
    });

    $('#tblCVitae tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblCVitae.cell($(this).closest('td, li')).index();
            teacher.details.cvitae.splice(tr.row, 1);
            teacher.list_cvitae();
        })
        .on('click', 'a[rel="edit"]', function () {
            var tr = tblCVitae.cell($(this).closest('td, li')).index();
            cvitae = tblCVitae.row(tr.row).data();
            $(fvCVitae.form).find('input[name="name"]').val(cvitae.name);
            $(fvCVitae.form).find('textarea[name="details"]').val(cvitae.details);
            $(fvCVitae.form).find('input[name="end_date"]').val(cvitae.end_date);
            $(fvCVitae.form).find('input[name="start_date"]').val(cvitae.start_date);
            select_typecvitae.val(cvitae.typecvitae.id).trigger('change');
            $('#myModalCVitae .modal-title').html('<b><i class="fas fa-edit"></i> Editar dato de la hoja de vida</b>');
            $('#myModalCVitae').modal('show');
        });

    $('.btnRemoveAllCVitae').on('click', function () {
        if (teacher.details.cvitae.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            teacher.details.cvitae = [];
            teacher.list_cvitae();
        });
    });
});