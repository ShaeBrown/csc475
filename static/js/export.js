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
                value: '{time}, {type}'
            }))
            .append($('<label>', {
                for: 'output_format',
                form: 'export_controls',
                text:'Output Format'
            }))
            .append($('<div>'))
            .append($('<input>', {
                id: 'output_filename',
                name: 'output_filename',
                type: 'text',
                required: true,
                value: 'drum_events'
            }))
            .append($('<label>', {
                for: 'output_filename',
                form: 'export_controls',
                text:'Output Filename'
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
        var drum_times = $('body').visualization('get_all_drum_times');
        form.push({name: 'drum_events',
                   value: JSON.stringify(drum_times)})

        $.post(action, form, function (result) {
            // https://stackoverflow.com/a/26129406/4234532
            var blob=new Blob([result]);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download=$('#output_filename')[0].value;
            link.click();
        
        });
    }

})
})(jQuery);
