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
                id: 'zip_file',
                name: 'zip_file',
                type: 'checkbox',
                checked: false
            }))
            .append($('<label>', {
                for: 'zip_file',
                form: 'export_controls',
                text:'Zip File'
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
                value: 'drum_events_{type}.txt'
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
            }));
        
        $('#export_submit').on('click', this.export_data);
    },

    export_data: function() {
        var zip = $('#zip_file')[0].checked;
        var separate = $('#separate_classes')[0].checked;
        var filename = $('#output_filename').val();
        var line_format = $('#output_format').val();
        var drum_times = $('body').visualization('get_all_drum_times');

        // Post results to the server here
        var drums = [{
            name: 'drum_events',
            value: JSON.stringify(drum_times)
        }];
        $.post(action, drums); 
        // Client side processing here
        /*
        for event_class, times in drum_events.items():
            for event_time in times:
                f.write(output_format.format(time=event_time, type=event_class))
                f.write('\n')
        */

        Object.keys(drum_times).forEach(function(key) {        
        
        }
        // Build file(s)
        
        // Trigger download
        /*
        // This calls from the context of the submit button
        // https://stackoverflow.com/a/26129406/4234532
        console.log(result) // pre-formatted list of events
        var blob=new Blob([result]);
        var link=document.createElement('a');
        link.href=window.URL.createObjectURL(blob);
        link.download=$('#output_filename')[0].value;
        link.click();
        */
    }});
})(jQuery);
