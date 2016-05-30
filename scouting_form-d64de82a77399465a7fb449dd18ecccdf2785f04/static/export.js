function switchStage(stage, details) {
    $('.stage').hide().filter('#stage-' + stage).show().find('#details').text(details || '');
}

function checkPath() {
    var path = $('#path').val();
    $.getJSON('/export/check_path', {path: path}, function(data) {
        switchStage(data.ok ? 'confirm' : 'bad-path', path);
    });
}

$(function(){
    $.getJSON('/export/info', function(data) {
        var lines = data.stats.lines;
        $('#stats > span').text(lines + ' match' + (lines == 1 ? '' : 'es') + ', exporting to ' + data.filename);
        if (!data.stats.lines) {
            // ugly
            switchStage('nothing');
            $('#stage-nothing .alert').removeClass('alert-info').addClass('alert-warning').text('No data to export');
            $('#path-row').hide();
        }
    });
    $('a[href^=#stage-]').click(function(e){
        e.preventDefault();
        switchStage($(this).attr('href').replace(/#stage\-/, ''));
    })
    $('#path').keydown(function(e){
        switchStage('nothing');
        if (e.which == 13)
            checkPath();
    });
    $('#check-path').click(checkPath);
    $('a[href=#stage-export]').click(function(){
        $.getJSON('/export/do_export', {path: $('#path').val()}, function(data){
            if (data.ok) {
                switchStage('success');
                $('#path-row').hide();
            }
            else
                switchStage('failed', data.error);
        });
    });
});
