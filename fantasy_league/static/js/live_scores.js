jQuery(function() {
  jQuery('.selectpicker').selectpicker({"width":"100px"});

  jQuery('.selectpicker').on('changed.bs.select', function (event, clickedIndex) {
    window.open(window.location.origin+'/live-scores/?week='+(clickedIndex+1),'_self')
  });
});
