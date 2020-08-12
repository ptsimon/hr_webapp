$(document).ready(function() {
    $('#checkin-table').DataTable( {
        searching: false,
        select: true,
        responsive: true,
        order: [[0, 'desc']],
        // rowGroup: {
        //     dataSrc: 0
        // },
        "aaSorting": [],
        columnDefs: [{
            orderable: false,
            targets: [2, 3, 4]
        }],

    });
} );