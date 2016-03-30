$(document).ready(function(){

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    if ($(".requestsTable").length) {

        function sendViews(requests) {
            $.ajax({
                method: "post",
                url: "/requests/ajaxrequests/",
                data: {'data':JSON.stringify(requests)}
            });
        }

        function fillData(data) {
            var compiledRow = _.template(
                "<tr class=<%=bold_class%>>" +
                "<td><%=date%></td>" +
                "<td><%=method%></td>" +
                "<td><%=path%></td>" +
                "<td><%=server_protocol%></td> " +
                "<td><%=ip_addr%></td> " +
                "<td><%=priority%></td> " +
                "</tr>");
            var rows = '';
            data['ajaxrequests'].forEach(function (item) {
                var row = compiledRow({
                    date: item['date'],
                    method: item['method'],
                    path: item['path'],
                    server_protocol: item['server_protocol'],
                    ip_addr: item['ip_addr'],
                    priority: item['priority'],
                    bold_class: item['viewed'] == false ? 'bold-font' : '',
                });
                rows += row;
            });

            $('.requestsTable').html(rows);

            if (data['new_requests']){
                $('.requests').text('(' + data['new_requests'] + ') new requests');
                document.title = '(' + data['new_requests'] + ') new requests';
            }else{
                $('.requests').text('Last 10 Requests');
                document.title = 'Last 10 Requests';
            }
        }

        var requests = [];
        function fillRequests() {

            $.ajax({
                method: "get",
                url: "/requests/ajaxrequests/"
            }).done(function (data) {
                fillData(data);
                requests = data['ajaxrequests'];
                if (wasRequestsViewed()) {
                    sendViews(requests);
                }

            });
        }

        function wasRequestsViewed(){
            return document.visibilityState=='visible';
        }

        fillRequests();
        setInterval(fillRequests, 5000); //5 sec delay

    }


    if ($("#edit_form").length) {
         $( ".datepicker" ).datepicker({
           changeMonth: true,
           changeYear: true,
           yearRange: "1900:2026",
           dateFormat: 'yy-mm-dd',
         });
         $('#ajax_loader').hide();
         $('#message').hide();


         function show_enable() {
             $('#message').show();
             $('#ajax_loader').show();
             formElementsEnableDisable(true);
         }


         function showSuccess() {
             show_enable();
             $('#message').text('Info has been sucessfully changed!').attr('class', 'alert alert-success');
         }


         function showErrors(responseText) {
             show_enable();

             var errors_message = responseText.responseJSON
             var errors = []
             for (var key in errors_message){
                 errors += errors_message[key] + " "
             }

             $('#message').text('Oops! Something is wrong:) ' + errors).attr('class', 'alert alert-danger');

         }

        var options = {
             success: showSuccess,
             error: showErrors,
         };

         function formElementsEnableDisable(enable){
             if (enable){
                setTimeout(function(){
                    $("#edit_form :input").prop('disabled', false);
                }, 1000)
                $('#message').delay(5000).hide(0);
                $('#ajax_loader').delay(1000).hide(0);
             }else{
                $("#edit_form :input").prop('disabled', true);

             }
         }


        $('#edit_form').submit(function () {
            $(this).ajaxSubmit(options);
            formElementsEnableDisable(false);
            return false
        });

        function readURL(input) {

            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#preview').attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
            }
        }
        $(document).on('change', '#id_photo', function(){
            readURL(this);
        });
        

    }
    
});



$('.index').each(function(){
   $(this).html( $(this).html().replace(/((http|https|ftp):\/\/[\w?=&.\/-;#~%-]+(?![\w\s?&.\/;#~%"=-]*>))/g, '<a target="_blank" href="$1">$1</a> ') );
});

