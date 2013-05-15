(function($){
  var _xsrf = Tools.getCookie("_xsrf");

  // cal new category modal
  $(document).on('change', '#categories_select', function(){
    var self = $(this);
    if(self.val() === '创建新分类'){
      $("#add_category_input").val('');
      var modal = $("#add_category_modal");
      modal.reveal();
    }else{
      var cid = self.find(':selected').attr('cid');
      $("#category_id").val(cid);
    }
  });

  // do add new category
  $(document).on('click', '#do_add_category', function(){
    var cat = $("#add_category_input").val(),
        url = '/admin/category/add';
    $.ajax({
      type: 'POST',
      url: url,
      data: {category:cat, _xsrf:_xsrf},
      success: function(data){
        var obj = $.parseJSON(data);
        if(obj.success === 'true'){
          $("#category_id").val(obj.cid);
          $('#categories_select :selected').text(cat);
          $('#categories_select').append('<option>创建新分类</option>');
          $("#add_category_modal").trigger('reveal:close');
        }else{
          alert('数据库返回错误');
        }
      }
    });
  });

})(jQuery);
