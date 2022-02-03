var select_contract;
var tblMatter = null;

function getMatters() {

    var parameters = {
        'action': 'search_matters_period',
        'contract': select_contract.val()
    };

    if (parameters.contract === '') {
        if (tblMatter !== null) {
            tblMatter.clear().draw();
        }
        return false;
    }

    tblMatter = $('#tblMatter').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "name"},
            {data: "level.name"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    console.log(row);
                    var checked = row.status === 1 ? ' checked' : '';
                    return '<label class="checkbox-inline"><input type="checkbox" name="status" ' + checked + '></label>';
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}

document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
    const fv = FormValidation.formValidation(form, {
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
                            message: 'Seleccione un docente'
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
            var parameters = {};
            parameters['contract'] = select_contract.val();
            parameters['action'] = $('input[name="action"]').val();
            parameters['matters'] = JSON.stringify(tblMatter.rows().data().toArray().filter(function (item, key) {
                return item.status === 1;
            }));
            submit_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
                location.href = fv.form.getAttribute('data-url');
            });
        });
});

$(function () {

    select_contract = $('select[name="contract"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_contract.on('change', function () {
        getMatters();
    });

    $('#tblMatter tbody')
        .on('change', 'input[name="status"]', function () {
            var tr = tblMatter.cell($(this).closest('td, li')).index(),
                row = tblMatter.row(tr.row).data();
            row.status = this.checked ? 1 : 0;
        });

    $('input[name="stateall"]').on('change', function () {
        var status = this.checked;
        var cells = tblMatter.cells().nodes();
        $(cells).find('input[name="status"]').prop('checked', status).change();
    });
});