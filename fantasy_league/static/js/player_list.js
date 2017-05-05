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
      jQuery('select:not(#status)').selectpicker({
        "width": "70px",
        "noneSelectedText": "-"
      });
  };

  // Render Selectors
  reRenderSelectors();

  jQuery('.selectpicker').on('changed.bs.select', function (evt, index) {

  });
});
