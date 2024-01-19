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
                                            if(window.location.pathname == '/marketplace/cart/') {
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
})
