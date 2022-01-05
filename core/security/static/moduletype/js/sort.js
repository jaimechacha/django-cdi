function load_data() {
    let data = []
    let list_li = $('#sortable li');
    list_li.each((i, obj) => {
        data.push({id: obj.id, pos: i})
    })
    return data
}

$(function () {

    $(function () {
        $("#sortable").sortable();
    });

    $('#btnSubmit').on('click', function () {
        let data = load_data()
        submit_post(
            'Alerta',
            pathname,
            {
                'action': $('input[name="action"]').val(),
                'module_types': JSON.stringify(data)
            },
            () => {
                location.href = $('input[name="list_url"]').val();
            }
        )
    });

});