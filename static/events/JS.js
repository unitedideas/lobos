$(document).ready(function () {
    $("#feedbackform").submit(function (event) {
        event.preventDefault()
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function (response) {
                console.log(response)
                if (response['success']) {
                    $("#feedbackmessage").html("<div class='alert alert-success'>success</div>")
                    $("#feedbackform").addClass("hidden")
                }
                if (response['error']) {
                    $("#feedbackmessage").html("<div class='alert alert-danger'>" +
                        response['error']['comment'] + "</div>")
                }
            },
            error: function (request, status, error) {
                console.log(request.responseText)
            }
        })
    })
})
