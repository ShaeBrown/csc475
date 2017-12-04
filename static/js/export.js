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
        var files = {};
        output = "";
        Object.keys(drum_times).forEach(function(key) { // each class
            if (separate) {
                output = "";
            };

            drum_times[key].forEach(function (time) { // each time
                output += line_format.format({type: key, time: time});
                output += "\n";
            });

            if (separate) {
                files[filename.format({type: key})] = new Blob([output]);                   
            };
        });

        // Push the output as 1 file
        if (!separate) {
            files[filename.format({type: "all"})] = new Blob([output]);   
        };

        // Zip if needed
        if (!zip) {
            // Trigger download
            Object.keys(files).forEach(function(key) {
                var name = key;
                var data = files[key];
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(data);
                link.download = name;
                link.click();
            });
        } else {
            var zip_name = filename.format({type: "all"});
            zip_name = zip_name.replace(".txt", ".zip");

            var zipper = new JSZip();
            Object.keys(files).forEach(function(key) {
                zipper.file(key, files[key]);
            });

            zipper.generateAsync({type:"blob"}).then(function (blob) { 
                saveAs(blob, zip_name);
            }, function (err) {
                jQuery("#blob").text(err);
            });
        };
    }});
})(jQuery);

// https://stackoverflow.com/a/25327583/4234532
// Overrides string formatting to match that of python
String.prototype.format = function (arguments) {
    var this_string = '';
    for (var char_pos = 0; char_pos < this.length; char_pos++) {
        this_string = this_string + this[char_pos];
    }

    for (var key in arguments) {
        var string_key = '{' + key + '}'
        this_string = this_string.replace(new RegExp(string_key, 'g'), arguments[key]);
    }
    return this_string;
};