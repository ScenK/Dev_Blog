(function($){
  // do add new property
  $(document).on('click', '#do_add_property', function(){
    var cat = $("#add_property_input").val();
    $("#category_id").val(cat);
    $('#categories_select :selected').text(cat);
    $('#categories_select').append('<option>创建新分类</option>');
    $("#add_category_modal").trigger('reveal:close');
  });
})(jQuery);
