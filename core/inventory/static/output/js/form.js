let input_date;
let fv;
let select_teacher;
let tblMaterials;

const items = {
    details :{
        date_output: '',
        materials: [],
    },
    assign_position: function () {
        $.each(this.details.materials, function (i, item) {
            item.pos = i;
        });
    },
    list_materials: function () {
        this.assign_position()
        tblMaterials = $('#tblMaterials').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.materials,
            ordering: false,
            lengthChange: false,
            paginate: false,
            columns: [
                {data: "material.id"},
                {data: "material.name"},
                {data: "cantidad"},
                {data: "stock"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x" aria-hidden="true"></i></a>';
                    },
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '';
                        }
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cantidad" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center'
                }
            ],
            rowCallback: function (row, data, index) {
                const frm = $(row).closest('tr');

                frm.find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        })
    },
    get_materials_ids: function () {
        let ids = [];
        $.each(this.details.materials, function (i, item) {
            ids.push(item.material.id);
        });
        return ids;
    },
    add_materials: function (item) {
        this.details.materials.push(item);
        this.list_materials();
    },
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
                date_output: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
                teacher: {
                    validators: {
                        notEmpty: {
                            message: 'El campo no puede estar vacío'
                        },
                    }
                },
                num_doc: {
                    validators: {
                        notEmpty: {
                            message: 'El campo no puede estar vacío'
                        },
                    }
                }
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
            const url_refresh = form.getAttribute('data-url');

            items.details.date_output = $('input[name="date_output"]').val();

            if (items.details.materials.length === 0) {
                message_error('Debe tener al menos un material seleccionado');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de guardar la siguiente compra?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'items': JSON.stringify(items.details),
                    'teacher': $('#id_teacher').val(),
                    'num_doc': $('input[name="num_doc"]').val(),
                },
                function () {
                    location.href = url_refresh;
                },
            );
        });
});

$(function () {

    input_date = $('input[name="date_output"]');
    current_date = new moment().format("YYYY-MM-DD");

    input_date.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        maxDate: current_date
    });

    input_date.datetimepicker('date', input_date.val());

    input_date.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_output');
    });

    $("#search_material").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_material',
                    'term': request.term,
                    'materials': JSON.stringify(items.get_materials_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cantidad = 1;
            ui.item.state = true;
            items.add_materials(ui.item);
            $(this).val('').focus();
        }
    });

    $('#clearSearchMaterial').on('click', function () {
        $('#search_material').val('').focus();
    });

    $('#btnRemoveAllMaterials').on('click', function () {
        if (items.details.materials.length === 0) return false;
        dialog_action(
            'Notificación',
            '¿Estas seguro de eliminar todos los productos de tu detalle?',
            function () {
            items.details.materials = [];
            items.list_materials();
        });
    });

    $('#tblMaterials tbody')
        .on('change', 'input[name="cantidad"]', function () {
            const td = tblMaterials.cell($(this).closest('td, li')).index();
            const row = tblMaterials.row(td.row).data();
            items.details.materials[row.pos].cantidad = $(this).val();
        }).on('click', 'a[rel="remove"]', function () {
            const td = tblMaterials.cell($(this).closest('td, li')).index();
            const row = tblMaterials.row(td.row).data();
            items.details.materials.splice(row.pos, 1);
            items.list_materials();
        });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });
});
