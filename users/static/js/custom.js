function showPassword() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function showPassword1() {
    var x = document.getElementById("password1");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
};

$(document).ready(function() {
    $('.nice-select').hide()
    $('select').show()
        //console.log('present')
    $('#country_name').focusout(function() {
        //console.log('working')
        $('#city_name').empty();
        var selectedCountryId = $('#country_name option:selected').val()
        console.log(selectedCountryId)
        $.ajax({
            url: '/users/get_city_by_country/',
            data: {
                'selected_country_id': selectedCountryId
            },
            dataType: 'json',
            success: function(cities) {
                $('#city_name').append(cities.data)
            }
        })
    });

    // load more projects
    $("#load_more").on("click", function(e) {
        e.preventDefault();
        var _currentPreojects = $(".project-box").length;
        var _limit = $(this).attr("data-limit");
        var _total = $(this).attr("data-total");
        // start ajax
        $.ajax({
            url: "/users/load_more_project/",
            data: {
                limit: _limit,
                offset: _currentPreojects,
            },
            dataType: "json",
            beforeSend: function() {
                $("#load_more").attr("disabled", true);
                $(".load-more-icon").addClass("fa-spinner");
            },
            success: function(res) {
                $(".project-cards").append(res.data);
                $("#load_more").attr("disabled", false);
                $(".load-more-icon").removeClass("fa-spinner");

                if (_currentPreojects == _total) {
                    $("#load_more").remove();
                    $(".project_end").show();
                }
            },
        });
        // end ajax
    });
})