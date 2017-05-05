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
  // Position eligible for which spots; Note: -1 is Bench
  var eligibility = {"QB":[0,1,-1], "RB": [2,3,7,8,9,-1], "WR":[4,5,7,8,9,-1], "TE": [6,7,8,9,-1], "K": [10,-1], "DEF": [11,-1]};
  var reRenderSelectors = function () {
    for (var i = 0; i < window.fl_starter.length; i++) {
      var select = jQuery(jQuery('.starting .selectpicker')[i]);
      var p = window.fl_starter[i];
      var empty = Boolean(p.player_id === 'noplayer');
      if(!empty) {
        for (var j = 0; j < eligibility[p.player_position].length; j++) {
          if (eligibility[p.player_position][j] > -1) {
            var sel_player = window.fl_starter[eligibility[p.player_position][j]];
            select.append('<option value="'+eligibility[p.player_position][j]+'" title="'+sel_player.position+'"'+(eligibility[p.player_position][j]===i ? ' selected ' : '')+'>' + sel_player.position + ' - '+sel_player.player_name+'</option>');
          } else {
            select.append('<option value="-1" title="BEN">Bench - Empty</option>');
          }
        }
      }
      select.selectpicker({
        "width": "76px",
        "title": p.position
      });

      if(empty){
        select.attr('disabled','disabled');
      } else {
        select.removeAttr('disabled');
      }

    }
    for (var k = 0; k < window.fl_bench.length; k++) {
      var select_b = jQuery(jQuery('.bench .selectpicker')[k]);
      var pb = window.fl_bench[k];
      var empty_b = Boolean(pb.player_id === 'noplayer');
      if(!empty_b) {
        for (var l = 0; l < eligibility[pb.player_position].length; l++) {
          if (eligibility[pb.player_position][l] > -1) {
            var sel_player_b = window.fl_starter[eligibility[pb.player_position][l]];
            select_b.append('<option value="'+eligibility[pb.player_position][l]+'" title="'+sel_player_b.position+'">' + sel_player_b.position + ' - '+sel_player_b.player_name+'</option>');
          } else {
            select_b.append('<option value="-1" title="BEN" selected >Bench - '+pb.player_name+'</option>');
          }
        }
      }
      select_b.selectpicker({
        "width": "76px",
        "title": 'BEN'
      });

      if(empty_b){
        select_b.attr('disabled','disabled');
      } else {
        select_b.removeAttr('disabled');
      }
    }
  };
  var addToBench = function (player_index) {
    // Let's assume it's a starter
    var player_obj = window.fl_starter[player_index];
    var player_row = jQuery(jQuery('tr.starting')[player_index]);
    var empty_row = jQuery('tr.bench.empty:first');
    var empty_obj = {
      player_id: "noplayer",
      player_name: "Empty",
      position: "BEN",
      position_accepts: ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
    };
  };


  reRenderSelectors();

  jQuery('.selectpicker').on('changed.bs.select', function () {
    // Change the visual lineup
    var p_index = jQuery(this).parent().parent().find('.position_index').data('index');
    var s_index = Number(jQuery(this).val());
    if(s_index > -1 && p_index < 12){
      // Starter -> Starter Swap
      var swap = window.fl_starter[s_index];
      var orig = window.fl_starter[p_index];
      // Processing
      var temp = swap.position;
      var temp2 = swap.position_accepts;

      swap.position_accepts = orig.position_accepts;
      swap.position = orig.position;

      orig.position_accepts = temp2;
      orig.position = temp;

      window.fl_starter[jQuery(this).val()] = orig;
      window.fl_starter[p_index] = swap;
    } else if (s_index > -1 && p_index > 11) {
      // Bench -> Starter Swap
      var swap = window.fl_starter[s_index];
      var orig = window.fl_bench[p_index-12];
      // Processing
      var temp = swap.position;
      var temp2 = swap.position_accepts;

      swap.position_accepts = orig.position_accepts;
      swap.position = orig.position;

      orig.position_accepts = temp2;
      orig.position = temp;

      window.fl_starter[jQuery(this).val()] = orig;
      window.fl_bench[p_index-12] = swap;
    } else if (s_index === -1) {
      // Starter - > Bench
      var orig = window.fl_starter[p_index], swap;
      for (var z = 0; z < window.fl_bench.length; z++){
        if (!swap && window.fl_bench[z].player_id === 'noplayer'){
          s_index = z + 12;
          swap = window.fl_bench[z];
        }
      }
      if(!swap){
        swap = {player_id: "noplayer", player_name: "Empty", position: "BEN", position_accepts: ["QB","RB","WR","TE","K","DEF"]};
        s_index = z + 13;
      }
      // Processing
      var temp = swap.position;
      var temp2 = swap.position_accepts;

      swap.position_accepts = orig.position_accepts;
      swap.position = orig.position;

      orig.position_accepts = temp2;
      orig.position = temp;

      window.fl_bench[s_index-12] = orig;
      window.fl_starter[p_index] = swap;
    }
    // Sort out filled/empty classes
    var tr_1 = jQuery(jQuery('tr.starting, tr.bench')[p_index]);
    var tr_2 = jQuery(jQuery('tr.starting, tr.bench')[s_index]);
    if(tr_2.hasClass('empty')){
      tr_1.addClass('empty');
      tr_2.removeClass('filled');
    }
    // Assume tr_2 will always be filled
    tr_2.removeClass('empty');
    tr_2.addClass('filled');
    // Switch HTML
    var td_1 = tr_1.find('td:not(.team-position)');
    var td_2 = tr_2.find('td:not(.team-position)');
    for(var i = 0; i < td_1.length; i++){
      // Swap each td tag over individually
      var original = jQuery(td_1[i]).html();
      var orig_style = jQuery(td_1[i]).attr("style");
      var swapping = jQuery(td_2[i]).html();
      var swap_style = jQuery(td_2[i]).attr("style");

      jQuery(td_1[i]).html(swapping);
      jQuery(td_1[i]).attr("style", swap_style);
      jQuery(td_2[i]).html(original);
      jQuery(td_2[i]).attr("style", orig_style);
    }

    jQuery('.selectpicker').find('option').remove();
    reRenderSelectors();
    jQuery('.selectpicker').selectpicker('refresh');
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
    var starter_csv = '';
    for (var i = 0; i < window.fl_starter.length; i++){
      starter_csv += window.fl_starter[i].player_id;
      if (i !== (window.fl_starter.length-1)){
        starter_csv += ','
      }
    }
    var bench_csv = '';
    for (var j = 0; j < window.fl_bench.length; j++){
      if (window.fl_bench[j] && window.fl_bench[j].player_id !== 'noplayer') {
        if (bench_csv.length) {
          bench_csv += ','
        }
        bench_csv += window.fl_bench[j].player_id;
      }
    }
    var req = jQuery.post('/save-team/'+jQuery('#team-id-hidden').data('teamid')+'/',{
      "starters": starter_csv,
      "bench": bench_csv
    });
    // req.success(function() {
    //     alert('Team Saved!');
    //   }
    // );
  });
});
