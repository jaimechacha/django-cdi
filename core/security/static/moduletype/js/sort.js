function get_typemod_position() {
    let data = []
    let list_li = $('#sortable li');
    list_li.each((i, obj) => {
        data.push({id: obj.id, pos: i})
    })
    return data
}

function get_modules_position() {
    let data_modules = []
    const mod_collapse = $('#sortable .collapse')
    mod_collapse.each((i, obj) => {
        $(`#${obj.id} section`).each((e, obj) => {
            data_modules.push({id: obj.id, pos: e})
        })
    })
    return data_modules
}

$(function () {

    $(function () {
        $("#sortable").sortable().disableSelection();
        $('#sortable').sortable({cancel: '.collapse'});
        const mod_collapse = $('#sortable .collapse')
        mod_collapse.each((i, obj) => {
            $(`#${obj.id}`).sortable()
        })
    });

    $('#btnSubmit').on('click', function () {
        const data_typemodules = get_typemod_position();
        const data_modules = get_modules_position();
        submit_post(
            'Alerta',
            pathname,
            {
                'action': $('input[name="action"]').val(),
                'module_types': JSON.stringify(data_typemodules),
                'modules': JSON.stringify(data_modules),
            },
            () => {
                location.href = $('input[name="list_url"]').val();
            }
        )
    });

});