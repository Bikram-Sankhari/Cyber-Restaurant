let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: { 'country': ['in'] },
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else {
        var geocoder = new google.maps.Geocoder();
        var address = document.getElementById('id_address').value;

        geocoder.geocode({ 'address': address }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var latitude = results[0].geometry.location.lat();
                var longitude = results[0].geometry.location.lng();

                $('#id_latitude').val(latitude);
                $('#id_longitude').val(longitude);
            }

        })

        for (var i = 0; i < place.address_components.length; i++) {
            for (var j = 0; j < place.address_components[i].types.length; j++) {
                var addressType = place.address_components[i].types[j];
                try {
                    if (addressType == 'locality') {
                        document.getElementById('id_city').value = place.address_components[i].long_name;
                    }
                    else if (addressType == 'administrative_area_level_1') {
                        document.getElementById('id_state').value = place.address_components[i].long_name;
                    }
                    else if (addressType == 'country') {
                        document.getElementById('id_country').value = place.address_components[i].long_name;
                    }

                    else if (addressType == 'postal_code') {
                        document.getElementById('id_pin_code').value = place.address_components[i].long_name;
                    }

                    else {
                        document.getElementById('id_pin_code').value = "";
                    }
                }
                catch (err) { }
            }
        }

    }
    // get the address components and assign them to the fields
}

function user_not_logged_in() {
    Swal.fire({
        title: "You are not Logged In",
        text: "Do You want to Login??",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#c33332",
        cancelButtonColor: "grey",
        confirmButtonText: "Yes, Login!"
    }).then((result) => {
        if (result.isConfirmed) {
            let timerInterval;
            Swal.fire({
                title: "Hold Tight..............Redirecting Safely",
                html: "In <b></b> milliseconds.",
                timer: 2000,
                timerProgressBar: true,
                didOpen: () => {
                    Swal.showLoading();
                    const timer = Swal.getPopup().querySelector("b");
                    timerInterval = setInterval(() => {
                        timer.textContent = `${Swal.getTimerLeft()}`;
                    }, 100);
                },
                willClose: () => {
                    clearInterval(timerInterval);
                }
            }).then(function () {
                window.location = '/accounts/login';
            });
        }
    });
}

function update_details(response) {
    document.getElementById('qty-' + food_id).innerHTML = response.quantity;
    document.getElementById('total-qty').innerHTML = response.total_quantity['food_count'];
}

function update_amounts(response) {
    try {
        let gst = (parseFloat(response.subtotal) * 18 / 100).toFixed(2);
        document.getElementById('subtotal').innerHTML = response.subtotal;
        document.getElementById('gst').innerHTML = gst;
        document.getElementById('total').innerHTML = (parseFloat(response.subtotal) + parseFloat(gst)).toFixed(2);
    }

    catch (err) { }
}

function handle_empty_cart() {
    const cart_holder = document.getElementById('cart-holder');
    if (cart_holder.getElementsByTagName("li").length == 0) {
        const div = document.createElement("div");
        div.setAttribute("class", "text-center p-5");
        const h3 = document.createElement("h3");
        const empty_label = document.createTextNode("Your Cart is Empty")
        h3.appendChild(empty_label);
        div.appendChild(h3);
        cart_holder.appendChild(div);
    }
}

function get_days_map() {
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    const days_map = new Map();
    for (let i = 1; i < 8; i++) {
        days_map.set(String(i), days_of_week[i - 1]);
    }
    return days_map;
}

function get_times_map() {
    const start_time = new Date('July 1, 1999, 00:00:00');
    const end_time = new Date('July 2, 1999, 00:00:00');
    const increment = 30 * 60 * 1000;
    i = '0.0';

    const times_map = new Map();

    while (start_time < end_time) {
        hour = start_time.getHours();
        minutes = start_time.getMinutes();
        if (hour < 12) {
            if (hour < 10) {
                if (minutes < 10) {
                    times_map.set(String(i), "0" + hour + ":0" + minutes + " AM");
                }
                else {
                    times_map.set(String(i), "0" + hour + ":" + minutes + " AM");
                }
            }

            else {
                if (minutes < 10) {
                    times_map.set(String(i), hour + ":0" + minutes + " AM");
                }
                else {
                    times_map.set(String(i), hour + ":" + minutes + " AM");
                }
            }
        }

        else {
            if (hour >= 13) {
                hour = hour - 12;
                if (hour < 10) {
                    if (minutes < 10) {
                        times_map.set(String(i), "0" + hour + ":0" + minutes + " PM");
                    }
                    else {
                        times_map.set(String(i), "0" + hour + ":" + minutes + " PM");
                    }
                }

                else {
                    if (minutes < 10) {
                        times_map.set(String(i), hour + ":0" + minutes + " PM");
                    }
                    else {
                        times_map.set(String(i), hour + ":" + minutes + " PM");
                    }
                }
            }

            else {
                if (minutes < 10) {
                    times_map.set(String(i), hour + ":0" + minutes + " PM");
                }
                else {
                    times_map.set(String(i), hour + ":" + minutes + " PM");
                }
            }
        }


        start_time.setTime(start_time.getTime() + increment);
        i = parseFloat(i);
        i += 0.5;
        i = i.toFixed(1)
        i = String(i);
    }

    return times_map;
}

// Add, Remove and Delete functionalitites of Cart
$(document).ready(function () {
    $('.add-to-cart').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href');
        food_id = $(this).attr('data-id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'Success') {
                    update_details(response);
                    update_amounts(response);
                }

                else if (response.code == 400) {
                    user_not_logged_in();
                }

                else {
                    Swal.fire(response.message);
                }
            }
        })
    })

    $('.decrease-cart').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href');
        food_id = $(this).attr('data-id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'Success') {
                    if (response.code == 201) {
                        delete_url = "/marketplace/delete_cart/" + food_id;

                        Swal.fire({
                            title: "Remove Item from Cart",
                            text: "Do you confirm??",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonColor: "#c33332",
                            cancelButtonColor: "grey",
                            confirmButtonText: "Yes, Remove"
                        }).then((result) => {
                            if (result.isConfirmed) {
                                $.ajax({
                                    type: 'GET',
                                    url: delete_url,
                                    success: function (response) {
                                        if (response.status == 'Success') {
                                            if (window.location.pathname == '/marketplace/cart/') {
                                                document.getElementById('food-item-' + food_id).remove();
                                                handle_empty_cart();
                                            }
                                            else {
                                                document.getElementById('qty-' + food_id).innerHTML = 0;
                                            }
                                            document.getElementById('total-qty').innerHTML = response.total_quantity['food_count'];
                                            update_amounts(response);
                                            Swal.fire({
                                                title: "Success",
                                                text: "Item removed from Cart",
                                                icon: "success"
                                            });
                                        }

                                        else {
                                            Swal.fire(response.message);
                                        }
                                    }
                                })
                            }
                        });
                    }

                    else {
                        update_details(response);
                        update_amounts(response);
                    }
                }

                else if (response.code == 400) {
                    user_not_logged_in();
                }

                else {
                    Swal.fire(response.message);
                }
            }
        })

    })

    $('.delete-cart').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href');
        food_id = $(this).attr('data-id');

        Swal.fire({
            title: "Remove Item from Cart",
            text: "Do you confirm??",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#c33332",
            cancelButtonColor: "grey",
            confirmButtonText: "Yes, Remove"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'GET',
                    url: url,
                    success: function (response) {
                        if (response.status == 'Success') {
                            document.getElementById('food-item-' + food_id).remove();
                            document.getElementById('total-qty').innerHTML = response.total_quantity['food_count'];
                            update_amounts(response);
                            handle_empty_cart();
                            Swal.fire({
                                title: "Success",
                                text: "Item removed from Cart",
                                icon: "success"
                            });
                        }

                        else if (response.code == 400) {
                            user_not_logged_in();

                        }

                        else {
                            Swal.fire(response.message);
                        }
                    }
                })
            }
        });

    })

    $('#add-opening-hour').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href');
        day = $('#id_day').val();
        open = $('#id_open').val();
        close = $('#id_close').val();
        is_closed = $('#id_is_closed').is(":checked");
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        days_map = get_days_map();
        day_str = days_map.get('1');

        times_map = get_times_map();
        open_str = times_map.get(String(open));
        close_str = times_map.get(String(close));

        console.log(close_str, times_map);

        data = {
            'day': day,
            'open': open,
            'close': close,
            'is_closed': is_closed,
            'csrfmiddlewaretoken': csrf_token
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: function (response) {
                if (response.status == 'Success') {
                    Swal.fire({
                        title: "WooHooo!!!",
                        text: "Opening Hour added Successfully",
                        icon: "success"
                    }).then((result) => {
                        // New Row
                        new_row = document.createElement('tr')
                        new_row.setAttribute('class', 'row px-3 mb-2-');
                        new_row.setAttribute('style', 'border: 1px solid #d6d6d4;');

                        // Day Column
                        day_column = document.createElement('td')
                        bold = document.createElement('b');
                        day_column_string = document.createTextNode(day_str);
                        bold.appendChild(day_column_string)
                        day_column.appendChild(bold);
                        day_column.setAttribute('class', 'py-3 text-start col-12 col-sm-3 col-lg-2');

                        new_row.appendChild(day_column)

                        if (is_closed) {
                            // Holiday Column
                            holiday_column = document.createElement('td')
                            holiday_span = document.createElement('span')
                            holiday_column_string = document.createTextNode('Holiday');

                            holiday_span.appendChild(holiday_column_string)
                            holiday_column.appendChild(holiday_span);

                            holiday_span.setAttribute('class', 'text-muted');
                            holiday_column.setAttribute('class', 'py-3 col-11 col-sm-7 col-lg-5');

                            new_row.appendChild(holiday_column)
                        }

                        else{
                            // Opening time column
                            open_column = document.createElement('td')
                            open_text = document.createTextNode(open_str);

                            open_column.appendChild(open_text);
                            open_column.setAttribute('class', 'py-3 col-5 col-sm-3 col-lg-2');

                            new_row.appendChild(open_column)
                            // Hyphen
                            hyphen_column = document.createElement('td')
                            hyphen_text = document.createTextNode('-');

                            hyphen_column.appendChild(hyphen_text)
                            hyphen_column.setAttribute('class', 'py-3 px-0 col-1');

                            new_row.appendChild(hyphen_column)
                            // Closing time column
                            close_column = document.createElement('td')
                            close_text = document.createTextNode(close_str);

                            close_column.appendChild(close_text)
                            close_column.setAttribute('class', 'py-3 col-5 col-sm-3 col-lg-2');

                            new_row.appendChild(close_column)

                            // Delete and Edit icons
                            
                        }
                    });;
                }

                else {
                    Swal.fire({
                        title: "Oops!",
                        text: response.message,
                        icon: "info"
                    });
                }
            }
        })
    })
})


// Function for Fetching current location coords
function getLocation() {
    navigator.geolocation.getCurrentPosition(success, error);
}

function success(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    try {
        $('#id_latitude').val(latitude);
        $('#id_longitude').val(longitude)
    }
    catch (err) { }
    var url = "https://maps.google.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&key=" + google_api_key;
    var home_url = $("#home").attr('href') + "location_accessed";

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            if (response.status == "OK") {
                var address = response.results[0].formatted_address;
                try {
                    document.getElementById('id_address').value = address;
                }
                catch (err) { }
                document.getElementById('current-location').value = address;
                sessionStorage.setItem('current_location', address);
                window.location = home_url + "?longitude=" + longitude + "&latitude=" + latitude;
            }
            else {
                error(response);
            }
        }
    })
}

function error(err) {
    Swal.fire({
        title: "The Internet?",
        text: err.message,
        icon: "error"
    });
}
