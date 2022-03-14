$(function () {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        const td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        const id = parseInt(rows[0]);
        $('#tblMatDetails').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    action: 'search_outputs', id: id
                },
                dataSrc: ""
            },
            columns: [
                {data: "material"},
                {data: "description"},
                {data: "amount"},
                {data: "amount"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<b>'+data+'</b>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: (data, type, row) => {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cantidad" value="' + row.amount + '">';
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                const frm = $(row).closest('tr');

                frm.find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.amount,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
        $('#myModalOutputs').modal('show');
    });
});
