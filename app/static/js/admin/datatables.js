$(document).ready(function() {
    $('table').each(function(){
        $(this).DataTable({
            "dom": "<'row'<'col-sm-12 col-md-6 flex-d align-items-start'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-7'p>>",
            "iDisplayLength":5,
            "lengthChange": false,
            "ordering": false,
            "info": false,
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.11.3/i18n/es_es.json"
            }
        });
    });
} );
