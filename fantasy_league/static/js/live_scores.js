jQuery(function() {
  jQuery('.selectpicker').selectpicker({"width":"100px"});

  jQuery('.selectpicker').on('changed.bs.select', function (event, clickedIndex) {
    window.open(window.location.origin+'/live-scores/?week='+(clickedIndex+1),'_self')
  });

  // Implement Player Info Pop-Up
  jQuery('.live-score-player:not(.empty)').click(function(){
      // AJAX call some additional data on the player in
      jQuery.ajax('/ajax/player-info/'+(jQuery(this).find('#playerid').val())+'/');
  })
});
