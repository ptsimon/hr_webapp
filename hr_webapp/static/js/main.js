$(document).ready(function() {
    $('#checkin-table').DataTable( {
        order: [[0, 'desc']], //column to order, descending
        responsive: true, //mobile friendly
        searching: false, //disable search bar
        select: true, //enable row selection

        //make it scrollable rather than paged
        scrollY: 400,
        scrollX: true,
        scrollCollapse: true,
        paging: false,

        columnDefs: [
            { 
                //disable sorting of selected columns
                orderable: false, 
                targets: [2, 3, 4] //index of columns
            },
            {
                //change date format (removed time)
                "render": function ( data ) {
                    date_display = data.match(/(\w+(?:[, ])+){4}/gm);
                    
                    return date_display;
                },
                "targets": 0
             }
        ],

        rowGroup: {
            // grouping rows based in their month-year
            dataSrc: function ( row ) {
                var date = row['date'].split(" ");
                var month = date[2];
                var year = date[3];

                //this value is passed as 'group' in the startRender
                return "" + month + ' ' + year; 
            },
            startRender: function ( rows, group ) {
                month = group.split(" ")[0];
                year = group.split(" ")[1];

                // compute total hours for the group(month)
                var totalHours = rows
                    .data()
                    .pluck('hours')
                    .reduce( function (a, b) {
                        console.log(a,b);
                        return a + b*1;
                    }, 0);

                //to address the floating point weirdness
                totalHours = Math.round((totalHours + Number.EPSILON) * 100) / 100;
 
                return $('<tr/>')
                    .append( '<td colspan="3">' + month + ' ' + year + '</td>' )
                    .append( '<td style="text-align:right;">Month Total Hours:</td>')
                    .append( '<td>'+totalHours+'</td>' )
            },
            endRender: null
        },

        //calculate total number of hours
        dom: '<"top">rt<"bottom"lfp><"clear">',
        footerCallback: function (row, data, start, end, display) {
            var api = this.api(), data;

            //total all hours
            totalHours = api
                .column(4)
                .data()
                .reduce( function (a,b) {
                    return a + b*1;
                }, 0);

            //to address the floating point weirdness
            totalHours = Math.round((totalHours + Number.EPSILON) * 100) / 100;
            
            //update footer
            $( api.column(4).footer() ).html(
                totalHours
            )
        },

        //increase performance, load faster
        deferRender: true,
        processing: true,
        serverSide: true,
        ajax: {url: "/data"},
        columns: [
            { data: 'date' },
            { data: 'project_id' },
            { data: 'manager_id' },
            { data: 'user_id' },
            { data: 'hours' }
        ]
    });

    $(".reset-btn").click(function(){
        $("#search_form").trigger("reset");
        $(':input').val('');
    });
} );