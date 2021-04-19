/*
 * JavaScript file for the application to demonstrate
 * using the API for creating, updating and deleting materials
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        read_one: function (family_id, material_id) {
            let ajax_options = {
                type: 'GET',
                url: `/api/families/${family_id}/materials/${material_id}`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        read: function (family_id) {
            let ajax_options = {
                type: 'GET',
                url: `/api/families/${family_id}`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        create: function (family_id, material) {
            let ajax_options = {
                type: 'POST',
                url: `/api/families/${family_id}/materials`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(material)
            };
            return $.ajax(ajax_options);
        },
        update: function (family_id, material) {
            let ajax_options = {
                type: 'PUT',
                url: `/api/families/${family_id}/materials/${material.material_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(material)
            };
            return $.ajax(ajax_options);
        },
        'delete': function (family_id, material_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `/api/families/${family_id}/materials/${material_id}`,
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
        $timestamp = $('#timestamp'),
        $material_id = $('#material_id'),
        $masse_combustible = $('#masse_combustible'),
        $masse_surfacique = $('#masse_surfacique'),
        $material_name = $('#material_name'),
        $material = $('#material'),
        $create = $('#create'),
        $update = $('#update'),
        $delete = $('#delete'),
        $reset = $('#reset');

    // return the API
    return {
        NEW_MATERIAL: NEW_MATERIAL,
        EXISTING_MATERIAL: EXISTING_MATERIAL,
        reset: function () {
            $material_id.text('');
            $material_name.text('');
            $masse_surfacique.text('');
            $masse_combustible.text('');
            $material.val('').focus();
        },
        update_editor: function (material) {
            $material_id.text(material.material_id);
            $material_name.val(material.material_name);
            $masse_surfacique.val(material.masse_surfacique);
            $masse_combustible.val(material.masse_combustible);
            $material.val(material.material_name).focus();
        },
        set_button_states: function (state) {
            if (state === NEW_MATERIAL) {
                $create.prop('disabled', false);
                $update.prop('disabled', true);
                $delete.prop('disabled', true);
            } else if (state === EXISTING_MATERIAL) {
                $create.prop('disabled', true);
                $update.prop('disabled', false);
                $delete.prop('disabled', false);
            }
        },
        build_table: function (family) {
            let source = $('#materials-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // update the family data
            $family_id.text(family.family_id);
            $family_name.text(family.family_name);
            $timestamp.text(family.timestamp);

            // clear the table
            $('.materials table > tbody').empty();

            // did we get a material array?
            if (family.materials) {

                // Create the HTML from the template and materials
                html = template({materials: family.materials});

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
        $url_material_id = $('#url_material_id'),
        $material_id = $('#material_id'),
        $material = $('#material');

    // read the family data with materials
    setTimeout(function () {
        view.reset();
        model.read(parseInt($url_family_id.val()))
            .done(function (data) {
                view.build_table(data);
                view.update_editor(data);
                view.set_button_states(view.NEW_MATERIAL);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            });

        if ($url_material_id.val() !== "") {
            model.read_one(parseInt($url_family_id.val()), parseInt($url_material_id.val()))
                .done(function (data) {
                    view.update_editor(data);
                    view.set_button_states(view.EXISTING_MATERIAL);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });
        }
    }, 100);

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;

        view.error(error_msg);
        console.log(error_msg);
    }

    // initialize the button states
    view.set_button_states(view.NEW_MATERIAL);

    // Validate input
    function validate(material) {
        return material !== "";
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let material = $material.val();

        e.preventDefault();

        if (validate(material)) {
            model.create(parseInt($('#url_family_id').val()), {
                content: material  //FIXME: Replace content by material_name
            })
                .done(function (data) {
                    model.read(parseInt($('#url_family_id').val()))
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_states(view.NEW_MATERIAL);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

        } else {
            alert('Problem with material input');
        }
    });

    $('#update').click(function (e) {
        let family_id = parseInt($url_family_id.val()),
            material_id = parseInt($material_id.text()),
            material = $material.val();

        e.preventDefault();

        if (validate(material)) {
            model.update(family_id, {
                material_id: material_id,
                material: material
            })
                .done(function (data) {
                    model.read(data.family.family_id)
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_states(view.NEW_MATERIAL);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

        } else {
            alert('Problem with family name');
        }
    });

    $('#delete').click(function (e) {
        let family_id = parseInt($url_family_id.val()),
            material_id = parseInt($material_id.text());

        e.preventDefault();

        if (validate('placeholder', family_name)) {
            model.delete(family_id, material_id)
                .done(function (data) {
                    model.read(parseInt($('#url_family_id').val()))
                        .done(function(data) {
                            view.build_table(data);
                        })
                        .fail(function(xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                    view.set_button_states(view.NEW_MATERIAL);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

        } else {
            alert('Problem with family name');
        }
    });

    $('#reset').click(function () {
        view.reset();
        view.set_button_states(view.NEW_MATERIAL);
    })

    $('table').on('click', 'tbody tr', function (e) {
        let $target = $(e.target).parent(),
            material_id = $target.data('material_id'),
            material_name = $target.data('material_name'),
            masse_surfacique = $target.data('masse_surfacique'),
            masse_combustible = $target.data('masse_combustible');

            console.log(material_name);
            console.log(masse_surfacique);

        view.update_editor({
            material_id: material_id,
            material_name: material_name,
            masse_surfacique: masse_surfacique,
            masse_combustible: masse_combustible,
        });
        view.set_button_states(view.EXISTING_MATERIAL);
    });
}(ns.model, ns.view));
