/*
 * JavaScript file for the Home page
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        'read': function () {
            let ajax_options = {
                type: 'GET',
                url: '/api/materials',
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        }
    };
}());


// Create the view instance
ns.view = (function () {
    'use strict';

    var $table = $(".blog table");

    // Return the API
    return {
        build_table: function (data) {
            let source = $('#blog-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // Create the HTML from the template and materials
            html = template({materials: data});

            // Append the rows to the table tbody
            $table.append(html);
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


// Create the controller instance
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v;

    // Get the material data from the model after the controller is done initializing
    setTimeout(function () {

        // Attach event handlers to the promise returned by model.read()
        model.read()
            .done(function (data) {
                view.build_table(data);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            });
    }, 100);

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;

        view.error(error_msg);
        console.log(error_msg);
    }

    // handle application events
    $('table').on('dblclick', 'tbody td.family_name', function (e) {
        let $target = $(e.target).parent(),
            family_id = $target.data('family_id'),
            material_id = $target.data('material_id');

        window.location = `/families/${family_id}`;

    });

    $('table').on('dblclick', 'tbody td.material_name', function (e) {
        let $target = $(e.target).parent(),
            family_id = $target.data('family_id'),
            material_id = $target.data('material_id');

        window.location = `families/${family_id}/materials/${material_id}`;
    });
}(ns.model, ns.view));