(function($){
$.widget("custom.export_controls", {
    options: {
        action: ''
    },

    _create: function() {
        $('<form>', {
            id: 'export_form'
        }).appendTo('#export_control')
        
        // Stop reloading the page
        $( "form" ).submit(function( event ) {
            event.preventDefault();
        });

        $('#export_form')
            .append($('<input>', {
                id: 'separate_classes',
                name: 'separate_classes',
                type: 'checkbox',
                checked: true
            }))
            .append($('<label>', {
                for: 'separate_classes',
                form: 'export_controls',
                text:'Separate Classes'
            }))
            .append($('<div>'))
            .append($('<input>', {
                id: 'output_format',
                name: 'output_format',
                type: 'text',
                required: true,
                value: '{class}, {time}'
            }))
            .append($('<label>', {
                for: 'output_format',
                form: 'export_controls',
                text:'Output Format'
            }))
            .append($('<div>'))
            .append($('<input>', {
                id: 'export_submit',
                type: 'submit',
                value: 'Export'
            }))
        
        $('#export_submit').on('click', this.export_data);
    },

    export_data: function() {
        // This calls from the context of the submit button
        var form = $("form").serializeArray();
        console.log(form)
        form.push({name: 'test', value: 'content'})

        $.post(action, form, function(d) {
            console.log(d)
        });
    }

})
})(jQuery);
/*
$('#export_controls').submit(function() {
    form = this.serializeArray();
    
    form = form.concat([
        {name: "customer_id", value: window.username},
        {name: "post_action", value: "Update Information"}
    ]);
    
    $.post('/export', form, function(d) {
        if (d.error) {
            alert("There was a problem updating your user details")
        } 
    });
});*/
