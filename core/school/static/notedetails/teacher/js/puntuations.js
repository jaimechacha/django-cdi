var tblActivities;
var activities = {
    details: {
        homework: []
    },

    list: function () {
        tblActivities = $('#tblActivities').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.homework,

            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "student.user.full_name"},
                {data: "comment"},
                {data: "note"},
                {data: "evidence_doc"},
            ],
            columnDefs: [
                ///{
                // targets: [-3],
                //class: 'text-center',
                //render: function (data, type, row) {
                //return '<a target="_blank" href="' + row.archive + '" class="btn btn-primary btn-xs"><i class="fas fa-file-word"></i></a>';
                //console.log(data)
                //return data => `<select>${['fruit', 'vegie', 'berry'].reduce((options, item) => options+='<option value="'+item+'" '+(item == data ? 'selected' : '')+'>'+item+'</option>', '<option value=""></option>')}</select>`
                //}
                //},
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.exists_doc){
                            return `<a href="${row.evidence_doc}" target="_blank">Ver archivo</a>`
                        }
                        return '<input class="form-control form-control-sm" type="file" autocomplete="off" name="evidence_doc" id="' + row.id + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data >= 9) {
                            //var html = '<span class="badge bg-warning">&nbsp;&nbsp;'+data+'&nbsp;&nbsp;</span>'   style="background-color:#FFFF00;color:white;"
                            var html = '<input type="text" class="form-control input-sm is-valid" autocomplete="off" name="note" value="' + row.note + '">';
                            return html;
                        } else if (data >= 7 && data < 9) {
                            var html = '<input type="text" class="form-control input-sm is-warning" autocomplete="off" name="note" value="' + row.note + '">';
                            return html;
                        } else if (data < 7) {
                            var html = '<input type="text" class="form-control input-sm is-invalid" autocomplete="off" name="note" value="' + row.note + '">';
                            return html;
                        } else {
                            return '<input type="text" class="form-control input-sm" autocomplete="off" name="note" value="' + row.note + '">';
                            ;
                        }

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        //return '<select size="1" id="row-1-office" name="note"><option value="Edinburgh" selected="selected">' + row.note + '</option><option value="London">Excelente</option></select>';
                        return '<input class="form-control input-sm" placeholder="Ingrese un comentario" autocomplete="off" name="comment" value="' + row.comment + '">';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="note"]')
                    .TouchSpin({
                        min: 0.00,
                        max: 10,
                        step: 0.01,
                        decimals: 2,
                        boostat: 5,
                        verticalbuttons: true,
                        maxboostedstep: 10,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    }


};

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
    const fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {},
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

            if (activities.details.homework.length === 0) {
                message_error('Debe tener al menos un item en el detalle');
                return false;
            }

            let parameters = new FormData();
            parameters.append('action', 'punctuation');
            parameters.append('notedetails', JSON.stringify(activities.details));
            $.each($("input[type=file]"), function (i, obj) {
                $.each(obj.files, function (j, file) {
                    parameters.append(`[${ obj.id }]`, file);
                })
            });

            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                },
            );
        });
});


$(function () {

    $('#tblActivities tbody')
        .on('keyup', 'input[name="note"]', function () {
            let tr = tblActivities.cell($(this).closest('td, li')).index();
            //activities.details.homework[tr.row].note = parseInt($(this).val());
            activities.details.homework[tr.row].note = $(this).val();
        })
        .on('change', 'input[name="comment"]', function () {
            let tr = tblActivities.cell($(this).closest('td, li')).index();
            activities.details.homework[tr.row].comment = $(this).val();
        })
});

/* 
$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    console.log('iiiiiii')
    $('select[name="note"]').select2({
        
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'detalles_orden',
                'id': data.peticion,
            },
            
            processResults: function (data) {
                console.log(data);
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un nombre',
        minimumInputLength: 1,
        //llamamos a la funcion que contiene el html para presentar los datos
        templateResult: formatRepo,
        
    });
});
 */