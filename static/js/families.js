/*
 * JavaScript file for the application to demonstrate
 * using the API for the Families SPA
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        read_one: function (family_id) {
            let ajax_options = {
                type: 'GET',
                url: `/api/families/${family_id}`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        read: function () {
            let ajax_options = {
                type: 'GET',
                url: '/api/families',
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        create: function (family) {
            let ajax_options = {
                type: 'POST',
                url: '/api/families',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(family)
            };
            return $.ajax(ajax_options);
        },
        update: function (family) {
            let ajax_options = {
                type: 'PUT',
                url: `/api/families/${family.family_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(family)
            };
            return $.ajax(ajax_options);
        },
        calculate: function(family_id){
            let ajax_options = {
                type: 'GET',
                url: `/api/families/${family_id}/calculate`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        'delete': function (family_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `/api/families/${family_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            return $.ajax(ajax_options);
        }
    };
}());

// Create the view instance
ns.view = (function () {
    'use strict';

    const NEW_MATERIAL = 0,
        EXISTING_MATERIAL = 1;

    let $family_id = $('#family_id'),
        $family_name = $('#family_name'),


        $create = $('#create'),
        $update = $('#update'),
        $calculate = $('#calculate'),
        $delete = $('#delete'),
        $reset = $('#reset');

    // return the API
    return {
        NEW_MATERIAL: NEW_MATERIAL,
        EXISTING_MATERIAL: EXISTING_MATERIAL,
        reset: function () {
            $family_id.text('');
            $family_name.val('').focus();
        },
        update_editor: function (family) {
            $family_id.text(family.family_id);
            $family_name.val(family.family_name).focus();
        },
        update_table: function(attributes){

            let $row = $("[data-family_id="+$family_id.text()+"]");
            let $nb_materials = $row.find('td.nb_materials'),
            $min_ms = $row.find('td.min_ms'),
            $max_ms = $row.find('td.max_ms'),
            $min_mc = $row.find('td.min_mc'),
            $max_mc = $row.find('td.max_mc');

            $nb_materials.text(attributes.nb_materials),
            $min_ms.text(attributes.min_ms),
            $max_ms.text(attributes.max_ms),
            $min_mc.text(attributes.min_mc),
            $max_mc.text(attributes.max_mc);

        },
        set_button_state: function (state) {
            if (state === NEW_MATERIAL) {
                $create.prop('disabled', false);
                $update.prop('disabled', true);
                $calculate.prop('disabled', true);
                $delete.prop('disabled', true);
            } else if (state === EXISTING_MATERIAL) {
                $create.prop('disabled', true);
                $update.prop('disabled', false);
                $calculate.prop('disabled', false);
                $delete.prop('disabled', false);
            }
        },
        build_table: function (families) {
            let source = $('#families-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // clear the table
            $('.families table > tbody').empty();

            // did we get a families array?
            if (families) {

                // Create the HTML from the template and families
                html = template({families: families})

                // Append the html to the table
                $('table').append(html);
            }
        },
        error: function (error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function () {
                $('.error').fadeOut();
            }, 2000)
        }
    };
}());

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $url_family_id = $('#url_family_id'),
        $family_id = $('#family_id'),
        $family_name = $('#family_name'),
        $nb_materials = $('#nb_materials'),
        $min_ms = $('#min_ms'),
        $max_ms = $('#max_ms'),
        $min_mc = $('#min_mc'),
        $max_mc = $('max_mc');


    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        view.reset();
        model.read()
            .done(function(data) {
                view.build_table(data);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            })

        if ($url_family_id.val() !== "") {
            model.read_one(parseInt($url_family_id.val()))
                .done(function(data) {
                    view.update_editor(data);
                    view.set_button_state(view.EXISTING_MATERIAL);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });
        }
    }, 100)

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;

        view.error(error_msg);
        console.log(error_msg);
    }
    // initialize the button states
    view.set_button_state(view.NEW_MATERIAL);

    // Validate input
    function validate(family_name) {
        return family_name !== "";
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let family_name = $family_name.val();


        e.preventDefault();

        if (validate(family_name)) {
            model.create({
                'family_name': family_name,

            })
                .done(function(data) {
                    model.read()
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.set_button_state(view.NEW_MATERIAL);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

            view.reset();

        } else {
            alert('Problem with family name');
        }
    });

    $('#update').click(function (e) {
        let family_id = parseInt($family_id.text()),
            family_name = $family_name.val();


        e.preventDefault();

        if (validate(family_name)) {
            model.update({
                family_id: family_id,
                family_name: family_name,

            })
                .done(function(data) {
                    model.read()
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_state(view.NEW_MATERIAL);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                })

        } else {
            alert('Problem with family name');
        }
        e.preventDefault();
    });

    $('#calculate').click(function (e) {
        let family_id = parseInt($('#family_id').text());
        //console.log(family_id)

        e.preventDefault();

        if (validate(family_name)) {
            model.calculate(
                family_id
            )
                .done(function(data) {
                    model.read()
                        .done(function(data) {
                            //view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.update_table(data);
                    view.reset();
                    view.set_button_state(view.NEW_MATERIAL);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                })

        } else {
            alert('Problem with family name');
        }
        e.preventDefault();
    });

    $('#delete').click(function (e) {
        let family_id = parseInt($family_id.text());

        e.preventDefault();

        if (validate('placeholder', family_name)) {
            model.delete(family_id)
                .done(function(data) {
                    model.read()
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_state(view.NEW_MATERIAL);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

        } else {
            alert('Problem with family name');
        }
    });

    $('#reset').click(function () {
        view.reset();
        view.set_button_state(view.NEW_MATERIAL);
    })

    $('table').on('click', 'tbody tr', function (e) {
        let $target = $(e.target).parent(),
            family_id = $target.data('family_id'),
            family_name = $target.data('family_name');


        view.update_editor({
            family_id: family_id,
            family_name: family_name,

        });
        view.set_button_state(view.EXISTING_MATERIAL);
    });

    $('table').on('dblclick', 'tbody tr', function (e) {
        let $target = $(e.target),
            family_id = $target.parent().attr('data-family_id');

        window.location.href = `/families/${family_id}/materials`;

    });
}(ns.model, ns.view));
