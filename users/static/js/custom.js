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
    })
})