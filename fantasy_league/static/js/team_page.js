jQuery(function() {
  jQuery('.selectpicker').selectpicker({"width":"76px"});

  jQuery('.selectpicker').on('changed.bs.select', function (event, clickedIndex) {
    // Change the visual lineup
    var new_pos = jQuery(event.currentTarget).find('option:nth-of-type('+(clickedIndex+1)+')').val();
    var current_pos_html = jQuery(jQuery('tr.'+new_pos.split('-')[0])[Number(new_pos.split('-')[1])-1]);
    var old_html = jQuery(event.currentTarget).parent().parent().parent();

    //Replace HTML
    var replacing_html = jQuery(jQuery('tr.'+new_pos.split('-')[0])[Number(new_pos.split('-')[1])-1]).html();
    jQuery(jQuery('tr.'+new_pos.split('-')[0])[Number(new_pos.split('-')[1])-1]).html(old_html.html());
    // Check new player can go to position
    if((current_pos_html.data("playerPos") === old_html.data("playerPos")) || old_html.hasClass('FLEX')){
      jQuery(event.currentTarget).parent().parent().parent().html(replacing_html);
    } else {
      // Player can't be placed into old slot. Put on bench.
      var empty_html = jQuery('tr.bench.empty').first().html();
      console.log(empty_html);
      jQuery('tr.bench.empty').first().html(replacing_html);
      old_html.html(empty_html);

      // Switch filled/empty classes
      jQuery('tr.bench.empty').first().removeClass('empty').addClass('filled');
      old_html.removeClass('filled').addClass('empty');
    }
  });
});
