function generateValidationRules(form) {
    var rules = {};
    form.find('input[type=number]').each(function(_, e) {
        rules[$(e).attr('name')] = {
            min: 0,
            required: true,
        };
    });
    return rules;
}

// allow custom, per-field validators
// the validate plugin calls any functions it finds in rules, so it is necessary
// to pass the custom function in a one-element array
$.validator.addMethod('custom', function(value, element, callbacks) {
    return callbacks[0](value, element);
});

$(function() {
    if (location.pathname.indexOf('/form') == 0) {
        var match_data = {data: {}, loaded: false};
        // open links in a new window
        $('a[href^="/"]').attr('target','_blank');
    	//This allows the Match ID field to be automatically filled
    	//based on the previous value entered + 1
        if (!$('#match_id').val())
            $('#match_id').val(Number(localStorage.getItem('last_match_id')) + 1);
        $('#scouting-form').on('submit', function() {
            localStorage.setItem('last_match_id',$('#match_id').val());
        }).validate({
            rules: generateValidationRules($('#scouting-form')),
            highlight: function(element) {
                $(element).closest('.form-field').addClass('has-error');
            },
            unhighlight: function(element) {
                $(element).closest('.form-field').removeClass('has-error');
            },
            errorElement: 'span',
            errorClass: 'help-block',
            errorPlacement: function(error, element) {
                // disable messages
                return true;
            }
        });

        $('#scouting-form #match_id').rules('add', {custom: [function(value){
            return !(match_data.loaded && !(value in match_data.data));
        }]});

        $('#match_id').on('change keyup focus blur', function(){
            if (!match_data.loaded)
                return;
            $('#team_id').val(match_data.data[$(this).val()] || '')
                .change()
                .valid();
        });
        $('#team_id').on('change keyup focus blur', function(){
            if (!match_data.loaded)
                return;
            var expected = match_data.data[$('#match_id').val()];
            if (!expected)
                return;
            if ($(this).val() == expected)
                $('#alert').hide();
            else
                $('#alert').show().attr({'class': 'alert alert-warning'}).text('Team ID not set to ' + expected);
        });

        $.getJSON('/match_schedules', function(data) {
            if (data.error) {
                if ($('form #alert').is(':hidden'))
                    $('form #alert').show().addClass('alert-danger').text(data.error);
                return;
            }
            match_data.data = data;
            match_data.loaded = true;
            $('#match_id').change();
        });

        //Add +/- buttons next to input fields so it is easy on touchscreen
        function mkbutton() {
            return $('<a>').attr('href', '#').addClass('btn btn-default input-group-addon').click(function(e){e.preventDefault();});
        }
        $('input[type=number]').each(function(i, e) {
            if ($(e).hasClass('no-buttons'))
                return;
            var increment = function(n) {
                return function() {
                    $(e).val(Number($(e).val()) + n);
                    $(e).trigger('keyup');
                }
            }
            var button_inc = mkbutton().text('+').insertAfter($(e)).click(increment(1));
            var button_dec = mkbutton().text('-').insertBefore($(e)).click(increment(-1));
        });
        $('.checkbox-button-field input[type=checkbox]').each(function(_, e) {
            if ($(e).prop('checked'))
                $(e).parent('label').addClass('btn-success active').removeClass('btn-default');
        }).change(function() {
            var label = $(this).parent('label');
            label.removeClass('btn-default btn-success').addClass(
                $(this).prop('checked') ? 'btn-success' : 'btn-default'
            );
        });
    }
});
