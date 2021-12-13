var select_period;
var tblMatter;

function getData() {
    tblMatter = $('#tblMatter').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_period',
                'period': select_period.val()
            },
            dataSrc: ""
        },
        columns: [
            {data: "matter.name"},
            {data: "matter.level.name"},
            {data: ""},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="students" class="btn btn-success btn-xs btn-flat"><i class="fas fa-user-friends"></i></a> ';
                    buttons += '<a rel="notedetails" class="btn btn-info btn-xs btn-flat"><i class="fas fa-book"></i></a> ';
                    buttons += '<a href="/school/notedetails/teacher/add/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="far fa-plus-square"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    select_period = $('select[name="period"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_period
        .on('change.select2', function () {
            getData();
        });

    $('#tblMatter tbody').on('click', 'a[rel="students"]', function () {
        $('.tooltip').remove();
        var tr = tblMatter.cell($(this).closest('td, li')).index(),
            rows = tblMatter.row(tr.row).data();
        $('#tblStudents').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_students',
                    'id': rows.id
                },
                dataSrc: ""
            },
            columns: [
                {data: "student.user.full_name"},
                {data: "student.user.dni"},
                {data: "student.mobile"},
                {data: "student.user.email"},
            ],
            columnDefs: []
        });
        $('#myModalStudents').modal('show');
    });

    $('#tblMatter tbody').on('click', 'a[rel="notedetails"]', function () {
        $('.tooltip').remove();
        var tr = tblMatter.cell($(this).closest('td, li')).index(),
            rows = tblMatter.row(tr.row).data();
        tbl = $('#tblNotedetails').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_notedetails',
                    'id': rows.id,
                    'matter_id': rows.matter.id
                },
                dataSrc: ""
            },
            columns: [
                {data: "typeactivity.name"},
                {data: "name"},
                {data: "desc"},
                {data: "perioddetail.matter.name"},
                {data: ""},
                
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/school/notedetails/teacher/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/school/notedetails/teacher/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';                    
                        buttons += '<a href="/school/notedetails/teacher/puntuations/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-sticky-note"></i></a> ';
                        buttons += '<a rel="notes" class="btn btn-info btn-xs btn-flat"><i class="fas fa-book-open"></i></a> '; 
                        return buttons;
                    }
                },
            ]
        });
        $('#myModalNotedetails').modal('show')
        .on('shown.bs.modal', function (e) {
            if ('#myModalNotedetails:visible') return e.preventDefault()
            $('#myModalNotes').on('shown');
            //$(this).off('hidden.bs.modal'); // Remove the 'on' event binding
        });
    });

    $('#tblNotedetails tbody').on('click', 'a[rel="notes"]', function () {
        $('.tooltip').remove();
        var tr = tbl.cell($(this).closest('td, li')).index(),
            rows = tbl.row(tr.row).data();
        $('#tblNotes').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_punctuations',
                    'id': rows.id
                },
                dataSrc: ""
            },
            columns: [
                {data: "student.user.full_name"},
                {data: "comment"},
                {data: "note"},
                {data: "score.name"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center ',
                    orderable: false,
                    render: function (data, type, row) {
    
                        
                        if (data >= 9 ) {
                            var html = '<span class="badge bg-light">&nbsp;&nbsp;&nbsp;'+data+'&nbsp;&nbsp;&nbsp;</span>'
                            return html;
                        } else if (data === 'Medio') {
                            var html = '<span class="badge bg-gray">&nbsp;'+data+'&nbsp;</span>'
                            return html;
                        } else if (data === 'Alto') {
                            var html = '<span class="badge bg-dark">&nbsp;&nbsp;&nbsp;'+data+'&nbsp;&nbsp;&nbsp;</span>'
                            return html;
                        } 
                        else{
                            return data;
                        }
                       
                    }
                },
            ]
        });
        $('#myModalNotes').modal('show');
    });
});


