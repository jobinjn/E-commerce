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


//$(document).ready(function () {
//    console.log("jQuery is working inside function.js");
//
//    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
//    console.log("CSRF Token:", csrftoken);
//
//    $("#reviewForm").submit(function (e) {
//        e.preventDefault();
//        console.log("Form submitted");
//
//        $.ajax({
//            url: $(this).attr("action"),
//            method: $(this).attr("method"),
//            data: $(this).serialize(),
//            headers: {
//                "X-CSRFToken": csrftoken
//            },
//            success: function (response) {
//                console.log("Comment saved to DB", response);
//
//                // ✅ Append the new review to the reviews section
//                $("#reviews").append(`
//                    <p><strong>${response.avg.user}</strong>: ${response.avg.review} (Rating: ${response.avg.ratings})</p>
//                `);
//
//                // ✅ Update the average rating
//                $("#averageRating").text(`Average Rating: ${response.average_rating.rating.toFixed(1)}`);
//
//                    if (response.bool == true) {
//                        $("#review_success").html("Review added Successfully.");
//
//                        let _html = '<div class="d-flex">';
//                        _html += '<img src="/static/img/avatar.jpg" class="img-fluid rounded-circle p-3" style="width: 100px; height: 100px;" alt="User Avatar">';
//                        _html += '<div class="">';
//                        _html += '<p class="mb-2" style="font-size: 14px;">Just Now</p>'; // No template tags inside JS
//                        _html += '<div class="d-flex justify-content-between">';
//                        _html += '<h5>' + response.context.user + '</h5>';
//                        _html += '<div class="">';
//                        for (let i = 1; i <= response.context.ratings; i++) {
//                            _html += '<i class="fas fa-star text-warning"></i>';
//                        }
//                        _html += '</div>';
//
//                        _html += '</div>';
//                        _html += '<p>' + response.context.review + '</p>';
//                        _html += '</div>';
//                        _html += '</div>';
//
//                        // Append the new review to the review section
//                        $("#reviews").prepend(_html);
//
//                        // ✅ Reset the form after submission
//
//                    }
//                    $("#reviewForm").reset();
//
//
//
//            },
//            error: function (xhr) {
//                console.log("Error:", xhr.responseText);
//            }
//        });
//    });
//});
//

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
            headers: { "X-CSRFToken": csrftoken },
            success: function (response) {
                console.log("API Response:", response);

                if (response.bool) {
                    if (!response.context || !response.context.user) {
                        console.error("Invalid response data:", response);
                        return;
                    }

                    $("#review_success").html("Review added successfully.");

                    let _html = `
                        <div class="d-flex">
                            <img src="/static/img/avatar.jpg" class="img-fluid rounded-circle p-3" style="width: 100px; height: 100px;" alt="User Avatar">
                            <div>
                                <p class="mb-2" style="font-size: 14px;">Just Now</p>
                                <div class="d-flex justify-content-between">
                                    <h5>${response.context.user}</h5>
                                    <div>
                                        ${"★".repeat(response.context.ratings)}
                                    </div>
                                </div>
                                <p>${response.context.review}</p>
                            </div>
                        </div>`;

                    $("#reviews").prepend(_html);
                    $("#reviewForm")[0].reset();
                }
            },
            error: function (xhr) {
                console.log("Error:", xhr.responseText);
            }
        });
    });
});
