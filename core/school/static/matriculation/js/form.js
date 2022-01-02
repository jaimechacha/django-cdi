let select_period;
let select_student;
let select_level;
let tblMatter = null;
let fv;
let level_coupons;

const items = {
    details: {
        students: []
    },
    assign_position: function () {
        $.each(this.details.students, function (i, item) {
            item.pos = i;
        });
    },
    list_students: function () {
        this.assign_position()
        tblMatter = $('#tblMatter').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.students,
            ordering: false,
            lengthChange: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "period"},
                {data: "level"},
                {data: "name"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x" aria-hidden="true"></i></a>';
                    },
                },
            ],
            rowCallback: function (row, data, index) {

            },
        })
    },
    add_students: function (item) {
        this.details.students.push(item);
        console.log(this.details.students)
        this.list_students();
    },
}

function getMatters() {

    let parameters = {
        'action': 'search_matters_period',
        'period': select_period.val(),
        'student': select_period.val(),
        'level': select_level.val(),
    };

    if (parameters.period === '' || parameters.level === '') {
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
            {data: "contract.teacher.user.full_name"},
            {data: "contract.job.name"},
            {data: "matter.name"},
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}

function getCoupons() {
    let parameters = {
        'action': 'get_coupons',
        'period': select_period.val(),
        'level': select_level.val(),
    };
    $.post(pathname, parameters, (res) => {
        level_coupons = res.coupons;
        $("#level_coupons").text(res.coupons);
    })
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
                period: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un periodo'
                        },
                    }
                },
                student: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un estudiante'
                        },
                    }
                },
                level: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un nivel'
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
            // let parameters = new FormData($(fv.form)[0]);
            // parameters.append('action', $('input[name="action"]').val());
            // parameters.append('matters', JSON.stringify(tblMatter.rows().data().toArray()));
            // submit_formdata_with_ajax('Alerta', '¿Estas seguro de realizar la siguiente acción?', pathname, parameters, function () {
            //     location.href = fv.form.getAttribute('data-url');
            // });
        });
});

$(function () {

    select_period = $('select[name="period"]');
    select_student = $('select[name="student"]');
    select_level = $('select[name="level"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period
        .on('change', function () {
            fv.revalidateField('period');
        });

    select_student
        .on('change', function () {
            fv.revalidateField('student');
        });

    select_level.on('change', function () {
        fv.revalidateField('level');
        getCoupons()
    });

    if ($('input[name="action"]').val() === 'edit') {
        // getMatters();
    }

    $('#btnRemoveAllStudents').on('click', function () {
        if (items.details.students.length === 0) return false;
        dialog_action(
            'Notificación',
            '¿Estas seguro de eliminar todos los estudiantes de la lista?',
            function () {
                items.details.students = [];
                items.list_students();
            });
    });

    $('#btnAddStudent').on('click', () => {
        fv.revalidateField('period');
        fv.revalidateField('level');
        fv.revalidateField('student');

        fv.validate()
            .then(function (status) {
                if (status === 'Valid') {
                    const std = {
                        id: select_student.val(),
                        name: $("#id_student option:selected").text(),
                        level: $("#id_level option:selected").text(),
                        level_id: select_level.val(),
                        period: $("#id_period option:selected").text(),
                        period_id: select_period.val()
                    }
                    const fnd_student = items.details.students.find(s => s.id === std.id)
                    const fnd_level = items.details.students.find(s => s.level_id !== std.level_id)
                    if (fnd_student) {
                        alert("Estudiante ya ha sido agregado")
                        return
                    }
                    if (fnd_level) {
                        alert("Compruebe que el nivel seleccionado sea el mismo")
                        return;
                    }
                    if (level_coupons === items.details.students.length) {
                        alert("No hay más cupos disponibles para este nivel")
                        return;
                    }
                    items.add_students(std);
                }
            })
    })

    $('#tblMatter tbody')
        .on('change', 'input[name="status"]', function () {
            let tr = tblMatter.cell($(this).closest('td, li')).index(),
                row = tblMatter.row(tr.row).data();
            row.status = this.checked ? 1 : 0;
        }).on('click', 'a[rel="remove"]', function () {
        const td = tblMatter.cell($(this).closest('td, li')).index();
        const row = tblMatter.row(td.row).data();
        items.details.students.splice(row.pos, 1);
        items.list_students();
    });

    $('#btnSubmit').on('click', function () {
        if (items.details.students.length === 0) {
            alert("Agregue al menos un estudiante en la lista")
            return
        }
        submit_post(
            'Alerta',
            pathname,
            {
                'action': $('input[name="action"]').val(),
                'students': JSON.stringify(items.details.students)
            },
            () => {
                location.href = fv.form.getAttribute('data-url');
            }
        )
    });

});