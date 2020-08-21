$(document).ready(function() {
    $('#checkin-table').DataTable( {

        //to increase performance/load data faster
            //--failed attempt? mabagal pa rin haha :((
        deferRender: true,
        // processing: true,
        // serverSide: true,
        // ajax: {url: "/data"},
        // columns: [
        //     { data: 'date' },
        //     { data: 'project_id' },
        //     { data: 'manager_id' },
        //     { data: 'user_id' },
        //     { data: 'hours' }
        // ],


        aaSorting: [[ 0, "desc" ]], //column to order, descending
        responsive: true, //mobile friendly
        searching: false, //disable search bar
        select: true, //enable row selection

        //make it scrollable
        // scrollY: 500,
        // scrollX: true,
        // scrollCollapse: true,
        paging: false,
        "bInfo" : false,

        columnDefs: [
            { 
                //disable sorting of selected columns
                orderable: false, 
                targets: [2, 3, 4] //index of columns
            },
            {
                // //change date format (removed time)
                // "render": function ( data ) {
                //     date_display = data.match(/(\w+(?:[, ])+){4}/gm);
                    
                //     return date_display;
                // },
                // "targets": 0
             }
        ],

        rowGroup: {
            // grouping rows based in their month-year
            dataSrc: function ( row ) {
                var date = row[0].split("-");
                var month = date[1]*1;
                var year = date[0];

                var months = [ "January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December" ];

                var selectedMonthName = months[month-1];

                //this value is passed as 'group' in the startRender
                return "" + selectedMonthName + ' ' + year; 
            },
            startRender: function ( rows, group ) {
                month = group.split(" ")[0];
                year = group.split(" ")[1];

                // compute total hours for the group(month)
                var totalHours = rows
                    .data()
                    // .pluck('hours')
                    .pluck(4)
                    .reduce( function (a, b) {
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
        // dom: '<"top">rt<"bottom"lfp><"clear">',
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
    });

    $(".reset-btn").click(function(){
        $("#search_form").trigger("reset");
        $(':input').val('');
    });
} );