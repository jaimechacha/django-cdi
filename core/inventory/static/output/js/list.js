let tblMatDetails;
let out_materials;

const list_output_materials = () => {
    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        const td = table.cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data();
        const id = parseInt(rows[0]);
        tblMatDetails = $('#tblMatDetails').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            searching: false,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    action: 'search_outputs',
                    id
                },
                dataSrc: (data) => {
                    out_materials = data?.map(d => ({ ...d, refund: 0 }));
                    return data
                }
            },
            columns: [
                {data: "material"},
                {data: "description"},
                {data: "amount"},
                {data: "amount"},
            ],
            columnDefs: [
                {
                    targets: [0, 1],
                    render: (data, type, row) => {
                        if(row.amount === 0){
                            return `<p class="text-black-50">${ data }</p>`
                        }
                        return data
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: (data, type, row) => {
                        if(row.amount === 0){
                            return `<p class="text-black-50">${ data } (Devolución)</p>`
                        }
                        return data
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: (data, type, row) => {
                        if(row.amount === 0){
                            return `<input 
                            type="text" 
                            class="form-control input-sm" 
                            autocomplete="off"
                            name="refund"
                            disabled
                            value="0">`
                        }
                        return `<input 
                            type="text" 
                            class="form-control input-sm" 
                            autocomplete="off" 
                            name="refund" 
                            value="0">`;
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                const frm = $(row).closest('tr');

                frm.find('input[name="refund"]').TouchSpin({
                    min: 0,
                    max: data.amount,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
        $('#myModalOutputs').modal('show');
    });
}

const submit_refund_materials = () => {
    $('#submit_refunds').click(() => {
        submit_with_ajax('Notificación',
            '¿Estas seguro de guardar los cambios?',
            pathname,
            {
                'action': 'refund_materials',
                'out_materials': JSON.stringify(out_materials),
            },
            function () {
                alert_sweetalert(
                    'success',
                    'Notificación',
                    'Cambios guardados',
                    ()=>{}
                )
                $('#myModalOutputs').modal('hide');
            },
        );
    })
}

$(function () {
    $('#tblMatDetails tbody')
        .on('change', 'input[name="refund"]', function () {
            const td = tblMatDetails.cell($(this).closest('td, li')).index();
            const row = tblMatDetails.row(td.row).data();
            out_materials.map(om => {
                if (om.id === row.id){ om.refund = parseInt($(this).val()) }
            })
        })
    list_output_materials()
    submit_refund_materials()
});
