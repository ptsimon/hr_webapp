$(document).ready(function() {
    $('#checkin-table').DataTable( {
        order: [[0, 'desc']], //column to order, descending
        responsive: true, //mobile friendly
        searching: false, //disable search bar
        select: true, //enable row selection
        columnDefs: [{ 
            orderable: false, //disable sorting of selected columns
            targets: [2, 3, 4] //index of columns
        }],
        rowGroup: {
            // grouping rows based in their month-year
            dataSrc: function ( row ) {
                var date = row[0].split("-");
                var month = date[1];
                var year = date[0];

                //this value is passed as 'group' in the startRender
                return "" + month + ' ' + year; 
            },
            startRender: function ( rows, group ) {
                month = group.split(" ")[0]*1;
                year = group.split(" ")[1];

                var months = [ "January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December" ];

                var monthName = months[month-1];

                // compute total hours for the group(month)
                var totalHours = rows
                    .data()
                    .pluck(4)
                    .reduce( function (a, b) {
                        return a + b*1;
                    }, 0);

                //to address the floating point weirdness
                totalHours = Math.round((totalHours + Number.EPSILON) * 100) / 100;
 
                return $('<tr/>')
                    .append( '<td colspan="3">' + monthName + ' ' + year + '</td>' )
                    .append( '<td style="text-align:right;">Total Hours:</td>')
                    .append( '<td>'+totalHours+'</td>' )
            },
            endRender: null
        },

        //make it scrollable rather than paged
        scrollY: 400,
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
        }
    });

    $(".reset-btn").click(function(){
        $("#search_form").trigger("reset");
        $(':input').val('');
    });
} );