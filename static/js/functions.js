console.log("working fine");

//
//$("#reviewForm").submit(function(e){
//    e.preventDefault();
//
//    $.ajax({
//        date:$(this).serialize(),
//
//        method:$(this).attr("method"),
//
//        url: $(this).attr("action"),
//
//        dataType :"json",
//
//        success: function(response){
//        console.log("comment saved to db")
//        }
//
//    })
//})
$(document).ready(function () {
    console.log("jQuery is working inside function.js");

    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    console.log("CSRF Token:", csrftoken);

    $("#reviewForm").submit(function (e) {
        e.preventDefault();
        console.log("Form submitted");

        $.ajax({
            url: $(this).attr("action"),
            method: $(this).attr("method"),
            data: $(this).serialize(),
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                console.log("Comment saved to DB", response);

                // ✅ Append the new review to the reviews section
                $("#reviews").append(`
                    <p><strong>${response.avg.user}</strong>: ${response.avg.review} (Rating: ${response.avg.ratings})</p>
                `);

                // ✅ Update the average rating
                $("#averageRating").text(`Average Rating: ${response.average_rating.rating.toFixed(1)}`);

                    if (response.bool == true){
                        $("#review_success").html("Review added Successfully.           ")
                    }



            },
            error: function (xhr) {
                console.log("Error:", xhr.responseText);
            }
        });
    });
});
