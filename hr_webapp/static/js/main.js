$(document).ready(function() {
    $('#checkin-table').DataTable( {
        order: [[0, 'desc']],
        responsive: true,
        searching: false,
        select: true,
        // rowGroup: {
        //     dataSrc: 0
        // },
        "aaSorting": [],
        columnDefs: [{
            orderable: false,
            targets: [2, 3, 4]
        }],

        //make it scrollable rather than paged
        scrollY: 500,
        scrollX: true,
        scrollCollapse: true,
        paging: false,

        //increase performance, load faster
        // ajax: json_checkins,
        deferRender: true,

        //calculate total number of hours
        dom: '<"top">rt<"bottom"lfp><"clear">',
        footerCallback: function (row, data, start, end, display) {
            var api = this.api(), data;

            //string to int
            var intVal = function(i) {
                return typeof i === 'string' ?
                    i*1 :
                    typeof i === 'number' ?
                        i:0;
            };

            //total all hours
            totalHours = api
                .column(4)
                .data()
                .reduce( function (a,b) {
                    return intVal(a) + intVal(b);
                }, 0);
            
            //update footer
            $( api.column(4).footer() ).html(
                totalHours
            )
        }
    });

    $(".reset-btn").click(function(){
        $("#search_form").trigger("reset");
        $(':input').val('');
    });
} );