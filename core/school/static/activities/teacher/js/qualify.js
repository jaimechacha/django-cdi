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
                {data: "archive"},
                {data: "comment"},
                {data: "note"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a target="_blank" href="' + row.archive + '" class="btn btn-primary btn-xs"><i class="fas fa-file-word"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="note" value="' + row.note + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
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

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                {
                    'action': 'qualify',
                    'activities': JSON.stringify(activities.details)
                },
                function () {
                    location.href = fv.form.getAttribute('data-url');
                },
            );
        });
});


$(function () {

    $('#tblActivities tbody')
        .on('change', 'input[name="note"]', function () {
            var tr = tblActivities.cell($(this).closest('td, li')).index();
            activities.details.homework[tr.row].note = parseInt($(this).val());
        })
        .on('keyup', 'input[name="comment"]', function () {
            var tr = tblActivities.cell($(this).closest('td, li')).index();
            activities.details.homework[tr.row].comment = $(this).val();
        });
});