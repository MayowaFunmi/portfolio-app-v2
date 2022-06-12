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
// social media share

/*
    Social Share links:

    Whatsapp:
    https://api.whatsapp.com/send?text=[post-title] [post-url]

    Facebook:
    https://www.facebook.com/sharer.php?u=[post-url]

    Twitter:
    https://twitter.com/share?url=[post-url]&text=[post-title]&via=[via]&hashtags=[hashtags]

    Email:
    $email = 'mailto:?subject=' . $[post-title] . '&body=Check out this site: '. $[post-url] .'" title="Share by Email';

    LinkedIn
    https://www.linkedin.com/shareArticle?url=[post-url]&title=[post-title]

    Telegram
    https://t.me/share/url?url={url}&text={text}

*/
const facebookBtn = document.querySelector('.facebook-btn')
const twitterBtn = document.querySelector('.twitter-btn')
const whatsappBtn = document.querySelector('.whatsapp-btn')
const linkedinBtn = document.querySelector('.linkedin-btn')
const telegramBtn = document.querySelector('.telegram-btn')

function init() {
    let postUrl = encodeURI(document.location.href)
    let postTitle = encodeURI('Read this post from Akinade Mayowa blog: ')

    facebookBtn.setAttribute('href', `https://www.facebook.com/sharer.php?u=${postUrl}`)
    twitterBtn.setAttribute('href', `https://twitter.com/share?url=${postUrl}&text=${postTitle}`)
    whatsappBtn.setAttribute('href', `https://api.whatsapp.com/send?text=${postTitle} ${postUrl}`)
    linkedinBtn.setAttribute('href', `https://www.linkedin.com/shareArticle?url=${postUrl}&title=${postTitle}`)
    telegramBtn.setAttribute('href', `https://t.me/share/url?url=${postUrl}&text=${postTitle}`)
}

$(document).ready(function() {
    $('.nice-select').hide()
    $('select').show()
        //console.log('present')
    $('#country_name').focusout(function() {
        //console.log('working')
        $('#city_name').empty();
        var selectedCountryId = $('#country_name option:selected').val()
            //console.log(selectedCountryId)
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


    // weather form
    $('form#weather_form').on('submit', function(e) {
        e.preventDefault()
        var city = $('input[name="room_name"]').val()
        var result_page = $('#result_page')
            // ajax call
        $.ajax({
            url: "/weather/weather_details/",
            data: {
                'city': city
            },
            dataType: 'json',
            beforeSend: function() {
                $("#btn_send").text('Fetching Weather Data...');
                $("#btn_send").attr("disabled", true);
                $("#btn_send").css('cursor', 'not-allowed');
            },
            success: function(detail) {
                $('#result_page').empty()
                var weather_detail = detail
                result_page.append(`
                    <div>
                        <h2 class="contact-title">City Name: ${city}</h2>
                        <h3>Latitude: ${weather_detail.latitude}</h3>
                        <h3>longitude: ${weather_detail.longitude}</h3>
                        <h3>Description: ${weather_detail.description}</h3>
                        <h3>Weather Type: ${weather_detail.weather_type}</h3>
                        <h3>Temperature: ${weather_detail.temperature} degree celsius</h3>
                        <h3>Temperature Feels Like: ${weather_detail.feels_like} degree celsius</h3>
                        <h3>Minimum Temperature: ${weather_detail.min_temp} degree celsius</h3>
                        <h3>Maximum Temperature: ${weather_detail.max_temp} degree celsius</h3>
                        <h3>Pressure: ${weather_detail.pressure} hPa</h3>
                        <h3>Humidity: ${weather_detail.humidity} %</h3>
                        <h3>Visibility: ${weather_detail.visibility} km</h3>
                    </div>
                `)
                $('#result_page').show()
                $("#btn_send").text('Show Weather Details');
                $("#btn_send").attr("disabled", false);
                $("#btn_send").css('cursor', 'pointer');
            },
        })

    })
})

init()