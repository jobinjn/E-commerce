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
    console.log("jQuery is working inside functions.js");

    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    console.log("CSRF Token:", csrftoken);
    const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

    $("#reviewForm").submit(function (e) {
        e.preventDefault();
        console.log("Form submitted");

        let dt = new Date();
        let time = dt.getDate() + " " + monthNames[dt.getMonth()] + ", " + dt.getFullYear(); // ✅ Fixed date formatting

        $.ajax({
            url: $(this).attr("action"),
            method: $(this).attr("method"),
            data: $(this).serialize(),
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                console.log("Comment saved to DB", response);

                if (response.bool === true) {
                    $("#review_success").html("Review added Successfully.");

                    // Hide message after 3 seconds
                    setTimeout(function () {
                        $("#review_success").html(""); // Clears the message
                    }, 3000);



                    // ✅ Define `_html` only when response is successful
                    let _html = '<div class="review-container d-flex align-items-start p-3 border-bottom bg-light rounded shadow-sm mb-3">';
                    _html += '<img src="/static/img/avatar.jpg" class="img-fluid rounded-circle me-3" style="width: 60px; height: 60px;" alt="User Avatar">';
                    _html += '<div class="flex-grow-1 review-text">';
                    _html += '<p class="mb-1 text-muted" style="font-size: 14px;">'+ time +'</p>';
                    _html += '<div class="d-flex justify-content-between align-items-center">';
                    _html += '<h5>' + response.context.user + '</h5>';

                    _html += '<div class="d-flex">';
                    for (let i = 1; i <= response.context.ratings; i++) {
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }
                    _html += '</div>';

                    _html += '</div>';
                    _html += '<p>' + response.context.review + '</p>';
                    _html += '</div>';
                    _html += '</div>';


                    // ✅ Prepend the new review to the top of the review section
                    $("#reviews").prepend(_html);

                    // ✅ Reset the form after submission
                    $("#reviewForm")[0].reset();
                } else {
                    $("#review_success").html("Error: Review not added.");
                }

                // ✅ Update the average rating dynamically
                if (response.average_rating) {
                    $("#averageRating").text(`Average Rating: ${response.average_rating.rating.toFixed(1)}`);
                }
            },
            error: function (xhr) {
                console.log("Error:", xhr.responseText);
            }
        });
    });
});
