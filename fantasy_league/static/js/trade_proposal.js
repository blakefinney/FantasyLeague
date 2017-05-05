jQuery(function() {
  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  var reRenderSelectors = function () {
      jQuery('select').selectpicker({
        "width": "100%"
      });
  };

  // Render Selectors
  reRenderSelectors();

  jQuery('.selectpicker').on('changed.bs.select', function (evt, index) {
    var selected = user_team[index-1];
    var ret_string = '';
    ret_string += '<div style="height: 11%; border-radius: 25px; border-style: solid; border-color: black; border-width: 1px; ';
    ret_string += 'background-image: url(\'http://s.nflcdn.com/static/content/public/static/img/fantasy/player-card/headshot-logo-bg/'+selected.team+'.png\'); background-size: cover; background-position: center;">';

    ret_string += '<img style="height: 98%; margin-left: 20px;" src="http://static.nfl.com/static/content/public/static/img/fantasy/transparent/200x200/'+selected.esb_id+'.png"/>';
    ret_string += '<div style="font-weight: 900; font-size: 1.3em; display:inline-block;">'+selected.position+' - '+selected.name+'</div>';
    ret_string += '<a style="float: right;" class="btn btn-danger">X</a>';
    ret_string += '</div>';
    jQuery('#UserPlayerHolder').append(ret_string)
  });

  jQuery.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  jQuery('#saveTeam').click(function(){

  });
});
