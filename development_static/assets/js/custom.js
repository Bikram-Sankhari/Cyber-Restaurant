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
                catch (err) {
                    console.log(err);
                 }
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
        document.getElementById('subtotal').innerHTML = response.amounts['subtotal'];
        document.getElementById('gst').innerHTML = response.amounts['gst'];
        document.getElementById('total').innerHTML = response.amounts['total'];
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

        checkout_button = document.getElementById('checkout_button')
        checkout_button.classList.add("disabled");
        checkout_button.innerHTML= "No Items to Checkout";
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

function confirm_deletion(url, message) {
    Swal.fire({
        title: "Confirmation",
        text: message,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#c33332",
        cancelButtonColor: "grey",
        confirmButtonText: "Yes, Delete"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location = url;
        }
    });
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
                if (hour < 1) {
                    hour = 12;

                    if (minutes < 10) {
                        times_map.set(String(i), hour + ":0" + minutes + " AM");
                    }
                    else {
                        times_map.set(String(i), hour + ":" + minutes + " AM");
                    }
                }

                else {
                    if (minutes < 10) {
                        times_map.set(String(i), "0" + hour + ":0" + minutes + " AM");
                    }
                    else {
                        times_map.set(String(i), "0" + hour + ":" + minutes + " AM");
                    }
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

function remove_opening_hour() {
    $('.remove_opening_hour').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href');
        csrf_token = $(this).parent("div").find('input[name="csrfmiddlewaretoken"]').val();

        headers = {
            'X-CSRFToken': csrf_token,
        }

        if ($(this).attr('data-is-holiday') == undefined) {
            message = "Remove " + $(this).attr('data-open') + " to " + $(this).attr('data-close') + " Open hours for " + $(this).attr('data-day') + "??"
        }

        else {
            message = "Remove Holiday for " + $(this).attr('data-day') + "??"
        }

        Swal.fire({
            title: "Are you sure?",
            text: message,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#c33332",
            cancelButtonColor: "grey",
            confirmButtonText: "Yes, Remove"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'DELETE',
                    url: url,
                    headers: headers,
                    success: function (response) {
                        if (response.status == 'Success') {
                            document.getElementById(response.new_id).remove();

                            tbody = document.getElementById('table-body');
                            rows = tbody.querySelectorAll('tr');

                            if (rows.length == 0) {
                                $('table').remove();
                                no_opening_hour = document.createElement('h6');
                                no_opening_hour_text = document.createTextNode('Set your Opening Hours and start receiving Orders');
                                no_opening_hour_hr = document.createElement('hr');

                                no_opening_hour.appendChild(no_opening_hour_text);
                                no_opening_hour.setAttribute('id', 'no_opening_hours');
                                no_opening_hour.setAttribute('class', 'text-center my-4');

                                top_hr = document.getElementById('top-hr');

                                top_hr.insertAdjacentElement('afterend', no_opening_hour);
                                no_opening_hour.insertAdjacentElement('afterend', no_opening_hour_hr);

                            }
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
            }
        })

    })
}

// Add, Remove and Delete functionalitites of Cart
$(document).ready(function () {
    $('#to-be-deleted').remove();

    try {
        $('#google-script').remove();
    }

    catch (err) { }

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
        day_str = days_map.get(String(day));

        times_map = get_times_map();
        open_str = times_map.get(String(open));
        close_str = times_map.get(String(close));

        data = {
            'day': day,
            'open': open,
            'close': close,
            'is_closed': is_closed,
            'csrfmiddlewaretoken': csrf_token
        }
        headers = {
            'X-CSRFToken': csrf_token,
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            headers: headers,
            success: function (response) {
                if (response.status == 'Success') {

                    // New Row
                    new_row = document.createElement('tr');
                    new_row.setAttribute('class', 'row px-3 mb-2');
                    new_row.setAttribute('style', 'border: 1px solid #d6d6d4;');
                    new_row.setAttribute('id', response.new_id);
                    new_row.setAttribute('data-day', String(day));
                    new_row.setAttribute('data-open', String(open));

                    // Day Column
                    day_column = document.createElement('td');
                    bold = document.createElement('b');
                    day_column_string = document.createTextNode(day_str);
                    bold.appendChild(day_column_string);
                    day_column.appendChild(bold);
                    day_column.setAttribute('class', 'py-3 text-start col-12 col-sm-3 col-lg-2');

                    new_row.appendChild(day_column);

                    if (is_closed) {
                        // Holiday Column
                        holiday_column = document.createElement('td');
                        holiday_span = document.createElement('span');
                        holiday_column_string = document.createTextNode('Holiday');

                        holiday_span.appendChild(holiday_column_string)
                        holiday_column.appendChild(holiday_span);

                        holiday_span.setAttribute('class', 'text-muted');
                        holiday_column.setAttribute('class', 'py-3 col-11 col-sm-7 col-lg-5');

                        new_row.appendChild(holiday_column);
                    }

                    else {
                        // Opening time column
                        open_column = document.createElement('td');
                        open_text = document.createTextNode(open_str);

                        open_column.appendChild(open_text);
                        open_column.setAttribute('class', 'py-3 col-5 col-sm-3 col-lg-2');

                        new_row.appendChild(open_column);

                        // Hyphen
                        hyphen_column = document.createElement('td');
                        hyphen_text = document.createTextNode('-');

                        hyphen_column.appendChild(hyphen_text);
                        hyphen_column.setAttribute('class', 'py-3 px-0 col-1');

                        new_row.appendChild(hyphen_column);
                        // Closing time column
                        close_column = document.createElement('td');
                        close_text = document.createTextNode(close_str);

                        close_column.appendChild(close_text);
                        close_column.setAttribute('class', 'py-3 col-5 col-sm-3 col-lg-2');

                        new_row.appendChild(close_column);
                    }

                    items_div = document.createElement('div');

                    // CSRF tag
                    csrf_input = document.createElement('input');
                    csrf_input.setAttribute('type', 'hidden');
                    csrf_input.setAttribute('name', 'csrfmiddlewaretoken');
                    csrf_input.setAttribute('value', response.csrf);

                    items_div.appendChild(csrf_input);

                    // Delete Icon
                    items_column = document.createElement('td');
                    delete_a = document.createElement('a');
                    delete_i = document.createElement('i');



                    delete_i.setAttribute('class', 'bi bi-trash mx-2');
                    delete_i.setAttribute('style', 'color:red;');
                    delete_a.appendChild(delete_i);
                    delete_a.append(delete_i);

                    delete_a.setAttribute('href', '/accounts/vendor/opening-hours/remove/' + response.new_id + '/');
                    delete_a.setAttribute('class', 'remove_opening_hour');
                    delete_a.setAttribute('data-day', day_str);


                    if (is_closed) {
                        delete_a.setAttribute('data-is-holiday', '');
                    }

                    else {
                        delete_a.setAttribute('data-open', open_str);
                        delete_a.setAttribute('data-close', close_str);
                    }


                    items_div.appendChild(delete_a);

                    items_div.setAttribute('class', 'float-end');
                    // items_div.setAttribute('title', 'Refresh First');

                    items_column.appendChild(items_div);
                    items_column.setAttribute('class', 'py-3 px-0 col-12 col-sm-2 col-lg-2');

                    new_row.appendChild(items_column);


                    no_opening_hour = document.getElementById('no_opening_hours');

                    if (no_opening_hour) {
                        // Append first row
                        top_hr = document.getElementById('top-hr');

                        table = document.createElement('table');
                        tbody = document.createElement('tbody');

                        tbody.appendChild(new_row);
                        table.appendChild(tbody);

                        tbody.setAttribute('class', 'container');
                        tbody.setAttribute('id', 'table-body');
                        table.setAttribute('class', 'table table-hover table-borderless');

                        top_hr.insertAdjacentElement('afterend', table);
                        no_opening_hour.remove();
                    }

                    else {
                        // Determine the position
                        adjacent_day_rows = null;
                        for (let i = day; i > 0; i--) {
                            adjacent_day_rows = document.querySelectorAll('[data-day="' + i + '"]');
                            if (adjacent_day_rows.length > 0) {
                                break;
                            }
                        }

                        if (adjacent_day_rows.length > 0) {
                            if (adjacent_day_rows[0].getAttribute('data-day') != day) {
                                // If the new entry is First Entry for that Day
                                adjacent_day_rows[adjacent_day_rows.length - 1].insertAdjacentElement('afterend', new_row);
                            }

                            else {
                                // If there are previous entries for that day
                                just_below_element = null;
                                for (let i = open - 0.5; i >= 0; i -= 0.5) {
                                    for (let j = 0; j < adjacent_day_rows.length; j++) {
                                        current_element = adjacent_day_rows[j]
                                        if (current_element.getAttribute('data-open') == i) {
                                            just_below_element = current_element;
                                            break;
                                        }
                                    }

                                    if (just_below_element) {
                                        break;
                                    }
                                }

                                if (just_below_element) {
                                    just_below_element.insertAdjacentElement('afterend', new_row);
                                }

                                else {
                                    adjacent_day_rows[0].insertAdjacentElement('beforebegin', new_row);
                                }
                            }
                        }
                        else {
                            // If the new entry is First Day
                            tbody = document.getElementById('table-body');
                            tbody.prepend(new_row);
                        }
                    }

                    remove_opening_hour();
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

    remove_opening_hour();

    $('.delete_food_item').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href')
        message = "You are about to delete " + $(this).attr('data-food') + " from category " + $(this).attr('data-category')
        confirm_deletion(url, message)
    })

    $('.delete_category').on('click', function (e) {
        e.preventDefault();
        url = $(this).attr('href')
        message = "You are about to delete " + $(this).attr('data-category') + " category"
        confirm_deletion(url, message)
    })

    $('.logout').on('click', function (e) {
        e.preventDefault;
        url = $(this).attr('href');
        sessionStorage.clear();
        window.location = url;
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
    var location_accessed_url = $("#home").attr('href') + "location_accessed";

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            if (response.status == "OK") {
                var address = response.results[0].formatted_address;
                document.getElementById('current-location').value = address;
                sessionStorage.setItem('current_location', address);
                window.location = location_accessed_url + "?longitude=" + longitude + "&latitude=" + latitude + "&current_url=" + window.location.href;
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
